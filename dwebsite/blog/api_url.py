from django.urls import path
from blog import api

urlpatterns = [
    #文章管理、
      #文章发布
      path('add-article/',api.add_article),
      #文章列表
      path('article-list/',api.articleList),
      #文章删除
      path('delete-article/',api.deleteArticle),
    #用户管理
      #登录
      path('dweb-login/',api.dweb_login),
      #注册
      path('dweb-register/',api.dweb_register),
      #自动登录
      path('auto-login/',api.dweb_autoLogin),
      #登出
      path('dweb-logout/',api.dweb_logout),
      #鉴权
      path('dweb-checkperm/',api.dweb_checkPerm),
      #用户列表
      path('dweb-userlist/',api.dweb_userlist),
    #用户组
      path('dweb-group/',api.dweb_group),
    #栏目管理
      path('dweb-lanmu/',api.dweb_lanmu),
]