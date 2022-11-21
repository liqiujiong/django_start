# Django 0.4

## Django start

### 安装Django+mysqlclient

```bash
python -m pip install Django
pip install mysqlclient
```

### 新建项目

```bash
django-admin startprojec django_start
```

### 新建目录结构

```bash
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

```bash
python manage.py runserver 0.0.0.0:8001
```

### 新建应用

Django中存在`项目`和`应用`的概念，一个项目中可以包括很多个应用，以应用为单位进行开发项目。

```bash
python manage.py startapp polls
```

通过在django_start/urls.py使用path()进行路径匹配，将polls/路径的请求通过include()发到polls/urls应用中，polls/urls中又将请求直接发给view，直接返回HttpResponse。

#### - path(route,view,kwargs,name)

1. route: 必选，路径匹配，例，URLconf 在处理请求 <https://www.example.com/myapp/> 时，它会尝试匹配 myapp/
2. view: 必选，route匹配到后，就会调用这个view函数，并传入一个 HttpRequest 对象作为第一个参数
3. kwargs: 可选，将参数传递给目标视图函数
4. name: 可选，为url取名，可以在django其他地方使用它\

---

## Django Database

### 配置Mysql数据库

1. 通过django_start/settings.py文件，修改DATABASES配置块，更换默认sqlite数据库

    ```python
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

    ```bash
    pip install mysqlclient
    ```

### 开启Django默认应用

django自带了`INSTALLED_APPS`中所描述的内置应用，这些应用默认是启用着的，需要通过插件通过Django在数据库中为它们创建一些表去开启他们

```python
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

```bash
python manage.py migrate
```

- migrate: 能根据 mysite/settings.py 文件中的数据库配置创建表，以及为项目中的应用创建任何必要的数据库表。

### 创建模型

作为以数据驱动的Django，Django中以模型至上，一个应用的第一步就是先创建模型。
为polls应用创建模型

```python
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

```python
INSTALLED_APPS = [
    'polls.apps.PollsConfig',
    'django.contrib.admin',
    ...
    'django.contrib.staticfiles',
]
```

运行manage.py激活

```python
python manage.py makemigrations polls
"""
Return：
Migrations for 'polls':
  polls\migrations\0001_initial.py
    - Create model Question
    - Create model Choice
"""
```

- makemigrations 命令，Django 会检测你对模型文件的修改（在这种情况下，你已经取得了新的），并且把修改的部分储存为进行一次`迁移`。

### `迁移`记录

执行迁移makemigrations 命令，django会记录一个模型变化记录，它被储存在 polls/migrations/0001_initial.py 里。

- sqlmigrate命令：可以将一个迁移文件转为一个SQL语句输出,可以用来创建数据库表

```sql
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

```bash
python manage.py migrate
```

tip: 当使用migrate命令创建了表后，又重新删除掉表，会发现重新执行没办法创建表提示“No migrations to apply.”,因为`migrate会在数据库表中进行记录`，记录了迁移点，所以重新执行创建不了，解决办法就是在数据库表django_migrations中删除掉name为0001_initial的最后一条记录

Django内置的这个迁移确实非常强大，能让你在开发过程中持续的改变数据库结构而不需要重新删除和创建表 - 它专注于使数据库平滑升级而不会丢失数据。
改变模型只需要简单一下三步：

1. 编辑 models.py 文件，改变模型。
2. 运行 python manage.py makemigrations 为模型的改变生成迁移文件。
3. 运行 python manage.py migrate 来应用数据库迁移。

### Django Shell --> Database API

通过manage.py shell命令，这种方式进入交互终端，会设置 `DJANGO_SETTINGS_MODULE` 环境变量导入Django项目，从而在这个终端中可以直接调用Django提供的API，例如直接进行数据库的交互操作

```python
>>> from polls.models import Choice, Question
# 获取所有
>>> Question.objects.all()
# <QuerySet []>

# 新增
>>> from django.utils import timezone
>>> q = Question(question_text="What's new?", pub_date=timezone.now())
>>> q.save()
>>> q.id
# 1

# 修改
>>> q.question_text
# "What's new?"
>>> q.pub_date
# datetime.datetime(2012, 2, 26, 13, 0, 0, 775217, tzinfo=datetime.timezone.utc)
>>> q.question_text = "What's up?"
>>> q.save()

# 获取所有
>>> Question.objects.all()
# <QuerySet [<Question: Question object (1)>]>
```

model返回`<Question: Question object (1)>`可以通过对model新增__str__方法实现返回字符串。
重新打开python manage.py shell

```python
>>> from polls.models import Choice, Question

>>> Question.objects.all()
# <QuerySet [<Question: What's up?>]>

# 筛选
>>> Question.objects.filter(id=1)
# <QuerySet [<Question: What's up?>]>
>>> Question.objects.filter(question_text__startswith='What')
# <QuerySet [<Question: What's up?>]>

# 日期筛选, __year双下划线筛选年份
>>> from django.utils import timezone
>>> current_year = timezone.now().year
>>> Question.objects.get(pub_date__year=current_year)
# <Question: What's up?>

# 筛选-不存在的会抛出DoesNotExist错误
>>> Question.objects.get(id=2)
# Traceback (most recent call last):
#     ...
# DoesNotExist: Question matching query does not exist.

# 通过主键查找，与直接get(id=1)一样
>>> Question.objects.get(pk=1)
# <Question: What's up?>

# 获取一个Question, 一对多关系操作
>>> q = Question.objects.get(pk=1)

# Choice和Question形成多对一关系，通过choice的外键关联，可以在Question使用choice_set进行获取关联值
>>> q.choice_set.all()
<QuerySet []>

# 为Question创建choice
>>> q.choice_set.create(choice_text='Not much', votes=0)
# <Choice: Not much>
>>> q.choice_set.create(choice_text='The sky', votes=0)
# <Choice: The sky>
>>> c = q.choice_set.create(choice_text='Just hacking again', votes=0)

>>> c.question
# <Question: What's up?>

# And vice versa: Question objects get access to Choice objects.
>>> q.choice_set.all()
# <QuerySet [<Choice: Not much>, <Choice: The sky>, <Choice: Just hacking again>]>
>>> q.choice_set.count()
# 3

# 使用双下划线__year进行筛选question中的年份
>>> Choice.objects.filter(question__pub_date__year=current_year)
# <QuerySet [<Choice: Not much>, <Choice: The sky>, <Choice: Just hacking again>]>

# 使用__startswith筛选外键值
>>> c = q.choice_set.filter(choice_text__startswith='Just hacking')
>>> c.delete()
```

### Django admin

上面开启了内置应用，此时通过/admin，已经可以访问到登录页面了，账号的话通过manage.py创建admin账号：

```bash
python manage.py createsuperuser
```

#### 在admin中新增我们自己写的polls应用

需要在polls的应用中进行注册，/polls/admin.py加入以下代码

```python
from django.contrib import admin

from .models import Question

admin.site.register(Question)
```

就可以在admin管理面板中管理Polls应用的相关模型

## View视图

在 Django 中，网页和其他内容都是从视图派生而来。每一个视图表现为一个 Python 函数（或者说方法，如果是在基于类的视图里的话）。Django 将会根据用户请求的 URL 来选择使用哪个视图。

URL 样式是 URL 的一般形式 - 例如：/newsarchive/\<year>/\<month>/。

Django 使用了 'URLconfs' 来配置URL，将 URL 和视图关联起来。

### 视图入门

```python
#polls\views.py
def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
```

新视图添加进 polls.urls 模块里，使用 url() 函数进行调用

```python
#polls\urls.py
from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    # ex: /polls/5/
    path('<int:question_id>/', views.detail, name='detail'),
    # ex: /polls/5/results/
    path('<int:question_id>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
```

现在通过不同的url路径就可以打开不同的视图，例如访问`/polls/34/`将会访问跳到detail视图中，页面会显示“You're looking at question 34.”

- Django匹配过程：

    当某人请求你网站的某一页面时——比如说， "/polls/34/" ，Django 将会载入 django_start.urls 模块，因为这在配置项 ROOT_URLCONF 中设置了。然后 Django 寻找名为 urlpatterns 变量并且按序匹配正则表达式。在找到匹配项 'polls/'，它切掉了匹配的文本（"polls/"），将剩余文本——"34/"，发送至 'polls.urls' URLconf 做进一步处理。在这里剩余文本匹配了 '\<int:question_id>/'，使得我们 Django 以如下形式调用 detail():

    ```python
    detail(request=<HttpRequest object>, question_id=34)
    ```

### 编写一个视图

每个视图必须要做的只有两件事：

  1. 进行业务操作如数据增删改查，或者你可以做任何你想做的事。
  2. 返回一个包含被请求页面内容的 HttpResponse 对象，或者抛出一个异常，比如 Http404。

接下来我们通过修改polls的视图，进行查询数据库，让它能展示数据库里以发布日期排序的最近 5 个投票问题。

1. 创建template目录，通过使用 Django 的模板系统，创建视图，将页面的显示效果从视图代码中分离出来。

    在你的 polls 目录里创建一个 templates 目录。Django 将会在这个目录里查找模板文件。

    > 项目的 TEMPLATES 配置项描述了 Django 如何载入和渲染模板。默认的设置文件设置了 DjangoTemplates，并将 APP_DIRS 设置成了 True。这一选项将会让 DjangoTemplates 在每个 INSTALLED_APPS 文件夹中寻找 "templates" 子目录。这就是为什么尽管我们没有像在第二部分中那样修改 DIRS 设置，Django 也能正确找到 polls 的模板位置的原因。

2. 在你刚刚创建的 templates 目录里，再创建一个目录 polls，然后在其中新建一个文件 index.html 。

    你的模板文件的路径应该是`polls/templates/polls/index.html` 。因为``app_directories`` 模板加载器是通过上述描述的方法运行的，所以 Django 可以引用到 polls/index.html 这一模板了。
    > 虽然我们现在可以将模板文件直接放在 polls/templates 文件夹中（而不是再建立一个 polls 子文件夹），但是这样做不太好。Django 将会选择第一个匹配的模板文件，如果你有一个模板文件正好和另一个应用中的某个模板文件重名，Django 没有办法 区分 它们。我们需要帮助 Django 选择正确的模板，最好的方法就是把他们放入各自的 命名空间 中，也就是把这些模板放入一个和 自身 应用重名的子文件夹里。

3. 完成html模板代码编写

    ```html
    <!-- polls\templates\polls\index.html -->
    <!DOCTYPE html>
    <body>
    {% if latest_question_list %}
    <ul>
    {% for question in latest_question_list %}
        <li><a href="/polls/{{ question.id }}/">{{ question.question_text }}</a></li>
    {% endfor %}
    </ul>
    {% else %}
        <p>No polls are available.</p>
    {% endif %}
    </body>
    </html>
    ```

4. 更新一下 polls/views.py 里的 index 视图来使用模板

    ```python
    from django.http import HttpResponse
    from django.template import loader

    from .models import Question


    def index(request):
        latest_question_list = Question.objects.order_by('-pub_date')[:5]
        template = loader.get_template('polls/index.html')
        context = {
            'latest_question_list': latest_question_list,
        }
        return HttpResponse(template.render(context, request))
    ```

    loader.get_template 载入 polls/index.html 模板文件，并且向它传递一个上下文(context)。这个上下文是一个字典，它将模板内的变量映射为 Python 对象。

### template.render()

载入模板，填充上下文，再返回由它生成的 **HttpResponse** 对象

Django也提供了快捷的使用方式：

```python

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)
```

### 抛出 404 错误

```python
# polls\views.py
from django.http import Http404
from django.shortcuts import render

from .models import Question
# ...
def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question': question})
```

```html
<!-- polls\templates\polls\detail.html -->
<!DOCTYPE html>
<body>
  {{ question }}
</body>
</html>
```

当访问不到详细的Question时,会抛出404错误,Django也提供了相应的快捷函数:

- **快捷函数：[get_object_or_404()](https://docs.djangoproject.com/zh-hans/4.1/topics/http/shortcuts/#get-object-or-404)**

    当用 get() 函数获取一个对象，如果不存在就抛出 Http404 错误。下面是修改后的详情 detail() ：

    ```python
    from django.shortcuts import get_object_or_404, render

    from .models import Question
    # ...
    def detail(request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        return render(request, 'polls/detail.html', {'question': question})
    ```

    > 为什么我们使用辅助函数 get_object_or_404() 而不是自己捕获 ObjectDoesNotExist 异常呢？还有，为什么模型 API 不直接抛出 ObjectDoesNotExist 而是抛出 Http404 呢？

    因为这样做会增加模型层和视图层的耦合性。指导 Django 设计的最重要的思想之一就是要保证松散耦合。一些受控的耦合将会被包含在 [django.shortcuts](https://docs.djangoproject.com/zh-hans/4.1/topics/http/shortcuts/#module-django.shortcuts) 模块中。


### 模板操作

在detail.html页面，我们传入了我们找到的Question，在模板中Django是如何使用这个question，最后进行显示出来的呢？
> 首先 Django 尝试对 question 对象使用字典查找（也就是使用 obj.get(str) 操作），如果失败了就尝试属性查找（也就是 obj.str 操作），结果是成功了。如果这一操作也失败的话，将会尝试列表查找（也就是 obj[int] 操作）。

修改detail.html，当question查找到值，就会在页面上渲染出来

```html
<!-- polls\templates\polls\detail.html -->
<!DOCTYPE html>
<body>
  <h1>{{ question.question_text }}</h1>
  <ul>
  {% for choice in question.choice_set.all %}
      <li>{{ choice.choice_text }}</li>
  {% endfor %}
  </ul>
</body>
</html>
```

### 去除模板硬编码

我们在 polls/index.html 里编写投票链接时，链接是硬编码的：

```html
<li><a href="/polls/{{ question.id }}/">{{ question.question_text }}</a></li>
```

硬编码即在模板中写死了URL，这种强耦合的连接写法，如果应用路径一发生变动，修改起来会非常麻烦，因为在每个地方都要改，而且模板中没办法被索引到。Django官方推荐使用`{% url %}`标签替代它：

```python
<li><a href="{% url 'detail' question.id %}">{{ question.question_text }}</a></li>
```

`{% url %}`的工作方式是通过polls.urls中定义url时设置的name参数进行匹配的。


### 为URL设置命名空间

上文使用`{% url 'detail' %}`标签，我们的项目中可能有很多不同应用下的detail，因此出现这种情况，为了区分是哪个应用的，我们需要为应用设置命名空间：

1. 修改polls/urls.py，加上 app_name 设置命名空间：

   ```python
   from django.urls import path

    from . import views

    app_name = 'polls'
    urlpatterns = [
        path('', views.index, name='index'),
        path('<int:question_id>/', views.detail, name='detail'),
        path('<int:question_id>/results/', views.results, name='results'),
        path('<int:question_id>/vote/', views.vote, name='vote'),
    ]
   ```

2. 修改polls/index.html，指向具有命名空间的详细视图：

   ```html
    <li><a href="{% url 'polls:detail' question.id %}">{{ question.question_text }}</a></li>
   ```

## Django表单