"""biyesheji2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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


from bs_app import views
from django.contrib import admin
from django.urls import path, include, re_path
from biyesheji2.settings import MEDIA_ROOT
from django.views.static import serve

# 可以设置访问页面去调用其他方法
urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    # admin
    path('admin/', admin.site.urls),
    # common
    path('index/', views.index),
    path('logout/', views.logout),
    path('mainpage/', views.mainpage),
    # user
    path('loginUser/', views.loginUser),
    path('missionChose/', views.missionChose),
    path('imageShow/', views.imageShow),
    path('tagChose/', views.tagChose),
    # client
    path('loginClient/', views.loginClient),
    path('upload/', views.upload),
    path('missionUpload/', views.missionUpload),
    path('missionShow/', views.missionShow),

]
