Django-Wallet

A simple wallet django app.

Get All a Wallets:
http://127.0.0.1:8000/api/v1/wallets/

Creating a New Wallet:
http://127.0.0.1:8000/api/v1/wallets/create/ - autocreate when put url

Get a Wallet Using WALLET_UUID:
http://127.0.0.1:8000/api/v1/wallets/<str:WALLET_UUID>/

Make transactions on Wallet, Using WALLET_UUID(DEPOSIT or WITHDRAW):
http://127.0.0.1:8000/api/v1/wallets/<str:WALLET_UUID>/operation/

Get a Info of Transaction using transaction_id:
http://127.0.0.1:8000/api/v1/transactions/<int:transaction_id>/

To start app use:
1.You'r variety of clone project \
2. Than "docker-compose up --build"

For Example for operation use :

{
    "operationType": WITHDRAW or DEPOSIT,
    "amount": x
}