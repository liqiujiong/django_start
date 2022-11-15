# Django 0.4


## Django start
### 新建项目
```
django-admin startprojec django_start
```
### 新建目录结构
```
django_start/
    manage.py       # 管理 Django 项目的命令行工具
    django_start/
        __init__.py
        settings.py # Django 项目的配置文件
        urls.py     # Django 项目的 URL 声明，就像你网站的“目录”
        asgi.py     # 项目的运行在 ASGI 兼容的 Web 服务器上的入口。
        wsgi.py     # 项目的运行在 WSGI 兼容的Web服务器上的入口。
```
### 运行项目
```
python manage.py runserver 0.0.0.0:8000
```

### 新建应用
Django中存在`项目`和`应用`的概念，一个项目中可以包括很多个应用，以应用为单位进行开发项目。
```
python manage.py startapp polls
```
通过在django_start/urls.py使用path()进行路径匹配，将polls/路径的请求通过include()发到polls/urls应用中，polls/urls中又将请求直接发给view，直接返回HttpResponse。

#### - path(route,view,kwargs,name)
1. route: 必选，路径匹配，例，URLconf 在处理请求 https://www.example.com/myapp/ 时，它会尝试匹配 myapp/
2. view: 必选，route匹配到后，就会调用这个view函数，并传入一个 HttpRequest 对象作为第一个参数
3. kwargs: 可选，将参数传递给目标视图函数
4. name: 可选，为url取名，可以在django其他地方使用它\
---
## Django Database
### 配置Mysql数据库

1. 通过django_start/settings.py文件，修改DATABASES配置块，更换默认sqlite数据库
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django_db',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': 3306,
        'ATOMIC_REQUEST': True,
        'OPTIONS': {
        	"init_command": "SET default_storage_engine=INNODB",
        }
    }
}
'''
'NAME':要连接的数据库，连接前需要创建好
'USER':连接数据库的用户名
'PASSWORD':连接数据库的密码
'HOST':连接主机，默认本机
'PORT':端口 默认3306
'ATOMIC_REQUEST': True,
设置为True统一个http请求对应的所有sql都放在一个事务中执行（要么所有都成功，要么所有都失败）。
是全局性的配置， 如果要对某个http请求放水（然后自定义事务），可以用non_atomic_requests修饰器
设置创建表的存储引擎为MyISAM，INNODB
'''
```
2. 安装mysql客户端
```
pip install mysqlclient
```
### 开启Django默认应用
django自带了`INSTALLED_APPS`中所描述的内置应用，这些应用默认是启用着的，需要通过插件通过Django在数据库中为它们创建一些表去开启他们
```
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```
使用migrate命令创建相关数据库表
```
python manage.py migrate
```
- migrate: 能根据 mysite/settings.py 文件中的数据库配置创建表，以及为项目中的应用创建任何必要的数据库表。

### 创建模型
作为以数据驱动的Django，Django中以模型至上，一个应用的第一步就是先创建模型。
为polls应用创建模型
```
# polls/models.py
from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE) # 一个多对一的关系
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
```
创建方式和同为ORM框架的sqlchemy类似，django模型继承django.db.models.Model类也相当于数据库中的一张表，不同的是这里`Field`，通过不同的field定义不同的表字段。而且如CharField的max_length不仅定义了字段最长长度，也会被用于数据校验。

### 模型激活
将polls应用（polls/apps的PollsConfig类）插入到Django项目中，在文件 mysite/settings.py 中 INSTALLED_APPS 新增路径后，它看起来像这样：
```
INSTALLED_APPS = [
    'polls.apps.PollsConfig',
    'django.contrib.admin',
    ...
    'django.contrib.staticfiles',
]
```
运行manage.py激活
```
python manage.py makemigrations polls
<!--
返回结果：
Migrations for 'polls':
  polls\migrations\0001_initial.py
    - Create model Question
    - Create model Choice
-->
```
-  makemigrations 命令，Django 会检测你对模型文件的修改（在这种情况下，你已经取得了新的），并且把修改的部分储存为进行一次`迁移`。

### `迁移`记录
执行迁移makemigrations 命令，django会记录一个模型变化记录，它被储存在 polls/migrations/0001_initial.py 里。
- sqlmigrate命令：可以将一个迁移文件转为一个SQL语句输出,可以用来创建数据库表
```
--
-- Create model Question
--
CREATE TABLE `polls_question` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `question_text` varchar(200) NOT NULL, `pub_date` datetime(6) NOT NULL);
--
-- Create model Choice
--
CREATE TABLE `polls_choice` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `choice_text` varchar(200) NOT NULL, `votes` integer NOT NULL, `question_id` bigint NOT NULL);
ALTER TABLE `polls_choice` ADD CONSTRAINT `polls_choice_question_id_c5b4b260_fk_polls_question_id` FOREIGN KEY (`question_id`) REFERENCES `polls_question` (`id`);

```

- check命令：可以帮助你检查项目中的问题，并且在检查过程中不会对数据库进行任何操作。
- migrate命令：在数据库里创建新定义的模型的数据表

或者使用migrate命令，在数据库把表创建出来
```
python manage.py migrate
```
tip: 当使用migrate命令创建了表后，又重新删除掉表，会发现重新执行没办法创建表提示“No migrations to apply.”,因为`migrate会在数据库表中进行记录`，记录了迁移点，所以重新执行创建不了，解决办法就是在数据库表django_migrations中删除掉name为0001_initial的最后一条记录

Django内置的这个迁移确实非常强大，能让你在开发过程中持续的改变数据库结构而不需要重新删除和创建表 - 它专注于使数据库平滑升级而不会丢失数据。
改变模型只需要简单一下三步：
1. 编辑 models.py 文件，改变模型。
2. 运行 python manage.py makemigrations 为模型的改变生成迁移文件。
3. 运行 python manage.py migrate 来应用数据库迁移。

### Django API 