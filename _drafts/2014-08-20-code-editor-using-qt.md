---
layout: post
title: 使用Qt编写代码编辑器
---
Qt提供的类库与机制使得编写建议的代码编辑器非常容易，示例程序中就包含有代码编辑、语法高亮两个项目，可以用来学习。

### 文本编辑功能

代码也是文本，因此对于代码编辑器而言，首先需要完成文本编辑的功能。文本编辑看似简单，实际上包含很多内容，因此，最好使用一个现有的控件，`QPlainTextEdit`是最理想的选择。

Qt自带了许多完成文本编辑功能的控件，`QPlainTextEdit`是专门为编辑纯文本而生的控件，在实现上做了许多优化。因此，适合将我们的编辑器控件实现为`QPlainTextEdit`的子类：

~~~ {.cpp}
class Editor : public QPlainTextEdit {
    Q_OBJECT
public:
    explicit Editor(QWidget *parent = 0);
    virtual ~Editor();
};
~~~

为了适应代码编辑，应该使用等宽字体，并将Tab宽度设为合适的值（例如4个空个字符的宽度），可以在构造函数中设置如下：

~~~ {.cpp}
Editor::Editor(QWidget *parent) {
    QFont font("Monospace", 12);
    font.setStyleHint(QFont::TypeWriter);
    font.setHintingPreference(QFont::PreferNoHinting);
    QFontMetrics metrics(font);
    this->setFont(font);
    this->setTabStopWidth(metrics.width("    "));
}
~~~
