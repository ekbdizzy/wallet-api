from decimal import Decimal

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from wallets.models import Wallet, Transaction
from wallets.v1.transactions.serializers import TransactionSerializer


class WalletAPITestCase(APITestCase):
    def setUp(self):
        self.wallet_1 = Wallet.objects.create(label="Label 1", balance=Decimal('30.00'))
        self.wallet_2 = Wallet.objects.create(label="Label 1", balance=Decimal('0.00'))
        
        self.transaction_1 = Transaction.objects.create(wallet=self.wallet_1, amount='50.00', is_inbound=True)
        self.transaction_1 = Transaction.objects.create(wallet=self.wallet_1, amount='20.00', is_inbound=False)

        self.url_list = reverse("wallets:v1:transactions-list")
        self.url_detail = reverse("wallets:v1:transactions-detail", 
                                  kwargs={"transaction_id": self.transaction_1.id})

    def test_transaction_list(self):
        # get
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(TransactionSerializer(Transaction.objects.all(), many=True).data, response.data["results"])

    def test_transaction_create(self):
        
        self.assertEqual(Transaction.objects.count(), 2)
        self.assertEqual(self.wallet_2.balance, Decimal('0.00'))
        
        body_1 = {
            "data": {
                "type": "TransactionListCreateView",
                "attributes": {
                    "wallet_id": self.wallet_2.id,
                    "amount": "45.22",
                    "is_inbound": True
                }
            }
        }
        
        # post
        response = self.client.post(self.url_list, data=body_1)
        self.wallet_2.refresh_from_db()
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.wallet_2.balance, Decimal('45.22'))
        self.assertEqual(response.data["amount"], "45.22")

        body_2 = {
            "data": {
                "type": "TransactionListCreateView",
                "attributes": {
                    "wallet_id": self.wallet_2.id,
                    "amount": "22.20",
                    "is_inbound": False
                }
            }
        }
        response = self.client.post(self.url_list, data=body_2)
        self.wallet_2.refresh_from_db()
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.wallet_2.balance, Decimal('23.02'))
        
        self.assertEqual(Transaction.objects.count(), 4)
        

        body_3 = {
            "data": {
                "type": "TransactionListCreateView",
                "attributes": {
                    "wallet_id": 124,  # Does not exist
                    "amount": "22.20",
                    "is_inbound": False
                }
            }
        }
        response = self.client.post(self.url_list, data=body_3)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_transaction_detail(self):
        # get
        response = self.client.get(self.url_detail)
        self.assertEqual(TransactionSerializer(self.transaction_1).data, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
