from django.urls import path, include


urlpatterns = [
    path('v1/', include('src.apps.accounts.api.v1.urls'))
]