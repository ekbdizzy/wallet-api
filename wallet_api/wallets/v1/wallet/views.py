from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_json_api.pagination import JsonApiPageNumberPagination


from wallets.models import Wallet
from wallets.v1.wallet.serializers import WalletSerializer


class WalletListCreateView(APIView, JsonApiPageNumberPagination):

    def get(self, request):
        wallets = Wallet.objects.all()
        wallets = self.paginate_queryset(wallets, request)
        serializer = WalletSerializer(wallets, many=True)
        return self.get_paginated_response(
            serializer.data,
        )


class WalletDetailView(APIView):
    def get(self, request, wallet_id):
        wallet = Wallet.objects.get(id=wallet_id)
        return Response(WalletSerializer(wallet).data)
