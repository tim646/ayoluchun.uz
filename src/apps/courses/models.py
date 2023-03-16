from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField

from helpers.models import BaseModel
from .choices import STATUS_CHOICES
from mutagen.mp4 import MP4, MP4StreamInfoError

from helpers.utils import get_timer


class CourseCategory(BaseModel):
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.name


class Course(BaseModel):
    title = models.CharField(max_length=80)
    image = models.ImageField(upload_to='media/course_images')
    description = RichTextField()
    demo_video = models.FileField()
    author = models.CharField('Author', max_length=150)
    price = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(CourseCategory, on_delete=models.SET_NULL, null=True)
    language = models.CharField(max_length=60)
    is_discount = models.BooleanField('Chegirma', default=False)
    discount_price = models.DecimalField('Chegirmadagi narxi', max_digits=12, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title[:20])
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'


class CourseLesson(BaseModel):
    title = models.CharField(max_length=70)
    description = RichTextField()
    order = models.PositiveIntegerField('Tartib nomeri', default=1)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lesson_status = models.CharField(max_length=40,
                                     choices=STATUS_CHOICES,
                                     default="Ko'rilmagan")
    slug = models.SlugField(unique=True, blank=True)
    video_count = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title[:20])
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class CourseVideo(BaseModel):
    course = models.ForeignKey('courses.CourseLesson', on_delete=models.CASCADE)
    title = models.CharField(max_length=80)
    video = models.FileField()
    slug = models.SlugField(unique=True, blank=True)
    length = models.DecimalField(default=0, max_digits=100, decimal_places=2, blank=True, null=True,
                                 help_text='Video uzunligi ozi yozadi yozmasangiz  bo\'ladi')
    is_viewed = models.BooleanField(default=False)
    useful_files = models.FileField(blank=True, null=True, upload_to='media/useful_materials')
    useful_links = models.URLField(blank=True, null=True)
    useful_images = models.ImageField(upload_to='media/useful_materials', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title[:4])
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_video_length(self):
        try:
            video = MP4(self.video)
            return video.info.length

        except MP4StreamInfoError:
            return 0.0

    def get_video_length_time(self):
        return get_timer(self.length)

    def get_video(self):
        return self.video.path


    def save(self, *args, **kwargs):
        self.length = self.get_video_length()
        les_obj = CourseLesson.objects.get(id=self.course.id)
        les_obj.video_count+=1
        les_obj.save()


        return super().save(*args, **kwargs)





