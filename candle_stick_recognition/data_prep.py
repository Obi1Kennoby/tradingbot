import requests
import pandas as pd
import talib

from candle_stick_recognition.identity_candlestick import recognize_candlestick


def data_prep():
    # link for Bitcoin Data
    link = "https://min-api.cryptocompare.com/data/histoday?fsym=BTC&tsym=USD&limit=365&aggregate=1"

    # API request historical
    historical_get = requests.get(link)

    # access the content of historical api request
    historical_json = historical_get.json()

    # extract json data as dictionary
    historical_dict = historical_json['Data']

    # extract Final historical df
    df = pd.DataFrame(historical_dict,
                                 columns=['close', 'high', 'low', 'open', 'time', 'volumefrom', 'volumeto'],
                                 dtype='float64')

    # time column is converted to "YYYY-mm-dd hh:mm:ss" ("%Y-%m-%d %H:%M:%S")
    posix_time = pd.to_datetime(df['time'], unit='s')

    # append posix_time
    df.insert(0, "Date", posix_time)

    # drop unix time stamp
    df.drop("time", axis = 1, inplace = True)


#######################
    # extract OHLC
    # candle_names = talib.get_function_groups()['Pattern Recognition']
    # op = df['open']
    # hi = df['high']
    # lo = df['low']
    # cl = df['close']
    # # create columns for each pattern
    # for candle in candle_names:
    #     df[candle] = getattr(talib, candle)(op, hi, lo, cl)

    recognize_candlestick(df)
############################
    df.to_csv('./_btc_data.csv')