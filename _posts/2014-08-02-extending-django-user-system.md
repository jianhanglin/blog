---
layout: post
title: 扩展Django用户系统
tags:
- django
- python
- user system
- web dev
---
Django内置的用户系统极大地减少了开发者的工作量，但是仍需要进行扩展才能适应特定程序。

### 用户模型

Django中，User对象是用户系统的核心，主要字段包括username、password、email、first\_name以及last\_name。如果要存储与用户相关的其他信息，就需要对User进行扩展。扩展有两种方法，一种是创建一个UserProfile类，并建立与User类的一对一映射关系，另一种是用自己实现的User类替换Django用户系统中默认的User类。

### 扩展已有的User模型

如果使用这种方法，数据库中将会有两个表，一张表存储基本用户信息，另一张表存储用户的额外信息，并通过一对一关系与基本用户信息表关联起来。下面的代码创建了UserProfile类，用来存储用户的额外信息：

~~~ {.python}
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User)   # 建立与User模型的一对一映射
    signature = models.CharField(max_length=200)
    # other attributes ...
~~~

这样，每次创建User对象的时候，都要手动创建UserProfile对象，因为UserProfile只是一个普通的Django模型而已。

### 替换默认的User模型

另一种方法是使用自己实现的User类替换默认的User类，例如在应用user_system中实现了User类，可以在工程的settings.py文件中进行如下设置：

~~~ {.python}
AUTH_USER_MODEL = 'user_system.User'
~~~

需要注意的是，这样做会改变数据表结构，因此替换默认的User之后需要执行`./manage.py syncdb`来同步数据库。另外，由于替换了默认的User模型，代码中不能再使用`django.contrib.auth.models.User`，而应使用`django.contrib.auth.get_user_model()`来引用。

自己实现User模型，需要至少提供Django内置User所具有的属性和方法，因此最简洁的方法是继承`django.contrib.auth.models.AbstractBaseUser`类，下面是一个自定义User模型的实例：

~~~ {.python}
from django.contrib.auth.models import AbstractBaseUser
class Account(AbstractBaseUser):

~~~
