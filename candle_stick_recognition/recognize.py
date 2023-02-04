from plotly.offline import plot
import plotly.graph_objs as go
import pandas as pd

from candle_stick_recognition.data_prep import data_prep
from candle_stick_recognition.identity_candlestick import recognize_candlestick

data_prep()

# df = pd.read_csv('./_btc_data.csv')
#
# df = recognize_candlestick(df)
#
# o = df['open'].astype(float)
# h = df['high'].astype(float)
# l = df['low'].astype(float)
# c = df['close'].astype(float)
#
# trace = go.Candlestick(
#             open=o,
#             high=h,
#             low=l,
#             close=c)
# data = [trace]
#
# layout = {
#     'title': '2019 Feb - 2020 Feb Bitcoin Candlestick Chart',
#     'yaxis': {'title': 'Price'},
#     'xaxis': {'title': 'Index Number'},
#
# }
#
# fig = dict(data=data, layout=layout)
# plot(fig, filename='btc_candles.html')