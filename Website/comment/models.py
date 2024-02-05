from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from mptt.models import MPTTModel, TreeForeignKey
from article.models import ArticlePost


class Comment(MPTTModel):
    article = models.ForeignKey(
        ArticlePost,
        on_delete=models.CASCADE,
        related_name='comments',
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
    )

    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
    )

    reply_to = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='repliers',
    )

    body = RichTextField()
    created = models.DateTimeField(auto_now_add=True)

    class MPTTMeta:
        order_insertion_by = ['created']

    def __str__(self):
        return self.body[:20]
