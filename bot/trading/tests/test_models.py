from django.test import TestCase, Client
from trading.models import *

class TestModels(TestCase):

    def setUp(self):
        self.trading_history1 = TradingHistory.objects.create(
            pair = "BTC/USDT",
            amount = 10,
            price = 100000.0,
            fee = 0.01,
            total = 9.99,
            image = None
        )
        self.trading_history1.save()

    def test_trading_history_creation(self):
        orders = TradingHistory.objects.all()
        self.assertEquals(orders.count(), 1)
        self.assertEquals(TradingHistory.objects.get(id=1), self.trading_history1)

    def test_trading_history_get(self):
        self.assertEquals(TradingHistory.objects.get(id=1), self.trading_history1)

    def tearDown(self):
        self.trading_history1.delete()
