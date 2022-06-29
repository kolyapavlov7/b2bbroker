from django_filters import rest_framework as df
from core.models import Wallet

__all__ = ('WalletFilter', )


class WalletFilter(df.FilterSet):
    label = df.CharFilter(method='label_filter')
    balance_from = df.CharFilter(method='balance_from_filter')
    balance_to = df.CharFilter(method='balance_to_filter')

    class Meta:
        model = Wallet
        fields = ('id', )

    @staticmethod
    def label_filter(queryset, name, value):
        return queryset.filter(label__icontains=value)

    @staticmethod
    def balance_from_filter(queryset, name, value):
        return queryset.filter(balance__gte=value)

    @staticmethod
    def balance_to_filter(queryset, name, value):
        return queryset.filter(balance__lte=value)
