import json
import plotly.graph_objects as go

from candle_stick_recognition.identity_candlestick import recognize_candlestick
from clients import binance
from helpers import convert_to_minutes, convert_ts_str
import datetime as dt
import pandas as pd
import chart
import talib

# from candle_stick_recognition import recognize


# howLong = 20
# untilThisDate = dt.datetime.now()
# sinceThisDate = untilThisDate - dt.timedelta(hours=howLong)
#
# # binance = binance.Binance('LINAUSDT')
# binance = binance.Binance('ZILUSDT')
# historical = binance.get_historical_data('1h', sinceThisDate, untilThisDate)
from strategy.Spot import Spot
from tools.collect_data import collect_candles, collect_patterns, get_candles_with_patterns, \
    get_all_candles_with_patterns

# collect('BTCUSDT', range='12w', interval='1m', draw=False)

# collect_patterns()

# depth = binance.get_depth(1000)
#
# def get_bids_asks(key: str):
#     total_amount = 0
#     bids = depth[key]
#     for item in bids:
#         price = float(item[0])
#         coin_amount = float(item[1])
#         total_amount += price * coin_amount
#     return total_amount
#
#
# total_bids_amount = get_bids_asks('bids')
# total_asks_amount = get_bids_asks('asks')
#
# print(f"Total bids: ${round(total_bids_amount, 0)}")
# print(f"Total asks: ${round(total_asks_amount, 0)}")
#
# print("LIMIT trend up" if total_asks_amount > total_bids_amount else "LIMIT trend down")



# trades = binance.get_trades(5)
# time = trades[0]['time']
# print(dt.datetime.fromtimestamp(time / 1000))
#
# total_bid_trade = 0
# total_ask_trade = 0
# for item in trades:
#     if item['isBuyerMaker']:
#         total_ask_trade += float(item['qty']) * float(item['price'])
#     else:
#         total_bid_trade += float(item['qty']) * float(item['price'])
#
# print(f"\n[+] Total BUY: ${round(total_bid_trade, 2)}")
# print(f"[-] Total SELL: ${round(total_ask_trade, 2)}")
#
# print("trend up" if total_bid_trade > total_ask_trade else "trend down")

# with open('depth.json', 'w') as f:
#     f.write(json.dumps(depth, indent=2))

# with open('trades.json', 'w') as f:
#     f.write(json.dumps(trades, indent=2))

# historical = get_candles_with_patterns('BTCUSDT', '12w', '1h')
# st = Spot(historical, buy_trigger=70, sell_trigger=-70)
# st.run()
# st.show_money()
from tools.strategy_investigation import show_spot_strategies

show_spot_strategies()

if False:
    best = 0
    best_buy_trigger = 0
    best_buy_times = 0
    best_sell_trigger = 0
    best_sell_times = 0

    for i in range(0, 400, 10):
        for j in range(-200, 0, 10):
            st = Strategy(historical, buy_trigger=i, sell_trigger=j)
            st.run()
            money = st.get_money_net()
            if money > best and st.buyTimes > 10:
                best = money
                best_buy_trigger = i
                best_buy_times = st.buyTimes

                best_sell_trigger = j
                best_sell_times = st.sellTimes

    print('BEST MONEY: ' + str(best))
    print('BUY TRIGGER: ' + str(best_buy_trigger))
    print('SELL TRIGGER: ' + str(best_sell_trigger))
    print('BUY TIMES: ' + str(best_buy_times))
    print('SELL TIMES: ' + str(best_sell_times))

# 1. by 320, sell -80; down trend (buyTimes: 13) 5m
# 2. by 240, sell -70; down trend (buyTimes: 51) 5m


# historical.to_csv('_test.csv')
# chart.draw(historical)

