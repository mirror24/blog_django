from django.contrib import admin

# Register your models here.

from .models import ArticlePost


admin.site.register(ArticlePost)


from .models import ArticleColumn


admin.site.register(ArticleColumn)
