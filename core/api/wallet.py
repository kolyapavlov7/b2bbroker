from django.db import models
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView
from rest_framework.filters import OrderingFilter
from rest_framework import status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from core.filters import WalletFilter
from core.models import Wallet
from core.serializers import WalletSerializer, WalletCreateSerializer
from core.paginations import WalletPagination

__all__ = ('WalletListCreate', 'WalletDetailDelete')


class WalletListCreate(ListCreateAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    pagination_class = WalletPagination
    filter_backends = (OrderingFilter, DjangoFilterBackend,)
    filterset_class = WalletFilter
    ordering_fields = ('id', 'balance',)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return self.serializer_class
        return WalletCreateSerializer

    def perform_create(self, serializer):
        return serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        wallet = self.perform_create(serializer)
        wallet_serializer = self.serializer_class(wallet)
        return Response(wallet_serializer.data)


class WalletDetailDelete(RetrieveDestroyAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            super(WalletDetailDelete, self).destroy(request)
        except models.deletion.ProtectedError:
            return Response(
                {
                    'msg': 'Нельзя удалить кошелек, у которого есть транзакции'
                },
                status = status.HTTP_400_BAD_REQUEST
            )

        return Response({'message': 'ok'}, status=status.HTTP_204_NO_CONTENT)
