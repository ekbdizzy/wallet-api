from rest_framework import serializers

from wallets.models import Wallet


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = (
            "id",
            "label",
            "balance",
        )


class WalletQuerySerializer(serializers.Serializer):
    label__icontains = serializers.CharField(required=False)
    order_by = serializers.CharField(required=False)
    
    
class WalletCreateSerializer(serializers.Serializer):
    label = serializers.CharField(required=True, max_length=128)
    
    def update(self, instance, validated_data):
        instance.label = validated_data.get("label")
        instance.save()
        return instance
