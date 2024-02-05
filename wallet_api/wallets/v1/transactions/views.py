import django_filters
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_json_api.pagination import JsonApiPageNumberPagination

from wallets.models import Transaction
from wallets.v1.transactions.schemas import TRANSACTIONS_CREATE_BODY_SCHEMA
from wallets.v1.transactions.serializers import TransactionSerializer, TransactionQuerySerializer, \
    TransactionCreateSerializer

import logging

logger = logging.getLogger("transactions")
tx_logger = logging.getLogger("transactions_logger")


class TransactionFilter(django_filters.FilterSet):
    class Meta:
        model = Transaction
        fields = {
            'wallet_id': ['exact'],
            'is_inbound': ['exact'],
            'created_at': ['gte', 'lte']
        }

        
class TransactionListCreateView(APIView, JsonApiPageNumberPagination):
        
    @swagger_auto_schema(tags=['Transaction'],
                         query_serializer=TransactionQuerySerializer(),
                         responses={
                             status.HTTP_200_OK: TransactionSerializer(many=True),
                         }, )
    def get(self, request):
        """Get transactions list."""
        
        order_by = request.GET.get('order_by', "created_at")
        for order in order_by.split(","):        
            queryset = Transaction.objects.order_by(order)
        
        filtered_queryset = TransactionFilter(request.GET, queryset=queryset).qs
        
        transactions = self.paginate_queryset(filtered_queryset, request)
        serializer = TransactionSerializer(transactions, many=True)       
        return self.get_paginated_response(serializer.data)
    
    @swagger_auto_schema(tags=['Transaction'],
                         responses={
                             status.HTTP_201_CREATED: TransactionSerializer(),
                             status.HTTP_400_BAD_REQUEST: "Bad request", },
                         request_body=TRANSACTIONS_CREATE_BODY_SCHEMA,
                         )
    def post(self, request):
        """Create a new transaction."""
        
        serializer = TransactionCreateSerializer(data=request.data)
        if serializer.is_valid():
            transaction = serializer.create(validated_data=serializer.validated_data)
            tx_logger.info(f"Transaction {transaction.id} {transaction.txid} created successfully.")
            return Response(TransactionSerializer(transaction).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionDetailView(APIView):
    @swagger_auto_schema(tags=['Transaction'],
                         responses={
                             status.HTTP_200_OK: TransactionSerializer(),
                             status.HTTP_404_NOT_FOUND: "Not found",
                         }, )
    def get(self, request, transaction_id):
        """Get transaction details."""
        transaction = get_object_or_404(Transaction, pk=transaction_id)
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)
    