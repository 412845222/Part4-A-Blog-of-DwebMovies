from django.urls import path
from blog import api

urlpatterns = [
    path('add-article/',api.add_article),
    #用户管理
      #登录
      path('dweb-login/',api.dweb_login),
      #注册
      path('dweb-register/',api.dweb_register),
      #自动登录
      path('auto-login/',api.dweb_autoLogin),
      #登出
      path('dweb-logout/',api.dweb_logout)
]