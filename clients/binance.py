import datetime as dt
import helpers
import json
import requests
import pandas as pd

from clients.base import BaseClient


class Binance(BaseClient):
    __root_url = 'https://api.binance.com/'

    def _get_historical_data(self, interval: str, start_time: int, end_time: int):
        url = self.__get_url('api/v1/klines') + '?symbol=' + self.symbol + '&interval=' + interval + '&startTime=' + str(start_time) + '&endTime=' + str(end_time) + '&limit=' + str(self.get_limit())
        data = json.loads(requests.get(url).text)
        df = pd.DataFrame(data)
        df.columns = ['open_time',
                      'o', 'h', 'l', 'c', 'v',
                      'close_time', 'qav', 'num_trades',
                      'taker_base_vol', 'taker_quote_vol', 'ignore']
        df.index = [dt.datetime.fromtimestamp(x / 1000.0) for x in df.open_time]
        return df.drop(columns=['qav', 'num_trades', 'taker_base_vol', 'taker_quote_vol', 'ignore'])

    def get_limit(self):
        return 1000

    def get_depth(self, limit=1000):
        url = self.__get_url('api/v3/depth') + '?symbol=' + self.symbol + '&limit=' + str(limit)
        data = json.loads(requests.get(url).text)
        return data

    def get_trades(self, limit=1000):
        url = self.__get_url('api/v3/trades') + '?symbol=' + self.symbol + '&limit=' + str(limit)
        data = json.loads(requests.get(url).text)
        return data

    def __get_url(self, endpoint_url):
        return self.__root_url + endpoint_url


