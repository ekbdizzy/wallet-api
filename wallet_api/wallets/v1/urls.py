from django.urls import path
from wallets.v1.wallet.views import WalletListCreateView, WalletDetailView
from wallets.v1.transactions.views import (
    TransactionListCreateView,
    TransactionDetailView,
)

app_name = "wallets_v1"

urlpatterns = [
    path("wallets/", WalletListCreateView.as_view(), name="wallets-list"),
    path("wallets/<int:wallet_id>", WalletDetailView.as_view(), name="wallets-detail"),
    path("transactions/", TransactionListCreateView.as_view(), name="transactions-list"),
    path("transactions/<int:transaction_id>", TransactionDetailView.as_view(), name="transactions-detail"),
]
