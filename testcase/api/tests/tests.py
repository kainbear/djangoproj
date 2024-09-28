from rest_framework.test import APITestCase
from rest_framework import status
from api.models import Wallet, Transaction
import uuid

class WalletTests(APITestCase):

    def setUp(self):
        self.wallet_data = {
            "current_balance": 100.00
        }
        self.wallet_url = "/wallets/"
        self.wallet = Wallet.objects.create(**self.wallet_data)

    def test_create_wallet(self):
        response = self.client.post(self.wallet_url + "create", self.wallet_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Wallet.objects.count(), 2)

    def test_get_wallets(self):
        response = self.client.get(self.wallet_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_wallet(self):
        response = self.client.get(f"{self.wallet_url}{self.wallet.WALLET_UUID}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['current_balance'], str(self.wallet.current_balance))

    def test_update_wallet(self):
        response = self.client.put(f"{self.wallet_url}{self.wallet.WALLET_UUID}/", {"current_balance": 200.00}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.current_balance, 200.00)

    def test_delete_wallet(self):
        response = self.client.delete(f"{self.wallet_url}{self.wallet.WALLET_UUID}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Wallet.objects.count(), 0)

class TransactionTests(APITestCase):

    def setUp(self):
        self.wallet = Wallet.objects.create(current_balance=100.00)
        self.transaction_data = {
            "wallet": self.wallet,
            "operationType": "DEPOSIT",
            "amount": 50.00,
            "running_balance": self.wallet.current_balance + 50.00
        }
        self.transaction_url = f"/wallets/{self.wallet.WALLET_UUID}/operation"
        self.transaction = Transaction.objects.create(wallet=self.wallet, operationType="DEPOSIT", amount=50.00, running_balance=self.wallet.current_balance + 50.00)

    def test_create_transaction(self):
        response = self.client.post(self.transaction_url, self.transaction_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transaction.objects.count(), 2)

    def test_get_transaction(self):
        response = self.client.get(f"/transactions/{self.transaction.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['operationType'], self.transaction.operationType)

    def test_update_transaction(self):
        response = self.client.put(f"/transactions/{self.transaction.id}/", {"operationType": "WITHDRAW", "amount": 25.00}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.transaction.refresh_from_db()
        self.assertEqual(self.transaction.operationType, "WITHDRAW")

    def test_delete_transaction(self):
        response = self.client.delete(f"/transactions/{self.transaction.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Transaction.objects.count(), 0)