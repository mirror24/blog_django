"""my_blog URL Configuration

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
from django.urls import path, include

import notifications.urls

from article.views import article_list
# 参数article分配了app的访问路径
# 'include' 将路径分发给下一步处理
# 'namespace' 可以保证反查到唯一的url，即使不同的app使用了相同的url
#
# 存放映射关系的列表
urlpatterns = [
    path(
        'admin/',
        admin.site.urls
    ),
    # 配置app的url
    path(
        'article/',
        include('article.urls', namespace='article')
    ),
    # 用户管理
    path(
        'userprofile/',
        include('userprofile.urls', namespace='userprofile')
    ),
    # 密码重置-第三方库
    path(
        'password-reset/',
        include('password_reset.urls')
    ),
    # 评论
    path(
        'comment/',
        include('comment.urls', namespace='comment')
    ),
    # 通知
    path(
        'inbox/notifications/',
        include(notifications.urls,namespace='notifications')
    ),
    # notice
    path(
        'notice/',
        include('notice.urls', namespace='notice')
    ),
    # django-allauth
    path(
        'accounts/',
        include('allauth.urls')
    ),
    # home
    path(
        '',
        article_list,
        name='home'
    ),
]
# 通过path将根路径为article的访问都分发给article这个app去处理
# 但app通常有多个页面地址，因为还需要app自己也有一个路由分发，就是指article.urls

# 上传图片
# 新引入的模块
from django.conf import settings
from django.conf.urls.static import static

# 添加这行
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
