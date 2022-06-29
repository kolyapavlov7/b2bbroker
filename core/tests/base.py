from django.test import TestCase


class Request:
    def __init__(self):
        self.method = 'GET'


class BaseTestCase(TestCase):
    url = 'http://127.0.0.1'
