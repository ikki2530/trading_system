import websocket, json, pprint, talib
import numpy as np
import config
from binance.client import Client
from binance.enums import *
# link de api de binance
# https://github.com/binance/binance-spot-api-docs/blob/master/web-socket-streams.md#klinecandlestick-streams
SOCKET = "wss://stream.binance.com:9443/ws/ethusdt@kline_1m"
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
TRADE_SYMBOL = 'ETHUSDT'
TRADE_QUANTITY = 0.05

closes = []
in_position = False

client = Client(config.API_KEY, config.API_SECRET)

def order(side, quantity, symbol, order_type=ORDER_TYPE_MARKET):
    try:
        print("Sending order!!!")
        # order = client.create_order(
        #     symbol=symbol,
        #     side=side,
        #     type=order_type,
        #     quantity=quantity)
        # print(order)
        return True
    except Exception as e:
        return False
    
    return True

def on_open(ws):
    print("opened connection")

def on_close(ws):
    print("closed connection")

def on_message(ws, message):
    global closes
    print("received message")
    json_message = json.loads(message)
    pprint.pprint(json_message)

    candle = json_message['k']
    is_candle_close = candle['x']
    close = candle['c']

    if is_candle_close:
        print("candle closed at {}".format(close))
        closes.append(close)
        print("closes", closes)

        if len(closes) > RSI_PERIOD:
            np_closes = np.array(closes)
            rsi = talib.RSI(np_closes, RSI_PERIOD)
            print("all rsis calculated so far")
            print(rsi)
            last_rsi = rsi[-1]
            print("the current rsi is {}".format(last_rsi))
            if last_rsi > RSI_OVERBOUGHT:
                if in_position:
                    print("Overbought sell! sell!")
                    # vender, sobrecompra
                    order_succeded = order(SIDE_SELL, TRADE_QUANTITY, TRADE_SYMBOL)
                    if order_succeded:
                        in_position = False
                else:
                    print("we don't own any. Nothing to do")
            if last_rsi < RSI_OVERSOLD:
                if in_position:
                    # ya entramos en una posición anterior
                    print("It is oversold, but you already own it, nothing to do!")
                else:
                    # comprar
                    print("Pversold! Buy buy!")
                    order_succeded = order(SIDE_BUY, TRADE_QUANTITY, TRADE_SYMBOL)
                    if order_succeded:
                        in_position = True

ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()