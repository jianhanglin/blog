---
layout: post
title: 使用GRUB引导自己的系统
category: osdev
tags:
- grub
- bootloader
- osdev
---
GRUB是一个强大的引导程序，使用GRUB引导自己的操作系统可以省去许多繁杂的初始化工作，让内核一开始就运行在保护模式下。GRUB遵循Multiboot规范，任何具有Multiboot header的文件都可以被GRUB加载并引导。

### GRUB Legacy or GRUB 2

GRUB有两个版本，早一些的GRUB被称作GRUB Legacy，现已停止开发。较新的叫做GRUB 2，是一个与GRUB Legacy**完全不同**的引导程序。GRUB 2的功能强大一些，但是用于引导自己的系统，还是GRUB Legacy更容易配置。

### 引导过程

计算机开机或重置时，首先执行的是加电自检（Power On Self Test，POST）过程，其中就包括检索可引导设备。现代计算机通常允许用户手动设定设备引导顺序，BIOS会按照这个顺序逐一查找可引导的设备。

判断一个设备是否可引导，标志就是这个设备第一个扇区的最后两个字节，如果第511个字节是`0x55`，第512个字节是`0xAA`，那么BIOS就认为这是一个可以引导的设备，并将这个设备的第一个扇区加载到内存地址`0x0000:0x7c00`处（实模式），然后跳转到那里开始执行，这个扇区也叫做引导扇区。

引导扇区空间有限，因此大多数引导程序都会使用多级引导，即利用引导扇区加载第二级引导程序，再用第二级引导程序加载第三级……最终将内核载入内存，完成一些初始化操作并开始执行内核。

### Multiboot规范

Multiboot规范是GRUB所遵循的标准，要让内核镜像能够通过GRUB引导，就必须符合Multiboot规范。根据规范，内核镜像中必须包含一个名为Multiboot Header的数据结构，格式如下表所示：

| 偏移 | 类型 | 字段名称 |
|:------:|:----:|:-------:|
| 0 | uint32 | magic |
| 4 | uint32 | flags |
| 8 | uint32 | checksum |
| 12 | uint32 | header\_addr |
| 16 | uint32 | load\_addr |
| 20 | uint32 | load\_end\_addr |
| 24 | uint32 | bss\_end\_addr |
| 28 | uint32 | entry\_addr |
| 32 | uint32 | mode_type |
| 36 | uint32 | width |
| 40 | uint32 | height |
| 44 | uint32 | depth |

具体字段的描述请参见[Multiboot规范](http://www.gnu.org/software/grub/manual/multiboot/multiboot.html#Specification)，这里要注意的是，Multiboot Header必须是4字节对齐的，且这个数据结构的第一个双字必须出现在镜像文件前8K字节内。

Multiboot规范中说，如果镜像文件是ELF格式，则不必提供地址信息（即\*\_addr字段）。然而，使用ELF固然方便，但也有很多限制，内核最理想的格式仍然是纯二进制。

### Linker Script

通过LD链接脚本，可以指定内核镜像在内存中的布局，同时提供相关位置信息给其他源程序，下面就是一个链接脚本

~~~ {.ld}
OUTPUT_FORMAT(binary)
SECTIONS {
    . = 1M;
    .text : ALIGN(4) {
        seg_text_start_addr = .;
        *(.bootstrap)
        *(.text)
        seg_text_end_addr = .;
    } = 0x90
    .data : ALIGN(4) {
        seg_data_start_addr = .;
        *(.rodata);
        *(.data);
        seg_data_end_addr = .;
    } = 0x90
    .bss : ALIGN(4) {
        seg_bss_start_addr = .;
        *(COMMON);
        *(.bss);
        seg_bss_end_addr = .;
    } = 0x90
}
~~~

这个脚本首先指定输出格式为二进制格式，然后设置起始地址为1M，顺序定义代码段、数据段，以及BSS段，同时用符号记录各个段的起止地址，这些符号可以再C语言、汇编语言的程序中引用。

### Header in Assembly

上面的链接脚本中，使用了一个名为`bootstrap`的节，这就是定义Multiboot header的节，汇编代码如下（NASM格式）：

~~~ {.assembly}
extern seg_data_end_addr
extern seg_bss_end_addr

MB1_MAGIC equ 0x1BADB002
MB1_FLAGS equ 1<<0|1<<1|1<<16
MB1_CHECK equ -(MB1_MAGIC+MB1_FLAGS)

[section .bootstrap]
[bits 32]

multiboot_start:
        jmp     multiboot_entry

ALIGN 4
multiboot_header:
        dd      MB1_MAGIC
        dd      MB1_FLAGS
        dd      MB1_CHECK

        dd      multiboot_header    ; header_addr
        dd      multiboot_start     ; load_addr
        dd      seg_data_end_addr   ; load_end_addr
        dd      seg_bss_end_addr    ; bss_end_addr
        dd      multiboot_entry     ; entry_addr

multiboot_entry:
        ;; code goes here
~~~

### 制作可引导软盘镜像

内核准备好之后，需要复制到一个安装了GRUB的存储器上在能用来启动计算机。最简单的方式就是找一个预装了GRUB的镜像，使用`mount`命令挂载，复制内核文件，编辑`menu.lst`并解除挂载即可。这个可引导镜像就可以用在虚拟机上进行测试了。

