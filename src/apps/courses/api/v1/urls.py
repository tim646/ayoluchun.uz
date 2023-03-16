from django.urls import path
from src.apps.courses.api.v1.views import CourseListView, CourseDetailView, CourseCreateView, CategoryListView, \
    CourseLessonsView, LessonVideoListView, VideoSingleView, CourseListByCategoryView

urlpatterns = [
    path('list/', CourseListView.as_view(), name='course-list'),
    path('list/category/<int:id>/', CourseListByCategoryView.as_view(), name='course-list-by-category'),
    path('<int:id>/', CourseDetailView.as_view(), name='course-detail'),
    path('create/', CourseCreateView.as_view(), name='course-create'),
    # path('<str:slug>/update/', CourceUpdateView.as_view(), name='course-update'),
    # path('<str:slug>/delete/', CourceDeleteView.as_view(), name='course-delete'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    # path('category/create/', CategoryCreateView.as_view(), name='category-create'),
    # path('category/<str:pk>/update/', CategoryUpdateView.as_view(), name='category-update'),
    # path('category/<str:pk>/delete/', CategoryDeleteView.as_view(), name='category-delete'),
    path('<int:id>/lessons/', CourseLessonsView.as_view(), name='lesson-list'),
    # path('lesson/<str:slug>/', CourseLessonsView.as_view(), name='lesson-detail'),
    # path('lesson/create/', LessonCreateView.as_view(), name='lesson-create'),
    # path('lesson/<str:slug>/update/', LessonUpdateView.as_view(), name='lesson-update'),
    # path('lesson/<str:slug>/delete/', LessonDeleteView.as_view(), name='lesson-delete'),
    path('lesson/<int:id>/', LessonVideoListView.as_view(), name='video-list'),
    path('<int:lesson_id>/<int:video_id>/', VideoSingleView.as_view(), name='video-detail'),
    # path('lesson/video/create/', VideoCreateView.as_view(), name='video-create'),
    # path('lesson/video/<str:slug>/update/', VideoUpdateView.as_view(), name='video-update'),
    # path('lesson/video/<str:slug>/delete/', VideoDeleteView.as_view(), name='video-delete'),
]