from django.contrib import admin

# Register your models here.
from .models import Certificate
from .models import Contact
from .models import Notification

class CertificateAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'created_at', )
    list_filter = ('user', 'course', 'created_at', )
    search_fields = ('user', 'course', )


admin.site.register(Certificate, CertificateAdmin)
admin.site.register(Contact)
admin.site.register(Notification)
