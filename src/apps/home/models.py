from __future__ import annotations

from django.db import models
from src.apps.accounts.models import Purchased_course

from helpers.models import BaseModel


class Contact(BaseModel):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=100)
    message = models.TextField()

    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'

    def __str__(self):
        return self.name


class Notification(BaseModel):
    user = models.ForeignKey(
        'accounts.Account', on_delete=models.CASCADE, related_name='notifications',
    )
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-id']

    def __str__(self):
        return self.title


class Certificate(BaseModel):
    user = models.ForeignKey(
        'accounts.Account', on_delete=models.CASCADE, related_name='certificates',
    )
    course = models.ForeignKey(
        'courses.Course', on_delete=models.CASCADE, related_name='certificates',
    )
    # user = models.ForeignKey(Purchased_course, on_delete=models.CASCADE, verbose_name='Foydalanuvchi')
    certificate_url = models.CharField(max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):

        self.certificate_url = f'/home/nurmuhammad/uic/ayoluchun.uz/static/certicats/{self.user}-{self.course.title}.jpg'
        super().save(*args, **kwargs)


    class Meta:
        verbose_name = 'Certificate'
        verbose_name_plural = 'Certificates'

    def __str__(self):
        return self.user.name
