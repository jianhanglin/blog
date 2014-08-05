---
layout: post
title: 使用Jekyll搭建静态博客
---

> Jekyll is a simple, blog-aware, static site generator. It takes a template directory containing raw text files in various formats, runs it through Markdown (or Textile) and Liquid converters, and spits out a complete, ready-to-publish static website suitable for serving with your favorite web server.

经过几天的折腾，这个用Jekyll搭成的静态博客基本成型了。虽然最终的博客外观非常简单，但是编写模板和样式还是占用了我大量的时间。

### 使用Pandoc作为Markdown引擎

Pandoc对Markdown语法进行了许多扩展，大大增强了Markdown的能力，这也是我采用Pandoc的原因。但是，Pandoc并不是Jekyll默认支持的Markdown引擎，因此需要额外的插件。

我使用的是David
Sanson写的[jekyll-pandoc-plugin](https://github.com/dsanson/jekyll-pandoc-plugin)。在安装了Pandoc和Gem包`pandoc-ruby`之后，直接将`pandoc_markdown.rb`复制到`_plugins`目录下即完成了安装。需要注意的是，在新版本的Jekyll中，需要将`pandoc_markdown.rb`第6、7行的`pygments_prefix`替换为`highlighter_prefix`，`pygments_suffix`替换为`highlighter_suffix`，这样脚本才能正常工作。

之后在`_config.yml`中进行如下配置，便可使用Pandoc引擎（同时启用MathJax）：

~~~{.yml}
markdown: pandoc
pandoc:
    extensions: [smart, mathjax]
~~~

### 用MathJax显示数学公式

幸亏有[MathJax](http://www.mathjax.org/)，在网页中排版数学公式变得非常轻松。

首先需要在jekyll-pandoc-plugin配置中启用MathJax扩展，并在模板文件中添加MathJax CDN的引用：

~~~ {.html}
<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS_HTML"></script>
~~~

这样，在Markdown中就可以直接嵌入LaTeX公式了，例如：

$$ G_{\mu \nu} = 8\pi G(T_{\mu \nu}+\rho_{\Lambda}g_{\mu \nu}) $$
$$ \int_a^b f'(x)dx = f(b) - f(a) $$

### 使用DISQUS实现用户评论

对博客来说，评论是必须的，有了[DISQUS](https://disqus.com/)，静态网站也可以有用户评论了。用第三方评论工具也省去了自己配置管理数据库的负担，可以说是最省心的一种方案。

### 还差什么

不管怎么说，现在的博客至少能用了，也能看了。有了公式与评论这两大特色，基本能满足我的需求。要说还有那些不完善，可以加强的地方，我觉得有以下几处：

- TikZ绘图
- RSS订阅功能
- 全文搜索
- 分类别浏览

