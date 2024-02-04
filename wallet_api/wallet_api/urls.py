from django.contrib import admin
from django.urls import path, include

from wallets.views import get_status_view

from wallet_api.swagger import swagger_urlpatterns

urlpatterns = [
    path("admin/", admin.site.urls),
    path("status/", get_status_view, name="status"),
    path("api/", include("wallets.urls", namespace="wallets")),
]

urlpatterns += swagger_urlpatterns
