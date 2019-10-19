"""book URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from shuchongwo import views as shuchongwo_views
from check import views as check_views
from admintool import views as tools_views
from myUpload import views as myupload
urlpatterns = [
    path('',shuchongwo_views.index),
    path('index',shuchongwo_views.index),
    path('login',shuchongwo_views.login),
    path('registered',shuchongwo_views.registered),
    path('user/<int:r_uid>',shuchongwo_views.User,name='user'),
    path('search',shuchongwo_views.Search),
    path('book/<int:bid>',shuchongwo_views.Book,name='book'),
    path('ranklist',shuchongwo_views.RankList),
    path('book_ressources',myupload.book_resources),
    path('book_pinglun',myupload.book_pinglun),
    path('book_r',myupload.book_r),
    path('del',myupload.delc),
    path('delr',myupload.delr),
    path('check_number',check_views.checkNumber),
    path('check_name',check_views.check_username),
    path('check_num',check_views.check_num),
    path('Logout',shuchongwo_views.Logout),
    path('admin/', admin.site.urls),
    path('updatebooks',tools_views.updatabooks),
    path('ct',tools_views.createTop),
]
