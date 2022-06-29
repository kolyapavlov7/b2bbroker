from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIRequestFactory
from core.api import WalletListCreate, WalletDetailDelete, TransactionListCreate, TransactionDetailDelete


class TransactionTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.factory = APIRequestFactory()
        cls.wallets_url = reverse('api:wallets')
        cls.transactions_url = reverse('api:transactions')

        # создали кошелек
        params = {'label': 'l1'}
        request = cls.factory.post(cls.wallets_url, params)
        view = WalletListCreate.as_view()
        response = view(request)
        cls.wallet_id = response.data['id']

    def setUp(self):
        pass

    def test_create1(self):
        """
        Создание и удаление транзакции
        :return:
        """

        # провели транзакцию с положительной суммой
        params = {'wallet': self.wallet_id, 'amount': '1.000000000000000001'}
        request = self.factory.post(self.transactions_url, params)
        view = TransactionListCreate.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['amount'], '1.000000000000000001')
        transaction1 = response.data['id']

        # проверили баланс кошелька
        url = reverse('api:wallets-item', kwargs={'pk': self.wallet_id})
        request = self.factory.get(url)
        view = WalletDetailDelete.as_view()
        response = view(request, pk=self.wallet_id)
        self.assertEqual(response.data['balance'], '1.000000000000000001')

        # провели транзакцию с отрицательной суммой
        params = {'wallet': self.wallet_id, 'amount': '-0.000000000000000001'}
        request = self.factory.post(self.transactions_url, params)
        view = TransactionListCreate.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['amount'], '-0.000000000000000001')
        transaction2 = response.data['id']

        # проверили баланс кошелька
        url = reverse('api:wallets-item', kwargs={'pk': self.wallet_id})
        request = self.factory.get(url)
        view = WalletDetailDelete.as_view()
        response = view(request, pk=self.wallet_id)
        self.assertEqual(response.data['balance'], '1.000000000000000000')

        # удаляем транзакцию с отрицательной суммой
        url = reverse('api:transactions-item', kwargs={'pk': transaction2})
        request = self.factory.delete(url)
        view = TransactionDetailDelete.as_view()
        view(request, pk=transaction2)

        # проверили баланс кошелька
        url = reverse('api:wallets-item', kwargs={'pk': self.wallet_id})
        request = self.factory.get(url)
        view = WalletDetailDelete.as_view()
        response = view(request, pk=self.wallet_id)
        self.assertEqual(response.data['balance'], '1.000000000000000001')

        # удаляем транзакцию с отрицательной суммой
        url = reverse('api:transactions-item', kwargs={'pk': transaction1})
        request = self.factory.delete(url)
        view = TransactionDetailDelete.as_view()
        view(request, pk=transaction1)

        # проверили баланс кошелька
        url = reverse('api:wallets-item', kwargs={'pk': self.wallet_id})
        request = self.factory.get(url)
        view = WalletDetailDelete.as_view()
        response = view(request, pk=self.wallet_id)
        self.assertEqual(response.data['balance'], '0.000000000000000000')



