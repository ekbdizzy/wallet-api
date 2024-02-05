import django_filters
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework_json_api.pagination import JsonApiPageNumberPagination

from wallets.models import Wallet
from wallets.v1.wallet.schemas import WALLET_DETAIL_BODY_SCHEMA, WALLET_CREATE_BODY_SCHEMA
from wallets.v1.wallet.serializers import WalletSerializer, WalletQuerySerializer, WalletCreateSerializer

import logging

logger = logging.getLogger("wallets")
tx_logger = logging.getLogger("transactions_logger")


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
        logger.debug("WalletListCreateView")

        order_by = request.GET.get('order_by', "created_at")
        for order in order_by.split(","):
            queryset = Wallet.objects.order_by(order)

        filtered_queryset = WalletFilter(request.GET, queryset).qs

        wallets = self.paginate_queryset(filtered_queryset, request)
        serializer = WalletSerializer(wallets, many=True)
        return self.get_paginated_response(
            serializer.data,
        )
    
    @swagger_auto_schema(tags=['Wallet'],
                         responses={
                             status.HTTP_201_CREATED: WalletSerializer(),
                             status.HTTP_400_BAD_REQUEST: "Bad request", },
                         request_body=WALLET_CREATE_BODY_SCHEMA,
                         )
    def post(self, request):
        """Create wallet."""
        serializer = WalletSerializer(data=request.data)
        if serializer.is_valid():
            wallet = serializer.create(validated_data=serializer.validated_data)
            logger.info(f"Wallet {wallet.label} with ID {wallet.id} created")
            return Response(WalletSerializer(wallet).data, status=status.HTTP_201_CREATED)
        logger.warning(f"Wallet create error: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            

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

    @swagger_auto_schema(tags=['Wallet'],
                         request_body=WALLET_DETAIL_BODY_SCHEMA,
                         responses={
                             status.HTTP_200_OK: WalletSerializer(),
                             status.HTTP_404_NOT_FOUND: "Not found",
                             status.HTTP_400_BAD_REQUEST: "Bad request"
                         }, )
    def patch(self, request, wallet_id):
        """Update wallet label."""

        wallet = get_object_or_404(Wallet, pk=wallet_id)
        serializer = WalletCreateSerializer(
            instance=wallet,
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid(raise_exception=True):
            serializer.update(wallet, request.data)
        return Response(
            WalletSerializer(wallet).data
        )

    @swagger_auto_schema(tags=['Wallet'],
                         responses={
                             status.HTTP_204_NO_CONTENT: "No content",
                             status.HTTP_404_NOT_FOUND: "Not found",
                         }, )
    def delete(self, request, wallet_id):
        wallet = get_object_or_404(Wallet, pk=wallet_id)
        wallet.transactions.all().delete()
        tx_logger.info(f"Transactions for Wallet ID={wallet_id} deleted.")
        wallet.delete()
        logger.info(f"Wallet ID={wallet_id} deleted")
        return Response(status=status.HTTP_204_NO_CONTENT)