from django.shortcuts import render, redirect
from django.contrib import messages
import json
from django.http import JsonResponse

# installed
import config
import csv
from binance.client import Client
from binance.enums import *


# client
client = Client(config.API_KEY, config.API_SECRET)

# Create your views here.
def index(request):


    account = client.get_account()
    balances = account["balances"]
    # print("in index client", balances)

    exchange_info = client.get_exchange_info()
    #print("exchange info",  exchange_info)
    symbols = exchange_info["symbols"]

    print("buyyy", request)



    context = {"title": "CoinView", "my_balances": balances, "symbols": symbols}

    return render(request, './index.html', context)


def buy(request):
    print("from buy", request)
    if request.method == "POST":
        """request.POST tiene el contenido del formulario,
            the ids of the forms fields are the keys"""
        try:

            order = client.create_order(
                symbol=request.POST["symbol"],
                side=SIDE_BUY,
                type=ORDER_TYPE_LIMIT,
                timeInForce=TIME_IN_FORCE_GTC,
                quantity=request.POST["quantity"],
                price=request.POST["price"])
        except Exception as e:
            # save the error
            messages.error(request, e)

    return redirect("home")


def sell(request):
    return render(request, './index.html', {})


def settings(request):
    print("settings!!")
    return render(request, './index.html', {})


def history(request):
    candlesticks = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_15MINUTE,
                                                "20 Feb, 2021", "20 Mar, 2021")
    
    processed_candlesticks = []

    for data in candlesticks:
        candlestick = {
            "time": data[0] / 1000,
            "open": data[1],
            "high": data[2],
            "low": data[3],
            "close": data[4]
        }

        processed_candlesticks.append(candlestick)

    return JsonResponse( processed_candlesticks, safe=False)

