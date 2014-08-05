---
layout: post
title: Haskell编程
---
> 我尝试Haskell编程的目的仅仅是为了编写Pandoc[脚本](http://johnmacfarlane.net/pandoc/scripting.html)，向Pandoc的Markdown添加tikZ画图的支持。

### 安装运行

在Linux下，运行Haskell可以安装GHC（The Glasgow Haskell Compilation System）：

~~~ {.bash}
sudo apt-get install ghc
~~~

安装完成后，输入`ghci`便可以启动GHC的交互式编程环境。

### 编程

Haskell是一门函数是编程语言，最基本的单位就是函数。Haskell函数名由小写英文字母开始，后跟任意多的英文字母、数字以及单引号。定义函数的语法如下：

~~~ {.haskell}
函数名 输入 = 输出
~~~

例如下面的代码定义了一个函数increase，接受一个输入，加一后返回：

~~~ {.haskell}
increase i = i+1
~~~

~~~ {.haskell}
~~~

