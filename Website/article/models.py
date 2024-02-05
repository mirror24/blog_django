from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from PIL import Image
from taggit.managers import TaggableManager


class ArticleColumn(models.Model):
    title = models.CharField(max_length=100, blank=True)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class ArticlePost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='article/%Y%m%d/', blank=True)
    column = models.ForeignKey(
        ArticleColumn,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='article'
    )

    tags = TaggableManager(blank=True)

    title = models.CharField(max_length=100)

    body = models.TextField()

    total_views = models.PositiveIntegerField(default=0)

    likes = models.PositiveIntegerField(default=0)

    created = models.DateTimeField(default=timezone.now)

    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article:article_detail', args=[self.id])

    def save(self, *args, **kwargs):
        article = super(ArticlePost, self).save(*args, **kwargs)

        if self.avatar and not kwargs.get('update_fields'):
            image = Image.open(self.avatar)
            (x, y) = image.size
            new_x = 400
            new_y = int(new_x * (y / x))
            resized_image = image.resize((new_x, new_y), Image.ANTIALTAS)
            resized_image.save(self.avatar.path)
        return article

    def was_created_recently(self):
        diff = timezone.now - self.created

        if diff.days == 0 and diff.senconds >= diff.seconds < 60:
            return True
        else:
            return False
