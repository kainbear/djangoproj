from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Transaction, Wallet
from .serializers import TransactionSerializer, WalletSerializer


@api_view(["GET"])
def get_wallets(request):
    wallets = Wallet.objects.all()
    serializer = WalletSerializer(wallets, many=True)
    return Response(serializer.data)


@api_view(["GET", "POST"])
def create_wallet(request):
    serializer = WalletSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def get_wallet(request, WALLET_UUID):
    try:
        wallet = Wallet.objects.get(WALLET_UUID=WALLET_UUID)
    except Wallet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = WalletSerializer(wallet)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = WalletSerializer(wallet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        wallet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(["GET", "POST"])
def operation(request, WALLET_UUID):
    try:
        wallet = Wallet.objects.get(WALLET_UUID=WALLET_UUID)
    except Wallet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = WalletSerializer(wallet)
        return Response(serializer.data)

    elif request.method == "POST":
        operation_type = request.data.get("operationType")
        amount = request.data.get("amount")

        # Проверка на валидность данных
        if amount <= 0:
            return Response({"error": "Сумма должна быть положительной."}, status=status.HTTP_400_BAD_REQUEST)

        if operation_type == "DEPOSIT":
            wallet.current_balance += amount
        elif operation_type == "WITHDRAW":
            if wallet.current_balance < amount:
                return Response({"error": "Недостаточно средств на кошельке."}, status=status.HTTP_400_BAD_REQUEST)
            wallet.current_balance -= amount
        else:
            return Response({"error": "Неверный тип операции."}, status=status.HTTP_400_BAD_REQUEST)

        # Сохраняем изменения в кошельке
        wallet.save()

        # Создание транзакции
        transaction = Transaction(
            wallet=wallet,
            operationType=operation_type,
            amount=amount,
            running_balance=wallet.current_balance
        )
        transaction.save()

        serializer = TransactionSerializer(transaction)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(["GET", "PUT", "DELETE"])
def get_transaction(request, transaction_id):
    try:
        transaction = Transaction.objects.get(id=transaction_id)
    except Transaction.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = TransactionSerializer(transaction, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        transaction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)