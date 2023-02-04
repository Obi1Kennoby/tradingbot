import math
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
import pandas as pd
from helpers import convert_ts_str, convert_to_minutes


class BaseClient(ABC):
    def __init__(self, symbol: str):
        self.symbol = symbol
        super().__init__()

    def get_historical_data(self, interval, start_time: datetime, end_time: datetime):
        return self._get_historical_data_chunks(interval, start_time, end_time, self._get_candle_count(interval, start_time, end_time))

    @abstractmethod
    def _get_historical_data(self, interval, start_time: int, end_time: int):
        pass

    @abstractmethod
    def get_limit(self):
        pass

    def _get_historical_data_chunks(self, interval, start_time: datetime, end_time: datetime, candle_count: int):
        start = convert_ts_str(str(start_time))
        end = convert_ts_str(str(end_time))

        if self.get_limit() >= candle_count:
            return self._get_historical_data(interval, start, end)

        iteration_count = candle_count / self.get_limit()
        duration = end_time - start_time
        chunk_duration = duration / iteration_count
        iteration_count = math.ceil(iteration_count)

        df = pd.DataFrame()
        for i in range(iteration_count):
            start = convert_ts_str(str(start_time + (chunk_duration * i)))
            chunk = self._get_historical_data(interval, start, end)
            df = df.append(chunk)

        return df

    @staticmethod
    def _get_candle_count(interval, start_time: datetime, end_time: datetime):
        delta = end_time - start_time
        delta_in_minutes = delta.days * 1440 + delta.seconds / 60
        interval_in_minutes = convert_to_minutes(interval)
        return delta_in_minutes / interval_in_minutes

