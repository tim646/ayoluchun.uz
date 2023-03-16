from __future__ import annotations

from django.contrib import admin

from .models import Account
from .models import UserProfile
from .models import Purchased_course
from .models import Speciality
from .models import Country
from .models import Region


class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'phone_number', 'email', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('username', 'phone_number', 'email')


class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_filter = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', )


class RegionAdmin(admin.ModelAdmin):
    list_display = ('title', 'country_id')
    list_filter = ('title', 'country_id')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'country_id')


class SpecialityAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_filter = ('title', )
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', )


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'speciality', 'country', 'region', 'birth_date')
    list_filter = ('user', 'speciality', 'country', 'region')
    search_fields = ('user', 'speciality', 'country', 'region')


class Purchased_courseAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'course', 'is_finished')
    list_filter = ('user_id', 'course', 'is_finished')
    search_fields = ('user_id', 'course',)


admin.site.register(Account, AccountAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Speciality, SpecialityAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(Purchased_course, Purchased_courseAdmin)