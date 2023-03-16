from django.db import models
# from unidecode import unidecode
#
#
# def generate_unique_slug(klass, field):
#     origin_slug = defaultfilters.slugify(unidecode((field)))  # noqa
#     unique_slug = origin_slug
#     numb = 1
#     while klass.objects.filter(slug=unique_slug).exists():
#         unique_slug = "%s-%d" % (origin_slug, numb)
#         numb += 1
#     return unique_slug


class BaseModel(models.Model):
    created_at = models.DateTimeField("Yaratilgan vaqti", auto_now_add=True)
    updated_at = models.DateTimeField("O`zgartirilgan vaqti", auto_now=True)

    class Meta:
        abstract = True

    # def save(self, *args, **kwargs):
    #     if hasattr(self, "slug") and hasattr(self, "title"):
    #         if not self.slug:
    #             self.slug = generate_unique_slug(self.__class__, self.title)
    #
    #     if hasattr(self, "slug") and hasattr(self, "name"):
    #         if not self.slug:
    #             self.slug = generate_unique_slug(self.__class__, self.name)
    #     super().save(*args, **kwargs)
