import django_filters
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_json_api.pagination import JsonApiPageNumberPagination

from wallets.models import Transaction
from wallets.v1.transactions.serializers import TransactionSerializer


class TransactionFilter(django_filters.FilterSet):
    class Meta:
        model = Transaction
        fields = {
            'wallet_id': ['exact'],
            'is_inbound': ['exact'],
            'created_at': ['exact', 'gte', 'lte']
        }
        
        
class TransactionListCreateView(APIView, JsonApiPageNumberPagination):
    
    filterset_class = TransactionFilter

    def get(self, request):
        
        order_by = request.GET.get('order_by', "created_at")
        for order in order_by.split(","):        
            queryset = Transaction.objects.order_by(order)
        
        filtered_queryset = TransactionFilter(request.GET, queryset=queryset).qs
        
        transactions = self.paginate_queryset(filtered_queryset, request)
        serializer = TransactionSerializer(transactions, many=True)
        return self.get_paginated_response(serializer.data)


class TransactionDetailView(APIView):
    def get(self, request, transaction_id):
        transaction = Transaction.objects.get(id=transaction_id)
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)
