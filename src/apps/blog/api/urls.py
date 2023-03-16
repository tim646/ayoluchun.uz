from django.urls import path, include


urlpatterns = [
    path('v1/', include('src.apps.blog.api.v1.urls'))
]