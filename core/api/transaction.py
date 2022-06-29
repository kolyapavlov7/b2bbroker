from decimal import Decimal

from django.db import transaction as db_transaction
from rest_framework.generics import RetrieveDestroyAPIView, ListCreateAPIView
from rest_framework.filters import OrderingFilter
from rest_framework import status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from core.models import Transaction
from core.serializers import TransactionSerializer, TransactionCreateSerializer
from core.paginations import TransactionPagination
from core.filters import TransactionFilter

__all__ = ('TransactionListCreate', 'TransactionDetailDelete',)


class TransactionListCreate(ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    pagination_class = TransactionPagination
    filter_backends = (OrderingFilter, DjangoFilterBackend, )
    filterset_class = TransactionFilter
    ordering_fields = ('id', )

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return self.serializer_class
        return TransactionCreateSerializer

    def perform_create(self, serializer):
        return serializer.save()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with db_transaction.atomic():
            transaction = self.perform_create(serializer)
            wallet = transaction.wallet
            wallet.balance += transaction.amount
            wallet.save(update_fields=('balance', ))

        transaction_serializer = self.serializer_class(transaction)
        return Response(transaction_serializer.data)


class TransactionDetailDelete(RetrieveDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def destroy(self, request, *args, **kwargs):
        transaction = self.get_object()
        with db_transaction.atomic():
            self.perform_destroy(transaction)
            wallet = transaction.wallet
            wallet.balance -= transaction.amount
            wallet.save(update_fields=('balance', ))

        return Response({'message': 'ok'}, status=status.HTTP_204_NO_CONTENT)
