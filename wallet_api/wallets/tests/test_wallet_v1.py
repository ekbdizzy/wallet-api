from decimal import Decimal

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from wallets.models import Wallet
from wallets.v1.wallet.serializers import WalletSerializer


class WalletAPITestCase(APITestCase):
    def setUp(self):
        
        self.wallet_1 = Wallet.objects.create(label="Label 1", balance=Decimal('100.00'))
        self.wallet_2 = Wallet.objects.create(label="Label 2", balance=Decimal('50.00'))
        self.wallet_3 = Wallet.objects.create(label="Label 3", balance=Decimal('-10.00'))
        
        self.url_list = reverse("wallets:v1:wallets-list")
        self.url_detail = reverse("wallets:v1:wallets-detail", kwargs={"wallet_id": 1})
        
    def test_wallet_list(self):
        # get
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(WalletSerializer(Wallet.objects.all(), many=True).data, response.data["results"])
        
    def test_wallet_create(self):
        self.assertEqual(Wallet.objects.count(), 3)
        body = {
            "data": {
                "type": "WalletListCreateView",
                "attributes": {
                    "label": "New label"
                }
            }
        }
        
        # post
        response = self.client.post(self.url_list, data=body)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["label"], "New label")
        self.assertEqual(Wallet.objects.count(), 4)
        
    def test_wallet_detail(self):
        # get
        response = self.client.get(self.url_detail)
        self.assertEqual(WalletSerializer(self.wallet_1).data, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # patch
        body = {
            "data": {
                "type": "WalletDetailView",
                "id": 1,
                "attributes": {
                    "label": "New Label 1"
                }
            }
        }
        response = self.client.patch(self.url_detail, data=body)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['label'], "New Label 1")
        
        # delete
        self.assertTrue(Wallet.objects.filter(id=1).exists())
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Wallet.objects.filter(id=1).exists())
        