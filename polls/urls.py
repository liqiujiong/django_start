from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'), # 通过django/urls.py的include路径polls/引导到这里
]