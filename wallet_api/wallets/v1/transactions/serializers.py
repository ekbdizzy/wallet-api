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
