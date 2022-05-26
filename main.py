from binance.client import Client
from datetime import datetime
from dotenv import load_dotenv
import os
import sys
from utilites import get_RSI
import time
import logging


load_dotenv()

logging.basicConfig(
    filename="app.log",
    filemode="a",
    format="%(asctime)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    level=logging.INFO,
)

if len(sys.argv) > 1:
    if sys.argv[1] == "dev":
        API_KEY = os.getenv("DEV_API_KEY")
        API_SECRET = os.getenv("DEV_API_SECRET")
        client = Client(API_KEY, API_SECRET)
    else:
        print("WRONG ARG")
        exit()
else:
    API_KEY = os.getenv("TEST_API_KEY")
    API_SECRET = os.getenv("TEST_API_SECRET")
    client = Client(API_KEY, API_SECRET, testnet=True)
    print("You are on testnet")


balance = float(client.get_asset_balance(asset="USDT")["free"])
start_balance = 192.6580
ordered = False


while 1:
    try:
        balance = float(client.get_asset_balance(asset="USDT")["free"])
        ticker = client.get_all_tickers()[2]["price"]
        buy = round((balance - 50) / float(ticker), 4)
        candles = client.get_historical_klines(
            "ETHUSDT", Client.KLINE_INTERVAL_1MINUTE, "1 hour ago UTC"
        )

        rsi = get_RSI(candles, 14)
        print(rsi)
        if rsi < 35 and not ordered:
            order = client.order_market_buy(symbol="ETHUSDT", quantity=buy)
            ordered, buy_quantity, buy_price = (True, buy, float(ticker))
            print(f"Zakupiles {buy_quantity} ETH po cenie {buy_price}")
            logging.info(f"Zakupiles {buy_quantity} ETH po cenie {buy_price}")

        if ordered and float(ticker) / buy_price > 1.0049:
            order = client.order_market_sell(symbol="ETHUSDT", quantity=buy_quantity)
            ordered = False
            print(
                f"Sprzedales {buy_quantity} ETH po cenie {float(ticker)} z zyskiem {float(ticker) / buy_price}"
            )
            logging.info(
                f"Sprzedales {buy_quantity} ETH po cenie {float(ticker)} z zyskiem {float(ticker) / buy_price}"
            )
            logging.info(f"Zyskales do tej pory {balance-start_balance}")
        elif ordered and float(ticker) / buy_price < 0.961:
            order = client.order_market_sell(symbol="ETHUSDT", quantity=buy_quantity)
            ordered = False
            print(
                f"Sprzedales {buy_quantity} ETH po cenie {float(ticker)} ze strata {float(ticker) / buy_price}"
            )
            logging.info(
                f"Sprzedales {buy_quantity} ETH po cenie {float(ticker)} ze strata {float(ticker) / buy_price}"
            )
            logging.info(f"Zyskales do tej pory {balance-start_balance}")
    except Exception as e:
        print(e)
        logging.info(e)
    time.sleep(1)
