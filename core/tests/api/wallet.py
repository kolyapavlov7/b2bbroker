from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIRequestFactory
from core.api import WalletListCreate, WalletDetailDelete, TransactionListCreate


class WalletTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.factory = APIRequestFactory()
        cls.url = reverse('api:wallets')

    def setUp(self):
        pass

    def test_create1(self):
        """
        Создание кошелька
        :return:
        """

        label = 'l1'
        params = {'label': label}
        request = self.factory.post(self.url, params)
        view = WalletListCreate.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['label'], label)
        self.assertEqual(response.data['balance'], '0.000000000000000000')

    def test_create2(self):
        """
        Попытка создать кошелек с непустым балансом
        :return:
        """

        label = 'l2'
        params = {'label': label, 'balance': 1}
        request = self.factory.post(self.url, params)
        view = WalletListCreate.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['label'], label)
        self.assertEqual(response.data['balance'], '0.000000000000000000')

    def test_list1(self):
        """
        Пагинация списка
        :return:
        """

        for i in range(10):
            params = {'label': 'l{}'.format(i)}
            request = self.factory.post(self.url, params)
            view = WalletListCreate.as_view()
            view(request)

        request = self.factory.get(self.url)
        view = WalletListCreate.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        results = response.data['results']
        self.assertEqual(len(results), 10)

        page_size = 5
        request = self.factory.get(self.url, {'page_size': page_size})
        view = WalletListCreate.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        results = response.data['results']
        self.assertEqual(len(results), page_size)

    def test_list2(self):
        """
        Сортировка списка
        :return:
        """

        for i in range(10):
            params = {'label': 'l{}'.format(i)}
            request = self.factory.post(self.url, params)
            view = WalletListCreate.as_view()
            view(request)

        request = self.factory.get(self.url)
        view = WalletListCreate.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        results = response.data['results']
        self.assertEqual(results[0]['label'], 'l0')
        self.assertEqual(results[1]['label'], 'l1')
        self.assertEqual(results[-2]['label'], 'l8')
        self.assertEqual(results[-1]['label'], 'l9')

        request = self.factory.get(self.url, {'ordering': '-id'})
        view = WalletListCreate.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        results = response.data['results']
        self.assertEqual(results[0]['label'], 'l9')
        self.assertEqual(results[1]['label'], 'l8')
        self.assertEqual(results[-2]['label'], 'l1')
        self.assertEqual(results[-1]['label'], 'l0')

    def test_list3(self):
        """
        Фильтрация списка
        :return:
        """

        for i in range(10):
            params = {'label': 'l{}'.format(i)}
            request = self.factory.post(self.url, params)
            view = WalletListCreate.as_view()
            view(request)

        request = self.factory.get(self.url, {'label': 'l2'})
        view = WalletListCreate.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        results = response.data['results']
        self.assertEqual(len(results), 1)

    def test_detail(self):
        """
        Получение информации о кошельке
        :return:
        """

        label = 'l1'
        params = {'label': label}
        request = self.factory.post(self.url, params)
        view = WalletListCreate.as_view()
        response = view(request)
        pk = response.data['id']

        url = reverse('api:wallets-item', kwargs={'pk': pk})
        request = self.factory.get(url)
        view = WalletDetailDelete.as_view()
        response = view(request, pk=pk)
        self.assertEqual(response.data['id'], pk)
        self.assertEqual(response.data['label'], label)

    def test_destroy1(self):
        """
        Удаление кошелька
        :return:
        """

        label = 'l1'
        params = {'label': label}
        request = self.factory.post(self.url, params)
        view = WalletListCreate.as_view()
        response = view(request)
        pk = response.data['id']

        url = reverse('api:wallets-item', kwargs={'pk': pk})
        request = self.factory.delete(url)
        view = WalletDetailDelete.as_view()
        response = view(request, pk=pk)
        self.assertEqual(response.status_code, 204)

        url = reverse('api:wallets-item', kwargs={'pk': pk})
        request = self.factory.get(url)
        view = WalletDetailDelete.as_view()
        response = view(request, pk=pk)
        self.assertEqual(response.status_code, 404)

    def test_destroy2(self):
        """
        Удаление кошелька, у которого есть транзакции
        :return:
        """

        # создали кошелек
        label = 'l1'
        params = {'label': label}
        request = self.factory.post(self.url, params)
        view = WalletListCreate.as_view()
        response = view(request)
        wallet_id = response.data['id']

        # создали транзакции для кошелька
        params = {'wallet': wallet_id, 'amount': 1}
        request = self.factory.post(reverse('api:transactions'), params)
        view = TransactionListCreate.as_view()
        view(request)

        # попытка удалить кошелек
        url = reverse('api:wallets-item', kwargs={'pk': wallet_id})
        request = self.factory.delete(url)
        view = WalletDetailDelete.as_view()
        response = view(request, pk=wallet_id)
        self.assertEqual(response.status_code, 400)
