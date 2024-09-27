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


@api_view(["GET"])
def get_wallet(request, WALLET_UUID):
    try:
        wallet = Wallet.objects.get(WALLET_UUID=WALLET_UUID)
    except Wallet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = WalletSerializer(wallet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET","POST"])
def operation(request, WALLET_UUID):
    try:
        wallet = Wallet.objects.get(WALLET_UUID=WALLET_UUID)
    except Wallet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = WalletSerializer(wallet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "POST":
        serializer = TransactionSerializer(Transaction, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)