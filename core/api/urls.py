from django.urls import path
from core.api import WalletListCreate, WalletDetailDelete, TransactionListCreate, TransactionDetailDelete


app_name = 'api'
urlpatterns = [
    path('wallets/', WalletListCreate.as_view(), name='wallets'),
    path('wallets/<int:pk>/', WalletDetailDelete.as_view(), name='wallets-item'),
    path('transactions/', TransactionListCreate.as_view(), name='transactions'),
    path('transactions/<int:pk>/', TransactionDetailDelete.as_view(), name='transactions-item'),
]
