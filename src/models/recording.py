import pandas as pd

from ..utils.helpers import extraction_func

class Recording:
    def __init__(self, data: list):
        self.data = Recording.preprocess(data)

    @staticmethod
    def preprocess(data: list, filename: str) -> list:
        data = list(map(lambda x: extraction_func(x, filename), data))
        data = Recording.cut_record(data)
        data = Recording.save_additional_data(data)
        return data

    @staticmethod
    def cut_record(data: list) -> list:
        prev_frame = data[0]
        cut_data = []

        start_flag = False
        end_flag = False

        for frame in data[1:]:
            if frame['preparation_end'] == 0 and prev_frame['preparation_end'] == 1:
                start_flag = True

            if start_flag:
                if frame['wire_cut'] == 1:
                    end_flag = True

                if end_flag:
                    break

                cut_data.append(frame)
            prev_frame = frame

        if not cut_data:
            return data
        
        return cut_data
    
    @staticmethod
    def save_additional_data(data: list):
        start_time = pd.Timestamp(data[0]['timestamp'])
        
        for frame in data:
            frame['time'] = pd.Timedelta(pd.Timestamp(frame['timestamp']) - start_time).total_seconds()

        return data