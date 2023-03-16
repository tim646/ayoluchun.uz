from django.contrib import admin
from .models import Blog, Category, BlogView

# Register your models here.
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'created_at', 'updated_at', 'views')
    list_filter = ('title', 'category')
    search_fields = ('title', 'category')


admin.site.register(Blog, BlogAdmin),
admin.site.register(Category),
admin.site.register(BlogView),