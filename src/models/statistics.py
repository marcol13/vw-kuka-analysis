import pandas as pd

from collections import defaultdict
from tqdm import tqdm

class Statistics:
    def __init__(self, time_window=3, sliding=1):
        self.time_window = time_window
        self.sliding = sliding
        self.window_statistics = []
        self.grouped_stats = defaultdict(lambda: defaultdict(list))

    def calculate_window_statistics(self, file_data: pd.DataFrame, ts: int, group: tuple) -> dict:
        start_time = pd.Timedelta(seconds=ts) - pd.Timedelta(seconds=self.time_window)
        start_time = start_time.total_seconds()
        data = file_data[(file_data['time'] >= start_time) & (file_data['time'] <= ts)]
        numeric_columns = data.select_dtypes(include='number').columns
        numeric_data = data[numeric_columns]
        self.grouped_stats[group][ts].append(numeric_data)
        # return {
        #     'time': ts,
        #     'mean': self.calculate_mean(numeric_data),
        #     'median': self.calculate_median(numeric_data),
        #     'stdev': self.calculate_stdev(numeric_data)
        # }

    def calculate_mean(self, data: pd.DataFrame):
        return data.mean()

    def calculate_median(self, data: pd.DataFrame):
        return data.median()

    def calculate_mode(self, data: pd.DataFrame):
        return data.mode()

    def calculate_variance(self, data: pd.DataFrame):
        return data.var()

    def calculate_stdev(self, data: pd.DataFrame):
        return data.std()
    
    def calculate_all_stats(self, data):
        numeric_columns = data.select_dtypes(include='number').columns
        numeric_data = data[numeric_columns]
        return {
            'count': numeric_data.count(),
            'mean': numeric_data.mean(),
            'median': numeric_data.median(),
            'stdev': numeric_data.std()
        }

    def save_file_statistics(self, file_data: pd.DataFrame, group: tuple) -> list:
        ts = self.sliding
        end_ts = file_data['time'].max()
        while ts <= end_ts:
            self.calculate_window_statistics(file_data, ts, group)
            ts += self.sliding

    def calculate_statistics(self):
        stats = defaultdict(lambda: defaultdict(dict))
        for group in tqdm(self.grouped_stats.keys()):
            for ts in self.grouped_stats[group].keys():
                data = self.grouped_stats[group][ts]
                data = pd.concat(data)
                stats[group][ts - self.time_window // 2] = self.calculate_all_stats(data)

        return stats