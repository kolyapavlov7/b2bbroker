from rest_framework import serializers
from core.models import Transaction

__all__ = ('TransactionSerializer', 'TransactionCreateSerializer')


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ['id', 'wallet', 'tx_id', 'amount']


class TransactionCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ['wallet', 'tx_id', 'amount']
