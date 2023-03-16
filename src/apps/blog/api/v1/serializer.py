from __future__ import annotations

from rest_framework import serializers

from src.apps.blog.models import Blog, BlogView
from src.apps.blog.models import Category


class BlogSerializerGet(serializers.ModelSerializer):
    category_title = serializers.SerializerMethodField('get_category_title')
    def get_category_title(self, obj):
        return obj.category.title
    class Meta:
        model = Blog
        fields = (
            'id', 'author', 'position', 'title',
            'category', 'category_title',  'image', 'description', 'views'
        )


class BlogSerializerPost(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = (
            'id', 'author', 'position', 'title',
            'category', 'image', 'description'
        )

    def create(self, validated_data):
        return Blog.objects.create(**validated_data)


class BlogSerializerPut(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = (
            'id', 'author', 'position', 'title',
            'category', 'image', 'description'
        )

    def update(self, instance, validated_data):
        instance.author = validated_data.get('author', instance.author)
        instance.position = validated_data.get('position', instance.position)
        instance.title = validated_data.get('title', instance.title)
        instance.category = validated_data.get('category', instance.category)
        instance.image = validated_data.get('image', instance.image)

        instance.save()
        return instance


class BlogSerializerDelete(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = (
            'id', 'author', 'position', 'title',
            'category', 'image', 'description'
        )

    def delete(self, instance):
        instance.delete()
        return instance

class BlogViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogView
        fields = (
            'id', 'blog_view', 'user',
        )

class CategorySerializerGet(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title', 'slug')




class CategorySerializerPost(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title', 'slug')

    def create(self, validated_data):
        return Category.objects.create(**validated_data)
