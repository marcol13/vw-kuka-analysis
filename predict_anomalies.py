import json
import os
import argparse
import pandas as pd
import numpy as np

from enum import Enum
from sklearn.linear_model import LinearRegression

from src.models.recording import Recording
from src.services.group_data import create_df


class Problem(Enum):
    SPEED_MAPPING = "SPEED_MAPPING"
    ENGINE_CURRENT = "ENGINE_CURRENT"

    def __str__(self):
        return self.value

THRESHOLD_DICT = {
    "binzel_motor_0_current": 100,
    "binzel_motor_1_current": 100,
    "wire_speed_projection": 0.9
}

def sort_data_by_timestamp(data: list):
    return sorted(data, key=lambda x: x[0])

def preprocess_data(filename: str):
    with open(filename, 'r') as file:
        data = json.load(file)
    
    return Recording.preprocess(data, filename.split("/")[-1].replace(".json", ""))

def get_directory_data(directory: str, vars: list):
    data = []
    for filename in os.listdir(directory):
        raw_data = preprocess_data(f"{directory}/{filename}")
        df = create_df(raw_data)
        data.append((pd.Timestamp(df['timestamp'][0]), {var: df[var].mean() for var in vars}))

    data = sort_data_by_timestamp(data)
    return data

def predict_date(data: list, var: str):
    X = np.array([int(x[0].timestamp()) for x in data]).reshape(-1, 1)
    y = np.array([x[1][var] for x in data])

    model = LinearRegression()
    model.fit(X, y)
    target_time = (THRESHOLD_DICT[var] - model.intercept_) / model.coef_[0]

    return pd.to_datetime(target_time, unit='s')

def predict_anomalies(data: list, problem: Problem):
    if problem == Problem.SPEED_MAPPING:
        data = get_directory_data(args.directory, ['binzel_motor_0_current', 'binzel_motor_1_current'])
        binzel_0_date = predict_date(data, 'binzel_motor_0_current')
        binzel_1_date = predict_date(data, 'binzel_motor_1_current')

        return min(binzel_0_date, binzel_1_date)

    elif problem == Problem.ENGINE_CURRENT:
        data = get_directory_data(args.directory, ['wire_speed_projection'])

        return predict_date(data, 'wire_speed_projection')

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--type', type=Problem, help='Type of the problem to solve', choices=list(Problem))
    parser.add_argument('--directory', type=str, help='Path to the directory with JSON files with KUKA robot data')
    args = parser.parse_args()
    
    data = get_directory_data(args.directory, ['binzel_motor_0_current', 'binzel_motor_1_current'])
    
    predicted_date = predict_anomalies(data, args.type)
    print(f"Predicted date: {predicted_date}")
    