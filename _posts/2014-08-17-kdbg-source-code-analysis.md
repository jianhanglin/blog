---
layout: post
title: KDbg源码分析
category: qt
---
KDbg是一个图形化调试器前端，后端使用的是GDB。这是一个KDE桌面环境的软件，虽然KDE使用的是Qt技术，但KDE对Qt框架做了进一步的封装。

### 主程序

分析一款软件的源代码，首先找的就是main函数。在kdbg目录下，可以发现有一个main.cpp文件，打开后发现这正是定义main函数的文件。

main函数中首先创建了`KAboutData`的实例，虽然不了解KDE编程，但是从名字上应该可以看出，这是指定程序的“关于”信息。之后调用`KCmdLineArgs::init(argc, argv, &aboutData);`，从该能猜出，这一句作用是初始化命令行参数，将`argc`和`argv`两个参数传递了进去，之后创建`KCmdLineOptions`的对象，并逐一指定每个参数及其描述。

之后，看到了似曾相识的一句：

~~~ {.cpp}
KApplication app;
~~~

在main函数结尾处，能看到这样的代码：

~~~ {.cpp}
int rc = app.exec();
return rc;
~~~

KDE使用的是Qt技术，因此`KApplication`应该和`QApplication`的作用相同。上面的两段代码之间，还有大量的程序，但是关键的只有`DebuggerMainWnd`对象的定义以及调用成员函数`show()`的语句。从中可以看出，调试器主界面由`DebuggerMainWnd`类实现。

### DebuggerMainWnd

根据名字，恰好找到了dbgmainwnd.h和dbgmainwnd.cpp两个文件。打开一看，代码竟然有上千行之多，一行一行看显然不行。既然分析KDbg源代码的目的是分析其使用GDB实现图形化调试的原理，那么就应该直接寻找使用GDB的方法。注意到`DebuggerMainWnd`有一个`KDebugger`类型的成员变量`m_debugger`，从类型和变量的名字来看，这应该就是实现调试功能的地方。找到类`KDebugger`定义的`debugger.h`和`debugger.cpp`文件，这又是两个奇长无比的文件，但是从成员的定义上来看，可以肯定这就是负责管理被调试程序，调用GDB实现各种调试功能的类。利用搜索，找到了这样两行代码：

~~~ {.cpp}
// debugger process
DebuggerDriver* m_d;
~~~

其中的注释一下子点破天机，`DebuggerDriver`就是真正的调试器进程。然而有些奇怪的是，`KDebugger`类使用`DebuggerDriver`实现真正的调试，但是并没有创建实例化`DebuggerDriver`，而是让上一层使用者，也就是`DebuggerMainWnd`提供。KDbg被设计成支持多种编程语言的调试，因此写成了这样的代码。

### 
