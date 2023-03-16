from __future__ import annotations

from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from src.apps.accounts.models import Purchased_course
from .serializer import ContactSerializerGet, PurchasCourseUpdate
from .serializer import ContactSerializerPost
from .serializer import NotificationSerializerGet
from .serializer import NotificationSerializerPost
from .serializer import CertificateSerializerGet

from src.apps.home.models import Contact
from src.apps.home.models import Notification
from src.apps.home.models import Certificate
from ...certificaty import certificaty


class ContactListView(generics.ListAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializerGet
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ContactCreateView(generics.CreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializerPost
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class NotificationListView(generics.ListAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializerGet
    permission_classes = (IsAuthenticated,)

    def clean(self):
        if self.request.user.is_authenticated:
            Notification.objects.filter(user=self.request.user).update(is_read=False)


class NotificationCreateView(generics.CreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializerPost
    permission_classes = (IsAuthenticated, IsAdminUser)

    def post(self, request, *args, **kwargs):
        certificaty(name=f'{self.request.user}', course=f'{self.queryset.get(id=self.lookup_field)}')
        return self.create(request, *args, **kwargs)


class CertificateCreate(generics.CreateAPIView):
    queryset = Purchased_course.objects.all()
    serializer_class = CertificateSerializerGet
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        user = request.user
        course = request.data.get('course')
        # print(request.data)   
        qs = self.queryset.get(user=user, course=course)
        if qs.lessons_video_count == qs.viewed_video_count:
            if len(Certificate.objects.filter(user_id=user.id, course_id=course)) == 0:
                obj = Certificate.objects.create(user_id=user.id, course_id=course)
                obj.save()
                # print(user, qs.course)
                certificaty(str(user), str(qs.course))
                serizalizer = self.get_serializer(obj).data
                return Response(serizalizer)
            return Response({"message": "Sertifikat mavjud"})
        return Response({'Error': "Kurslar to'liq ko'rilmagan!"})


class CertificateListView(generics.RetrieveAPIView):
    serializer_class = CertificateSerializerGet
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        user = request.user
        certificate = Certificate.objects.all()
        print(certificate)
        try:
            certificate = Certificate.objects.get(user_id=user, course_id=request.GET.get('course_id'))
            serializer = self.get_serializer(certificate).data
            return Response(serializer)
        except Exception as e:
            return Response({'Error': f'{e}'})


class CertificateListView(generics.ListAPIView):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializerGet

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class PurchaseUpdate(generics.UpdateAPIView):
    queryset = Purchased_course.objects.all()
    serializer_class = PurchasCourseUpdate

    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        print()
        instance.viewed_video_count += 1
        instance.save()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response({"message": "failed", "details": serializer.errors})
        serializer.save()
        return Response({"message": "updated successfully"})
