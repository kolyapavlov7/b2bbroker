from rest_framework import serializers
from core.models import Wallet

__all__ = ('WalletSerializer', 'WalletCreateSerializer')


class WalletSerializer(serializers.ModelSerializer):

    class Meta:
        model = Wallet
        fields = ['id', 'label', 'balance']


class WalletCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Wallet
        fields = ['label']
