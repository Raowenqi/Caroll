"""
URL configuration for Caroll project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app01 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('send/sms', views.send_sms, name='send_sms'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('home', views.home, name='home'),
    path('light', views.light, name='light'),
    path('home2', views.home2, name='home2'),
    path('', views.home2, name='h'),
    path('author', views.author, name='author'),
    path('demoIndex', views.demoIndex, name='demoIndex'),
    path('nxh', views.nxh, name='nxh'),
    path('shicha', views.shicha, name='shicha'),
    path('pubuliu', views.pubuliu, name='pubuliu'),
    path('pubuliu2', views.pubuliu2, name='pubuliu2'),
    path('pubuliu3', views.pubuliu3, name='pubuliu3'),
    path('maoboli', views.maoboli, name='maoboli'),
    path('awa', views.awa, name='awa'),
    path('index', views.index, name='index'),
    path('upload', views.upload, name='upload'),
    path('personInfo', views.personInfo, name='personInfo'),
    path('logout', views.logout, name='logout'),
]
