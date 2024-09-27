import uuid
from django.db import models
from requests import HTTPError


class Wallet(models.Model):
    WALLET_UUID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    current_balance = models.DecimalField(max_digits=150, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)


class Transaction(models.Model):
    wallet = models.ForeignKey(to=Wallet, on_delete=models.CASCADE)
    operationType = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=150, decimal_places=2, default=0)
    running_balance = models.DecimalField(max_digits=150, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
