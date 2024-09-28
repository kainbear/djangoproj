from django.urls import path
from .views import get_transaction, get_wallets, create_wallet, get_wallet, operation

urlpatterns = [
    path("wallets/", get_wallets, name="get_wallets"),
    path("wallets/create/", create_wallet, name="create_wallet"),
    path("wallets/<str:WALLET_UUID>/", get_wallet, name="get_wallet"),
    path("wallets/<str:WALLET_UUID>/operation/", operation, name="operation"),
     path("transactions/<int:transaction_id>/", get_transaction, name="get_transaction"),
]
