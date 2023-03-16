from django.urls import path, include


urlpatterns = [
    path('v1/', include('src.apps.comment.api.v1.urls'))
]