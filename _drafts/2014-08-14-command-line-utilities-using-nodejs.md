---
layout: post
title: 用Node.js编写命令行程序
---
Node.js通常用来编写网络应用程序，然而它的能力不止于此。JavaScript是一种通用目的的编程语言，因此用它可以完成任何事情，包括编写命令行应用程序。

例如，下面的代码就创建了一个最简单的程序：

~~~ {.javascript}
#! /usr/bin/env node
console.log('Hello, world!')
~~~

给这文件赋予可执行权限之后，就可以在命令行下执行了，执行之后将会看到“Hello, world!”的输出。

命令行程序需要处理命令行参数，Node.js的命令行参数通过全局变量`process.argv`传递，这是一个数组
