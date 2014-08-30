---
layout: post
title: 现代OpenGL编程
---
所谓现代OpenGL，主要指OpenGL版本3.0以上。与之前的版本相比，OpenGL 3.0引入了Shader、Profile等许多全新的概念，使得3.0之后的OpenGL与之前版本有很大区别。

### 窗口系统

要将渲染后的3D图形显示在窗口中，就需要窗口系统的支持，许多第三方库都提供了非常友好的支持，如Glut、FreeGlut、GLFW等。这里使用的是一个不常见于OpenGL的框架——SDL。SDL常用于编写2D游戏，但是其也有3D支持，而SDL中的3D正是通过OpenGL来实现的。


