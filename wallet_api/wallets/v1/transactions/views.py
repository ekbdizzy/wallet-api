from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_json_api.pagination import JsonApiPageNumberPagination

from wallets.models import Transaction
from wallets.v1.transactions.serializers import TransactionSerializer


class TransactionListCreateView(APIView, JsonApiPageNumberPagination):

    def get(self, request):
        transactions = Transaction.objects.all()
        transactions = self.paginate_queryset(transactions, request)
        serializer = TransactionSerializer(transactions, many=True)
        return self.get_paginated_response(serializer.data)


class TransactionDetailView(APIView):
    def get(self, request, transaction_id):
        transaction = Transaction.objects.get(id=transaction_id)
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)
