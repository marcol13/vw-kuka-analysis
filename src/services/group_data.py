import os
import pandas as pd

from ..utils.const import FILENAMES_PREFIXES, FINAL_DATA_DIRECTORY, ORIGINAL_DF_COLUMNS, FAILURES
from ..models.file import DataFile
from ..models.statistics import Statistics

from collections import defaultdict
from tqdm import tqdm

def format_data(data: dict, no: int) -> dict:
    df_data = {}
    for key in ORIGINAL_DF_COLUMNS:
        df_data[key] = data[key]
    df_data['model'] = "".join([str(x) for x in data['model']])
    df_data['no'] = no
    df_data['wire_speed_projection'] = data['real_wire_speed'] / data['given_wire_speed'] if data['given_wire_speed'] != 0 else 0
    df_data['inverse_wire_speed_projection'] =  data['given_wire_speed'] / data['real_wire_speed'] if data['real_wire_speed'] != 0 else 0
    return df_data

def create_df(data: list, no: int = 1) -> pd.DataFrame:
    df_data = list(map(lambda x: format_data(x, no), data))
    df = pd.DataFrame(df_data)
    return df

def group_data(omit_failures: bool = True) -> tuple:
    data = defaultdict(list)
    files = os.listdir(FINAL_DATA_DIRECTORY)
    stats = Statistics(1, 1)

    for file in tqdm(files):
        if file.split("_")[0] in FILENAMES_PREFIXES:
            
            file_path = os.path.join(FINAL_DATA_DIRECTORY, file)
            file_data = DataFile(file_path).read()
            model = "".join([str(x) for x in file_data[0]['model']])
            file_group = (file_data[0]['robot'], file_data[0]['program'], model)
        
            idx = len(data[file_group]) + 1
            df = create_df(file_data, idx)
            data[file_group].append(df)

            if omit_failures:
                if file.replace(".json", "") in FAILURES:
                    continue

            stats.save_file_statistics(df, file_group)

    final_stats = stats.calculate_statistics()

    return data, final_stats
