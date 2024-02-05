# 引入path
from django.urls import path
# 引入views.py
from . import views

# 正在部署的应用的名称
#    可以不用配置，只要my_blog中配置了namespace 就不用
app_name = 'article'
# 必须配置app_name，否则会报错

# 根据用户请求的URL选择使用哪个视图
# 当请求article/article-list链接时
# 会调用views.py中的article_list函数，并返回渲染后的对象
# name 用于反查url地址。类似于给url起个名字

# url地址http://127.0.0.1:8000/article/article-list/
# 其中 127.0.0.1是调试服务器的本地地址
# article是项目路由 my_blog\urls.py分发的地址
# article-list是刚配置的article\urls.py应用分发的地址

# 存放映射关系的列表
urlpatterns = [
    # path函数将url映射到视图
    path(
        'article-list/',
        views.article_list,
        name='article_list'
    ),
    # 文章详情
    # <> 定义需要传递的参数
    # 需要传递名为 ID 的整数到视图函数中去
    # 老版本中没有 path 语法的
    path(
        'article-detail/<int:id>/',
        views.article_detail,
        name='article_detail'
    ),
    # 写文章
    path(
        'article-create/',
        views.article_create,
        name='article_create'
    ),
    # 删除文章
    path(
        'article-delete/<int:id>/',
        views.article_delete,
        name='article_delete'
    ),
    # 安全删除文章
    path(
        'article-safe-delete/<int:id>/',
        views.article_safe_delete,
        name='article_safe_delete'
    ),
    # 更新文章
    path(
        'article-update/<int:id>/',
        views.article_update,
        name='article_update'
    ),
    # 点赞 +1
    path(
        'increase-likes/<int:id>/',
        views.IncreaseLikesView.as_view(),
        name='increase_likes'
    ),

    # # 列表类视图
    # path('list-view/', views.ArticleListView.as_view(), name='list_view'),
    # # 详情类视图
    # path('detail-view/<int:pk>/', views.ArticleDetailView.as_view(), name='detail_view'),
    # # 创建类视图
    # path('create-view/', views.ArticleCreateView.as_view(), name='create_view'),

]
