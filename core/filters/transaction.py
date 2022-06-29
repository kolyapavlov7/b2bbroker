from django_filters import rest_framework as df
from core.models import Transaction

__all__ = ('TransactionFilter', )


class TransactionFilter(df.FilterSet):
    tx_id = df.CharFilter(method='tx_filter')
    wallet_id = df.CharFilter(method='wallet_filter')
    amount_from = df.CharFilter(method='amount_from_filter')
    amount_to = df.CharFilter(method='amount_to_filter')

    class Meta:
        model = Transaction
        fields = ('id', )

    @staticmethod
    def wallet_filter(queryset, name, value):
        return queryset.filter(wallet_id=value)

    @staticmethod
    def tx_filter(queryset, name, value):
        return queryset.filter(tx_id__icontains=value)

    @staticmethod
    def balance_from_filter(queryset, name, value):
        return queryset.filter(amount__gte=value)

    @staticmethod
    def balance_to_filter(queryset, name, value):
        return queryset.filter(amount__lte=value)
