from __future__ import annotations

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.hashers import make_password
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import Sum
from django.db.models.signals import pre_save, post_save
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework_simplejwt.tokens import RefreshToken
from src.apps.courses.models import Course, CourseLesson

from .choosen import GENDER

from helpers.models import BaseModel


class AccountManager(BaseUserManager):
    def create_user(self, name, surname, phone_number, password=None, **extra_fields):
        user = self.model(
            phone_number=phone_number,
            name=name,
            surname=surname
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, surname, phone_number, password=None, **extra_fields):
        user = self.model(phone_number=phone_number, name=name,
                          surname=surname, password=make_password(password))
        user.is_superuser = True
        user.is_staff = True
        user.is_sponsor = True
        user.is_active = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser, PermissionsMixin, BaseModel):
    name = models.CharField(
        max_length=50, blank=True,
        null=True, verbose_name='Name',
    )
    surname = models.CharField(
        max_length=50, blank=True, null=True, verbose_name='Surname',
    )
    patronymic = models.CharField(
        max_length=50, blank=True, null=True, verbose_name='Patronymic',
    )
    username = models.CharField(
        max_length=255, blank=True, null=True, unique=True, verbose_name='Phone',
    )
    phone_number = PhoneNumberField(region='UZ', unique=True, verbose_name='Phone number')
    email = models.EmailField(
        max_length=255, blank=True, null=True, verbose_name='Email',
    )
    email_is_verified = models.BooleanField(
        default=False, verbose_name='Email is verified',
    )
    is_superuser = models.BooleanField(default=False, verbose_name='Superuser')
    is_staff = models.BooleanField(default=False, verbose_name='Admin')
    is_active = models.BooleanField(default=True)
    date_login = models.DateTimeField(auto_now=True, verbose_name='Date login')
    date_created = models.DateTimeField(
        auto_now_add=True, verbose_name='Date created',
    )

    objects = AccountManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['name', 'surname']

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'

    def __str__(self):
        return self.name

    @property
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return data


class Purchased_course(BaseModel):
    user = models.ForeignKey('accounts.Account', on_delete=models.CASCADE, verbose_name='User')
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, verbose_name='Kurs')
    lessons_video_count = models.PositiveIntegerField(default=0)
    viewed_video_count = models.PositiveIntegerField(default=0)
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return f'Course: {self.course}'

    class Meta:
        verbose_name = 'Purchase course'
        verbose_name_plural = 'Purchased courses'


def purchase_course_post_save(instance, sender, *args, **kwargs):
    if instance is not None:
        obj =  CourseLesson.objects.filter(course__id = instance.course.id).aggregate(Sum('video_count'))
        instance.lessons_video_count = obj.get('video_count__sum')


pre_save.connect(purchase_course_post_save, sender=Purchased_course)


class Speciality(BaseModel):
    title = models.CharField(max_length=255, verbose_name='Title')
    slug = models.SlugField(max_length=255, unique=True, verbose_name='Slug')

    class Meta:
        verbose_name = 'Speciality'
        verbose_name_plural = 'Specialities'

    def __str__(self):
        return self.title


class Country(BaseModel):
    title = models.CharField(max_length=255, verbose_name='Title')
    slug = models.SlugField(max_length=255, unique=True, verbose_name='Slug')

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'

    def __str__(self):
        return self.title


class Region(BaseModel):
    """Viloyatlar uchun model"""
    title = models.CharField(max_length=255, verbose_name='Title')
    country_id = models.ForeignKey(Country, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255, unique=True, verbose_name='Slug')

    class Meta:
        verbose_name = 'Region'
        verbose_name_plural = 'Regions'

    def __str__(self):
        return self.title


class UserProfile(BaseModel):
    user = models.OneToOneField(
        Account, on_delete=models.CASCADE, related_name='profile', verbose_name='User',
    )
    bio = models.TextField(max_length=500, blank=True, verbose_name='Bio')
    image = models.ImageField(
        upload_to='profile/',
        null=True, blank=True, verbose_name='Image',
    )
    gender = models.CharField(
        max_length=211, choices=GENDER, blank=True, verbose_name='Gender',
    )
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Country',
    )
    region = models.ForeignKey(
        Region, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Region',
    )
    zip_code = models.CharField(
        max_length=30, blank=True, verbose_name='Zip code',
    )
    birth_date = models.DateField(
        null=True, blank=True, verbose_name='Birth date',
    )
    workplace = models.CharField(
        max_length=255, blank=True, verbose_name='Workplace',
    )
    speciality = models.ForeignKey(
        Speciality, on_delete=models.CASCADE, null=True, blank=True,
        verbose_name='Speciality',
    )
    imkon_profile = models.CharField(
        max_length=255,
        validators=[RegexValidator(regex=r'https?://(?:www\.)?imkon\.uz/(?P<path>[a-zA-Z0-9/_.-]+)/?$')], blank=True,
        verbose_name='Imkon profile',
    )
    facebook_profile = models.CharField(
        max_length=255, validators=[RegexValidator(regex=r'https?://(www\.)?facebook\.com/[A-Za-z0-9_.-]+/?$')],
        blank=True,
        verbose_name='Facebook profile',
    )
    telegram_profile = models.CharField(
        max_length=255, validators=[RegexValidator(regex=r'https:\/\/t\.me\/[a-zA-Z0-9_]+')], blank=True,
        verbose_name='Telegram profile',
    )
    linkden_profile = models.CharField(
        max_length=255, validators=[RegexValidator(regex=r'https:\/\/www\.linkedin\.com\/in\/[a-zA-Z0-9-]+\/?$')],
        blank=True,
        verbose_name='Linkden profile',
    )

    class Meta:
        verbose_name = 'User profile'
        verbose_name_plural = 'User profiles'

    def __str__(self):
        return self.user.name
