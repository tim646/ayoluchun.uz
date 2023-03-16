from django.urls import path, include


urlpatterns = [
    path('v1/', include('src.apps.courses.api.v1.urls'))
]