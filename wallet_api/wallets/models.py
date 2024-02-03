import uuid

from django.db import models

from decimal import Decimal


class Wallet(models.Model):
    """Wallet with a label, balance and timestamps."""
    label = models.CharField(max_length=128, db_index=True)
    balance = models.DecimalField(max_digits=18,
                                  decimal_places=2,
                                  default=Decimal('0.00'),
                                  editable=False,
                                  db_index=True,
                                  )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'wallets'
        verbose_name = 'Wallet'
        verbose_name_plural = 'Wallets'

    def __str__(self):
        return f'{self.label}: {self.balance}'


class Transaction(models.Model):
    """Represents a transaction of a wallet with a unique transaction ID,
    associated wallet, amount, type (inbound or outbound) and timestamps."""

    @staticmethod
    def generate_uuid() -> str:
        return str(uuid.uuid4())

    txid = models.CharField(unique=True,
                            default=generate_uuid,
                            max_length=36,
                            editable=False,
                            db_index=True,
                            verbose_name='Transaction ID',
                            )
    wallet = models.ForeignKey(Wallet, on_delete=models.PROTECT, related_name='transactions')
    amount = models.DecimalField(max_digits=18, decimal_places=2)
    is_inbound = models.BooleanField(verbose_name='Is it inbound or not')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'transactions'
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
