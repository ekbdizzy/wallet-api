from rest_framework import serializers

from wallets.models import Transaction
from wallets.v1.wallet.serializers import WalletSerializer


class TransactionSerializer(serializers.ModelSerializer):
    wallet = WalletSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = (
            "id",
            "txid",
            "wallet",
            "amount",
            "is_inbound",
            "created_at",
        )


class TransactionQuerySerializer(serializers.Serializer):
    
    wallet_id = serializers.IntegerField(required=False)
    is_inbound = serializers.BooleanField(required=False)
    created_at__gte = serializers.CharField(required=False)
    created_at__lte = serializers.CharField(required=False)
    order_by = serializers.CharField(required=False)
    