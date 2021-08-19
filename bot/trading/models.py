from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class CryptoCoin(models.Model):
    # real time
    symbol = models.CharField(max_length=20)
    name = models.CharField(max_length=30)

    def __str__(self):
        return "{}".format(self.symbol)


class CryptoBase(models.Model):
    # real time
    symbol = models.CharField(max_length=20)
    name = models.CharField(max_length=30)

    def __str__(self):
        return "{}".format(self.symbol)


class TradingHistory(models.Model):
    """Registro de operaciones"""
    STATUS = (
        ('Open', 'Open'),
        ('Close', 'Close'),
    )

    TYPE_ORDER = (
        ('Buy', 'Buy'),
        ('Sell', 'Sell')
    )
    status = models.CharField(max_length=10, choices=STATUS)
    type_order = models.CharField(max_length=10, choices=TYPE_ORDER)
    date_created = models.DateTimeField(auto_now_add=True)
    coin = models.ForeignKey(CryptoCoin, null=True, on_delete=models.SET_NULL)
    base = models.ForeignKey(CryptoBase, null=True, on_delete=models.SET_NULL)
    amount = models.FloatField()
    buy_price = models.FloatField(default=0.0)
    sell_price = models.FloatField(default=0.0, null=True)
    total = models.FloatField(default=0.0, null=True)
    profile = models.ForeignKey(Profile, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return "pair: {}/{}, amount: {}".format(self.coin, self.base, str(self.amount))
