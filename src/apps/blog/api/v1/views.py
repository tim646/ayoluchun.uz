from __future__ import annotations

from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .serializer import BlogSerializerDelete
from .serializer import BlogSerializerGet
from .serializer import BlogSerializerPost
from .serializer import BlogSerializerPut
from .serializer import CategorySerializerGet
from .serializer import CategorySerializerPost
from src.apps.blog.models import Blog
from src.apps.blog.models import BlogView
from src.apps.blog.models import Category


class BlogListView(generics.ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializerGet

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class BlogCreateView(generics.CreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializerPost
    permission_classes = (IsAuthenticated, IsAdminUser)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class BlogDetailView(generics.RetrieveAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializerGet


    def get_queryset(self):
        # print(self.request.META.get('HTTP_USER_AGENT', ''))
        queryset = super().get_queryset()
        blog = get_object_or_404(queryset, id=self.kwargs["pk"])
        print(self.kwargs)
        if self.request.user.is_authenticated:
            blog_view, created = BlogView.objects.update_or_create(
                blog_view=blog,
                user=self.request.user,
            )
            if created:
                blog.views += 1
                blog.save()
        elif self.request.META.get('HTTP_USER_AGENT', ''):
            device_id = self.request.META.get('HTTP_USER_AGENT', '')
            print(device_id)
            blog_view, created = BlogView.objects.update_or_create(
                blog_view=blog,
                device_id=device_id,
            )
            if created:
                blog.views += 1
                blog.save()

        return queryset

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class BlogUpdateView(generics.UpdateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializerPut
    permission_classes = (IsAuthenticated, IsAdminUser)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class BlogDeleteView(generics.DestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializerDelete
    permission_classes = (IsAuthenticated, IsAdminUser)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class BlogSearchView(generics.ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializerGet

    def get_queryset(self):
        query = self.kwargs.get('query')
        queryset = Blog.objects.filter(title__icontains=query) | Blog.objects.filter(description__icontains=query)
        return queryset
class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializerGet
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class CategoryCreateView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializerPost
    permission_classes = (IsAuthenticated, IsAdminUser)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


