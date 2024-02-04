import django_filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_json_api.pagination import JsonApiPageNumberPagination


from wallets.models import Wallet
from wallets.v1.wallet.serializers import WalletSerializer


class WalletFilter(django_filters.FilterSet):
    class Meta:
        model = Wallet
        fields = {
            'label': ['icontains'],
        }


class WalletListCreateView(APIView, JsonApiPageNumberPagination):

    def get(self, request):
        queryset = Wallet.objects.all()
        filtered_queryset = WalletFilter(request.GET, queryset).qs
        
        wallets = self.paginate_queryset(filtered_queryset, request)
        serializer = WalletSerializer(wallets, many=True)
        return self.get_paginated_response(
            serializer.data,
        )


class WalletDetailView(APIView):
    def get(self, request, wallet_id):
        wallet = Wallet.objects.get(id=wallet_id)
        return Response(WalletSerializer(wallet).data)
