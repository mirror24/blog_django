from django.urls import path
from . import views

app_name = 'article'
urlpatterns = [
    path(
        'article-lit/',
        views.article_list,
        name='article_list',
    ),
    path(
        'article-detail/<int:id>/',
        views.article_detail,
        name='article_detail',
    ),
    path(
        'article-create/',
        views.article_create,
        name='article_create',
    ),
    path(
        'article-delete/<int:id>/',
        views.article_delete,
        name='article_delete',
    ),
    path(
        'article-safe-delete/<int:id>/',
        views.article_safe_delete,
        name='article_safe_delete',
    ),
    path(
        'article-update/<int:id>/',
        views.article_update,
        name='article_update',
    ),
    path(
        'increase-likes/<int:id>/',
        views.IncreaseLikeView.as_view(),
        name='increase_likes',
    ),

    path(
        'list-view/',
        views.ArticleListView.as_view(),
        name='list_view',
    ),
    path(
        'detail-view/<int:pk>/',
        views.ArticleDetailView.as_view(),
        name='detail_view',
    ),
    path(
        'create-view/',
        views.ArticleCreateView.as_view(),
        name='create_view',
    ),
]
