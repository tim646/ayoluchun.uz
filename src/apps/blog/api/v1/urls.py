from __future__ import annotations

from django.urls import path

from .views import BlogCreateView
from .views import BlogDeleteView
from .views import BlogDetailView
from .views import BlogListView
from .views import BlogUpdateView
from .views import CategoryCreateView
from .views import CategoryListView
from .views import BlogSearchView


urlpatterns = [
    path('blog/', BlogListView.as_view(), name='blog-list'),
    path('blog/<int:pk>/', BlogDetailView.as_view(), name='blog-detail'),
    path('blog/create/', BlogCreateView.as_view(), name='blog-create'),
    path('blog/<int:pk>/update/', BlogUpdateView.as_view(), name='blog-update'),
    path('blog/<int:pk>/delete/', BlogDeleteView.as_view(), name='blog-delete'),
    path('blog/search/<str:query>/', BlogSearchView.as_view(), name='blog-search'),
    # path('view/', BlogViewListView.as_view(), name='blog-view'),
    path('category/', CategoryListView.as_view(), name='category-list'),
    path('category/create/', CategoryCreateView.as_view(), name='category-create'),

]
