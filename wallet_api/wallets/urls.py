from django.urls import path, include
from .views import get_status_view

app_name = "wallets"


urlpatterns = [
    path("status/", get_status_view, name="status"),
    path("v1/", include("wallets.v1.urls", namespace="v1")),
]
