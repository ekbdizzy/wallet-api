from django.urls import path, include

app_name = "wallets"


urlpatterns = [
    path("v1/", include("wallets.v1.urls", namespace="v1")),
]
