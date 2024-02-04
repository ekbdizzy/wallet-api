import django_filters
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework_json_api.pagination import JsonApiPageNumberPagination

from wallets.models import Wallet
from wallets.v1.wallet.serializers import WalletSerializer, WalletQuerySerializer


class WalletFilter(django_filters.FilterSet):
    class Meta:
        model = Wallet
        fields = {
            'label': ['icontains'],
        }


class WalletListCreateView(APIView, JsonApiPageNumberPagination):

    @swagger_auto_schema(tags=['Wallet'],
                         query_serializer=WalletQuerySerializer(),
                         responses={
                             "200": WalletSerializer(many=True),
                         }, )
    def get(self, request):
        """ Get wallets list."""
        order_by = request.GET.get('order_by', "created_at")
        for order in order_by.split(","):
            queryset = Wallet.objects.order_by(order)

        filtered_queryset = WalletFilter(request.GET, queryset).qs

        wallets = self.paginate_queryset(filtered_queryset, request)
        serializer = WalletSerializer(wallets, many=True)
        return self.get_paginated_response(
            serializer.data,
        )


class WalletDetailView(APIView):

    @swagger_auto_schema(tags=['Wallet'],
                         responses={
                             status.HTTP_200_OK: WalletSerializer(),
                             status.HTTP_404_NOT_FOUND: "Not found",
                         }, )
    def get(self, request, wallet_id):
        """Get wallet details."""
        wallet = get_object_or_404(Wallet, pk=wallet_id)
        return Response(WalletSerializer(wallet).data)
