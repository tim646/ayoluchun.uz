from __future__ import annotations

from rest_framework import serializers

from src.apps.home.models import Contact
from src.apps.home.models import Notification
from src.apps.accounts.models import Purchased_course
from src.apps.home.models import Certificate
from src.apps.courses.models import CourseVideo
from ...certificaty import certificaty


class ContactSerializerGet(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('id', 'name', 'email',  'message', 'created_at')


class ContactSerializerPost(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('id', 'name', 'email', 'message', 'created_at')

    def create(self, validated_data):
        return Contact.objects.create(**validated_data)


class NotificationSerializerGet(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('id', 'user', 'title', 'message', 'is_read', 'created_at')


class NotificationSerializerPost(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('id', 'user', 'title', 'message', 'is_read', 'created_at')

    def create(self, validated_data):
        return Notification.objects.create(**validated_data)
class CertificateSerializerGet(serializers.ModelSerializer):
    # purchase_course = serializers.
    class Meta:
        model = Certificate
        fields = ('id', 'user', 'course', 'certificate_url')
        read_only_fields =("certificate_url",)


    def create(self, validated_data):
        return Certificate.objects.create(**validated_data)





class PurchasCourseUpdate(serializers.ModelSerializer):
    video_plus = serializers.IntegerField(required=False)
    class Meta:
        model = Purchased_course
        exclude = ('id', 'user','course','lessons_video_count',"viewed_video_count","is_finished")
        read_only_fields = ('id', 'user','course','lessons_video_count',"viewed_video_count","video_plus",)



