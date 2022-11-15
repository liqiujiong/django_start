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
```
python manage.py startapp polls
```
通过在django_start/urls.py使用path()进行路径匹配，将polls/路径的请求通过include()发到polls/urls应用中，polls/urls中又将请求直接发给view，直接返回HttpResponse。

#### - path(route,view,kwargs,name)
1. route: 必选，路径匹配，例，URLconf 在处理请求 https://www.example.com/myapp/ 时，它会尝试匹配 myapp/
2. view: 必选，route匹配到后，就会调用这个view函数，并传入一个 HttpRequest 对象作为第一个参数
3. kwargs: 可选，将参数传递给目标视图函数
4. name: 可选，为url取名，可以在django其他地方使用它