import datetime as dt

from candle_stick_recognition.identity_candlestick import recognize_candlestick
from clients.binance import Binance
import chart
from helpers import convert_to_minutes
from pathlib import Path
import os
import pandas as pd


def collect_candles(symbol: str, range, interval, draw=True, save=True):
    untilThisDate = dt.datetime.utcnow()
    sinceThisDate = untilThisDate - dt.timedelta(minutes=convert_to_minutes(range))

    binance = Binance(symbol)
    historical = binance.get_historical_data(interval, sinceThisDate, untilThisDate)

    if save:
        Path(f'raw/{symbol}/{range}').mkdir(parents=True, exist_ok=True)
        historical.to_csv(f'raw/{symbol}/{range}/{interval}.csv')

    if draw:
        chart.draw(historical)


def collect_patterns():
    for subdir, dirs, files in os.walk('raw'):
        for file in files:
            source = os.path.join(subdir, file)
            Path(f'data/{subdir.removeprefix("raw")}').mkdir(parents=True, exist_ok=True)
            destination = f'data{source.removeprefix("raw")}'

            historical = pd.read_csv(source)
            historical = recognize_candlestick(historical)
            historical.to_csv(destination)


def get_candles_with_patterns(symbol: str, range, interval):
    return pd.read_csv(f'data/{symbol}/{range}/{interval}.csv')


def get_all_candles_with_patterns():
    candles = []
    for subdir, dirs, files in os.walk('data'):
        for file in files:
            filename = os.path.join(subdir, file)
            symbol, range, interval = filename.removeprefix('data/').removesuffix('.csv').split('/')
            candles.append(get_candles_with_patterns(symbol, range, interval))
    return candles
