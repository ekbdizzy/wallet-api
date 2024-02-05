from decimal import Decimal

from django.db import transaction as _transaction

from rest_framework import serializers

from wallets.models import Transaction, Wallet
from wallets.v1.wallet.serializers import WalletSerializer

import logging

tx_logger = logging.getLogger("transactions_logger")


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
    
    
class TransactionCreateSerializer(serializers.Serializer):
    
    wallet_id = serializers.IntegerField(required=True)
    amount = serializers.CharField(required=False, max_length=18)
    is_inbound = serializers.BooleanField(required=True)
    
    def create(self, validated_data):
        try:
            wallet_id = validated_data["wallet_id"]
            wallet = Wallet.objects.get(id=wallet_id)
        
        except Wallet.DoesNotExist:
            tx_logger.error(f"Wallet with id {wallet_id} does not exist. Transaction failed.")
            raise serializers.ValidationError("Wallet with id {wallet_id} does not exist}")

        with _transaction.atomic():
            transaction = Transaction.objects.create(wallet=wallet, **validated_data)
            if transaction.is_inbound:
                wallet.balance += Decimal(transaction.amount)
            else:
                wallet.balance -= Decimal(transaction.amount)
            wallet.save()
            tx_logger.info(f"Transaction {transaction.id} created")
            tx_logger.info(f"Wallet {wallet.id} balance update: {'+' if transaction.is_inbound else '-'}{transaction.amount}")
            
        return transaction
                
            
    