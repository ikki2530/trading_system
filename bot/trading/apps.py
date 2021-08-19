from django.apps import AppConfig


class TradingConfig(AppConfig):
    name = 'trading'

    def ready(self):
        import trading.signals
