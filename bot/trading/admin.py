from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(TradingHistory)
admin.site.register(Profile)
admin.site.register(CryptoCoin)
admin.site.register(CryptoBase)

