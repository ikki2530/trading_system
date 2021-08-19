import websocket, json, pprint, talib
import numpy as np
import config
from binance.client import Client
from binance.enums import *


class Bot():
    def __init__(self, api_key, api_secret, trade_quantity=0.05, trade_symbol=None, intervals=None):
        if type(trade_quantity) != float or trade_quantity < 0.0:
            err = "trade_quantity must be a float greater or equal than 0.0"
            raise ValueError(err)

        self.__api_key = api_key
        self.__api_secret = api_secret
        self.__trade_quantity = trade_quantity
        self.__trade_symbol = trade_symbol
        self.__intervals = intervals
        self.__in_position = False
        self.__closes = []
        self.__rsi = False
        if self.__trade_symbol != None and self.__intervals != None:
            self.__socket = "wss://stream.binance.com:9443/ws/{}@kline_{}".format(self.__trade_symbol, self.__intervals)
        else:
            self.__socket = None
        print("socket", self.__socket)

    @staticmethod
    def order(side, quantity, symbol, order_type=ORDER_TYPE_MARKET):
        try:
            print("Sending order")
            order = client.create_order(
                symbol=symbol,
                side=side,
                type=order_type,
                quantity=quantity)
            print(order)
            return True
        except Exception as e:
            return False
        
        return True


    def on_open(self, ws):
        print("opened connection")

    def on_close(self, ws):
        print("closed connection")


    def on_message(self, ws, message):
        print("received message")
        json_message = json.loads(message)
        pprint.pprint(json_message)

        candle = json_message['k']
        is_candle_close = candle['x']
        close = candle['c']

        if is_candle_close:
            print("candle closed at {}".format(close))
            self.__closes.append(close)
            print("closes", self.__closes)

            if len(self.__closes) > self.__RSI_PERIOD:
                np_closes = np.array(self.__closes)
                rsi = talib.RSI(np_closes, self.__RSI_PERIOD)
                print("all rsis calculated so far")
                print(rsi)
                last_rsi = rsi[-1]
                print("the current rsi is {}".format(last_rsi))
                if last_rsi > self.__RSI_OVERBOUGHT:
                    if self.__in_position:
                        print("Overbought sell! sell!")
                        # vender, sobrecompra
                        order_succeded = order(SIDE_SELL, self.__trade_quantity, self.__trade_symbol)
                        if order_succeded:
                            self.__in_position = False
                    else:
                        print("we don't own any. Nothing to do")
                if last_rsi < self.__RSI_OVERSOLD:
                    if self.__in_position:
                        # ya entramos en una posición anterior
                        print("It is oversold, but you already own it, nothing to do!")
                    else:
                        # comprar
                        print("Pversold! Buy buy!")
                        order_succeded = order(SIDE_BUY, self.__trade_quantity, self.__trade_symbol)
                        if order_succeded:
                            self.__in_position = True
                print("on message position", self.__in_position)


    def rsi(self, RSI_PERIOD=14, RSI_OVERBOUGHT=70, RSI_OVERSOLD = 30, activate=False):
        if activate:
            self.__RSI_PERIOD = RSI_PERIOD
            self.__RSI_OVERBOUGHT = RSI_OVERBOUGHT
            self.__RSI_OVERSOLD = RSI_OVERSOLD
            self.__rsi = True
        else:
            self.__rsi = False


    def start(self):
        if self.__socket == None:
            return False
        if self.__rsi:
            client = Client(self.__api_key, self.__api_secret)
            ws = websocket.WebSocketApp(self.__socket, on_open=self.on_open, on_close=self.on_close, on_message=self.on_message)
            ws.run_forever()
            return True
        else:
            return False

# link de api de binance
# https://github.com/binance/binance-spot-api-docs/blob/master/web-socket-streams.md#klinecandlestick-streams
# SOCKET = "wss://stream.binance.com:9443/ws/ethusdt@kline_1m"
# RSI_PERIOD = 14
# RSI_OVERBOUGHT = 70
# RSI_OVERSOLD = 30
# TRADE_SYMBOL = 'ETHUSDT'
# TRADE_QUANTITY = 0.05

# closes = []
# in_position = False

# client = Client(config.API_KEY, config.API_SECRET)

# def order(side, quantity, symbol, order_type=ORDER_TYPE_MARKET):
#     try:
#         print("Sending order")
#         order = client.create_order(
#             symbol=symbol,
#             side=side,
#             type=order_type,
#             quantity=quantity)
#         print(order)
#         return True
#     except Exception as e:
#         return False
    
#     return True

# def on_open(ws):
#     print("opened connection")

# def on_close(ws):
#     print("closed connection")

# def on_message(ws, message):
#     global closes
#     print("received message")
#     json_message = json.loads(message)
#     pprint.pprint(json_message)

#     candle = json_message['k']
#     is_candle_close = candle['x']
#     close = candle['c']

#     if is_candle_close:
#         print("candle closed at {}".format(close))
#         closes.append(close)
#         print("closes", closes)

#         if len(closes) > RSI_PERIOD:
#             np_closes = np.array(closes)
#             rsi = talib.RSI(np_closes, RSI_PERIOD)
#             print("all rsis calculated so far")
#             print(rsi)
#             last_rsi = rsi[-1]
#             print("the current rsi is {}".format(last_rsi))
#             if last_rsi > RSI_OVERBOUGHT:
#                 if in_position:
#                     print("Overbought sell! sell!")
#                     # vender, sobrecompra
#                     order_succeded = order(SIDE_SELL, TRADE_QUANTITY, TRADE_SYMBOL)
#                     if order_succeded:
#                         in_position = False
#                 else:
#                     print("we don't own any. Nothing to do")
#             if last_rsi < RSI_OVERSOLD:
#                 if in_position:
#                     # ya entramos en una posición anterior
#                     print("It is oversold, but you already own it, nothing to do!")
#                 else:
#                     # comprar
#                     print("Pversold! Buy buy!")
#                     order_succeded = order(SIDE_BUY, TRADE_QUANTITY, TRADE_SYMBOL)
#                     if order_succeded:
#                         in_position = True

# ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
# ws.run_forever()


api_key = config.API_KEY
api_secret = config.API_SECRET
quantity=0.05
symbol = "ethusdt"
intervals = "1m"
blue_bot = Bot(api_key, api_secret, quantity, symbol, intervals)
blue_bot.rsi(activate=True)
blue_bot.start()
