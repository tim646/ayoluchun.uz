from django.db import models
from helpers.models import BaseModel
from ckeditor.fields import RichTextField


class Category(BaseModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['title']


class Blog(BaseModel):
    author = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blog/', null=True, blank=True)
    description = RichTextField()
    views = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Blog'
        verbose_name_plural = 'Blogs'


class BlogView(BaseModel):
    blog_view = models.ForeignKey(
        'blog.Blog',
        verbose_name=("BLogView"),
        on_delete=models.CASCADE,
        related_name="blog_views",
    )
    user = models.ForeignKey(
        "accounts.Account",
        verbose_name=("Foydalanuvchi"),
        on_delete=models.CASCADE,
        related_name="user_views",
        null=True,
        blank=True,
    )
    device_id = models.CharField(
        verbose_name=("Qurilmalar Identifikatori"),
        max_length=255,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "BlogView"
        verbose_name_plural = "BlogViews"