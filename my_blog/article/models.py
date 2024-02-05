from django.db import models

# Create your models here.
# 导入内建的User模型
from django.contrib.auth.models import User
# timezone用于处理时间相关事务
from django.utils import timezone

from django.urls import reverse
# Django-taggit
from taggit.managers import TaggableManager

from PIL import Image


class ArticleColumn(models.Model):
    """
    栏目的 Model
    """
    # 栏目标题
    title = models.CharField(max_length=100, blank=True)
    # 创建时间
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


# 引入imagekit
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit


# 博客文章数据模型
class ArticlePost(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    column = models.ForeignKey(
        ArticleColumn,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='article'
    )

    # 文章标签
    tags = TaggableManager(blank=True)

    # 文章标题图
    # 手写的
    avatar = models.ImageField(
        upload_to='article/%Y%m%d/',
        blank=True
    )

    # 文章标题。
    # models.CharField为字符串字段，用于保存较短的字符串，比如标题

    title = models.CharField(max_length=100)

    # 文章正文。
    # 保存大量文本使用TextField
    body = models.TextField()

    # 文章创建时间。
    # DateTimeField 为一个日期字段
    # 参数default=timezone.now指定其在创建数据时默认写入当前时间
    created = models.DateTimeField(default=timezone.now)

    # 文章更新时间。
    # 参数auto_now=True指定每次数据更新时自动写入当前时间
    updated = models.DateTimeField(auto_now=True)

    # 统计文章浏览量
    # PositiveIntegerField是用于存储正整数的字段
    # default = 0 设定初始值从0开始
    total_views = models.PositiveIntegerField(default=0)

    # 新增点赞数统计
    likes = models.PositiveIntegerField(default=0)

    # 内部类class Meta用于给model定义元数据
    # 元数据：不是一个字段的任何数据
    class Meta:
        # ordering指定模型返回的数据的排列顺序
        # -created表明数据应该以倒序排序
        ordering = ('-created',)

    def __str__(self):
        # return self.title将文章标题返回
        return self.title

    # 获取文章地址
    def get_absolute_url(self):
        return reverse('article:article_detail', args=[self.id])

    # 保存时处理图片
    def save(self, *args, **kwargs):
        article = super(ArticlePost, self).save(*args, **kwargs)

        if self.avatar and not kwargs.get('update_fields'):
            image = Image.open(self.avatar)
            (x, y) = image.size
            new_x = 400
            new_y = int(new_x * (y / x))
            resized_image = image.resize((new_x, new_y), Image.ANTIALIAS)
            resized_image.save(self.avatar.path)

        return article

    # 有bug 未来的不行
    def was_created_recently(self):
        # 若文章是"最近"发表的，则返回 True
        diff = timezone.now() - self.created
        # if diff.days <= 0 and diff.seconds < 60:
        if diff.days == 0 and 0 <= diff.seconds < 60:
            return True
        else:
            return False
