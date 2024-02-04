from django.contrib import admin

from .models import Transaction, Wallet


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = (
        "label",
        "balance",
    )
    search_fields = ("label",)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "txid",
        "wallet",
        "amount",
        "is_inbound",
    )
    list_filter = ("is_inbound",)
    search_fields = (
        "wallet",
        "txid",
        "amount",
    )
