from django.urls import path, include


urlpatterns = [
    path('', include('src.apps.payment.api.v1.urls'))
    ]
