from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import generics

from .serializer import CourseListSerializer, CourseSingleSerializer, CourseCreateSerializer, CourseLessonsSerializer, \
    LessonVideoListSerializer, VideoSingleSerializer, CategorySerializer

from src.apps.courses.models import Course, CourseCategory, CourseVideo, CourseLesson
from src.apps.accounts.models import Purchased_course


class CourseListView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseListSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = CourseListSerializer(queryset, many=True)
        return Response(serializer.data)


class CourseListByCategoryView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        category_id = self.kwargs['id']
        if category_id:
            queryset = Course.objects.filter(category__id=category_id)
        else:
            queryset = Course.objects.none()
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = CourseListSerializer(queryset, many=True)
        return Response(serializer.data)


class CourseDetailView(generics.UpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSingleSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = CourseSingleSerializer(queryset, many=True)
        return Response(serializer.data)


class CourseCreateView(generics.CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseCreateSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CourseLessonsView(generics.ListAPIView):
    serializer_class = CourseLessonsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        course_id = self.kwargs['id']
        if course_id:
            queryset = CourseLesson.objects.filter(course__id=course_id)
        else:
            queryset = CourseLesson.objects.none()
        return queryset

    def get(self, request, *args, **kwargs):

        queryset = self.get_queryset()
        serializer = CourseLessonsSerializer(queryset, many=True)
        return Response(serializer.data)


class LessonVideoListView(generics.ListAPIView):
    queryset = CourseVideo.objects.all()
    serializer_class = LessonVideoListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        lesson_id = self.kwargs['id']

        if lesson_id:
            queryset = CourseVideo.objects.filter(lesson__id=lesson_id)
        else:
            queryset = CourseVideo.objects.none()
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = LessonVideoListSerializer(queryset, many=True)
        return Response(serializer.data)


class VideoSingleView(generics.RetrieveAPIView):
    queryset = CourseVideo.objects.all()

    serializer_class = VideoSingleSerializer
    permission_classes = [IsAuthenticated]

    lookup_field = 'lesson_id'

    def get_queryset(self):

        lesson_id = self.kwargs['lesson_id']

        # print(self.kwargs)
        video_id = self.kwargs['video_id']
        if lesson_id and video_id:

            queryset = CourseVideo.objects.get(course_id=lesson_id, id=video_id)
            # print(queryset.course.course.id)
            # print(Purchased_course.objects.filter(user=self.request.user).values_list('course_id', flat=True))
            if queryset.course.course.id in Purchased_course.objects.filter(user=self.request.user).values_list(
                    'course_id', flat=True):
                return queryset
            #     queryset = CourseVideo.objects.filter(course_id=lesson_id, id=video_id)

        return CourseVideo.objects.none()

    def get(self, request, *args, **kwargs):
        if queryset := self.get_queryset():
            serializer = VideoSingleSerializer(queryset)
            return Response(serializer.data)
        return Response("You are not buy this course")


class CategoryListView(generics.ListAPIView):
    queryset = CourseCategory.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)
