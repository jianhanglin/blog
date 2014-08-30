---
layout: post
title: 为Pandoc Markdown添加TikZ支持
category: "blog"
---
Pandoc为Markdown添加了许多新特性，甚至数学公式都能借助MathJax完美地显示，然而我还想在Markdown中嵌入TikZ代码，这样画图也不需要使用单独软件了。

### Pandoc Filter

扩展Pandoc功能，首先想到的就是编写Pandoc的Filter，Filter相当于一个管道，输入是Pandoc抽象语法树，输出也是抽象语法树，其间可以进行任意的格式修改。在浏览Python写Filter的教程时，发现了[pandocfilters](https://github.com/jgm/pandocfilters)这个repo，在里面惊喜地发现了[tikz.py](https://github.com/jgm/pandocfilters/blob/master/examples/tikz.py)，代码如下：

~~~ {.python}
import hashlib
import re
import os
import sys
import shutil
from pandocfilters import toJSONFilter, Para, Image
from subprocess import Popen, PIPE, call
from tempfile import mkdtemp

imagedir = "tikz-images"

def sha1(x):
    return hashlib.sha1(x).hexdigest()

def tikz2image(tikz, filetype, outfile):
    tmpdir = mkdtemp()
    olddir = os.getcwd()
    os.chdir(tmpdir)
    f = open('tikz.tex', 'w')
    f.write("""\\documentclass{standalone}
               \\usepackage{tikz}
               \\begin{document}""")
    f.write(tikz)
    f.write("\n\\end{document}\n")
    f.close()
    p = call(["pdflatex", 'tikz.tex'], stdout=sys.stderr)
    os.chdir(olddir)
    if filetype == 'pdf':
        shutil.copyfile(tmpdir + '/tikz.pdf', outfile + '.pdf')
    else:
        call(["convert", tmpdir + '/tikz.pdf', outfile + '.' + filetype])
    shutil.rmtree(tmpdir)

def tikz(key, value, format, meta):
    if key == 'RawBlock':
        [fmt, code] = value
        if fmt == "latex" and re.match("\\\\begin{tikzpicture}", code):
            outfile = imagedir + '/' + sha1(code)
            if format == "html":
                filetype = "png"
            elif format == "latex":
                filetype = "pdf"
            else:
                filetype = "png"
            src = outfile + '.' + filetype
            if not os.path.isfile(src):
                try:
                    os.mkdir(imagedir)
                    sys.stderr.write('Created directory ' + imagedir + '\n')
                except OSError:
                    pass
                tikz2image(code, filetype, outfile)
                sys.stderr.write('Created image ' + src + '\n')
            return Para([Image([], [src,""])])

if __name__ == "__main__":
    toJSONFilter(tikz)
~~~

就算没有了解过Pandoc AST结构与Filter的写法，上面这段代码的逻辑应该也是很清晰的。首先查找所有以`\begin{tikzpicture}`开头的块，如果输出是LaTeX格式，那么转化成pdf格式（个人感觉完全没必要），如果输出是HTML以及其他格式，则转换为png格式，转换后的文件放在一个名叫`tikz-image`的子目录下，然后在将整个TikZ代码块替换成对图片文件的引用。

下面来看一下核心的格式转换部分，`tikz2image`函数用以实现此功能。函数首先创建一个临时文件`tikz.tex`，然后写入下面的内容：

~~~ {.latex}
\documentclass{standalone}
\usepackage{tikz}
\begin{document}
    % TikZ代码
\end{document}
~~~

将TikZ代码包围起来，形成了一个完整且合法的LaTeX文件，然后调用pdflatex进行格式转换，并将输出文件改名复制到`tikz-image`子目录下，完成。

### 与Jekyll的集成

> 想不到这一部分用了我两天才搞定，由于不熟悉Ruby语言走了好多弯路。

在Jekyll中使用Pandoc markdown语法，是通过一个插件完成的，因此，将TikZ Filter用在Jekyll上，自然的想法就是修改这个插件。浏览[jekyll-pandoc-plugin的源代码](https://github.com/dsanson/jekyll-pandoc-plugin/blob/master/pandoc_markdown.rb)，在其中发现了这样的函数：

~~~ {.ruby}
def convert(content)
    extensions = config_option('extensions', [])
    format = config_option('format', 'html5')
    PandocRuby.new(content, *extensions).send("to_#{format}")
end
~~~

这段代码实现的就是Markdown到HTML5的转换，使用了pandoc-ruby实现。我尝试了各种方法来加入自己的Filter，但是都没有成功，最终放弃pandoc-ruby，使用直接执行pandoc程序的方法：

~~~ {.ruby}
def convert(content)
    output = ''
    Open3::popen3("pandoc -f markdown -t html5 -S --mathjax --filter ./tikz.py") do |stdin, stdout, stderr|
        stdin.puts content
        stdin.close
        output = stdout.read
    end
    output
end
~~~

通过一种及其不优雅的方式，实现了Markdown语言中嵌入TikZ图形的功能。以后，绘制示意图可以直接在Markdown文件中完成，例如下面的代码绘制了一个圆。

~~~ {.latex}
\begin{tikzpicture}
    \draw[red,thick,dashed] (2,2) circle (3cm);
\end{tikzpicture}
~~~

渲染之后是这个样子：

\begin{tikzpicture}
    \draw[red,thick,dashed] (2,2) circle (3cm);
\end{tikzpicture}

