import json
import argparse
import pandas as pd

from src.models.recording import Recording
from src.models.statistics import Statistics

from sklearn.preprocessing import StandardScaler

multiply_dict = {
    "given_laser_power": 1,
    "given_wire_speed": 1,
    "real_wire_speed": 1,
    "binzel_motor_0_current": 1,
    "binzel_motor_1_current": 1,
    "scansonic_head_angle": 1,
    "scansonic_tip_depth": 1,
    "wire_speed_projection": 1
}

def preprocess_data(filename: str):
    with open(filename, 'r') as file:
        data = json.load(file)
    
    return Recording.preprocess(data, filename.split("/")[-1].replace(".json", ""))

def calculate_stats(data: list):
    stats = Statistics(1, 1)
    for frame in data:
        stats.save_file_statistics(frame)
    
    return stats.calculate_statistics()

def calculate_difference(data: list, stats: dict):
    pass

def predict_tip(filename: str):
    data = preprocess_data(filename)
    print(data[0])
    model = (data[0]["robot"], data[0]["program"], "".join([str(x) for x in data[0]["model"]]))

    with open("stats.json", 'r') as file:
        stats = json.load(file)
        stats = pd.DataFrame(stats)

    print(stats[[str(model)]])

    # reference_stat = stats[[((model))][0]]
    # print(reference_stat)

    return None


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', type=str, help='Path to the JSON file with KUKA robot data')
    args = parser.parse_args()
    
    predict_tip(args.filename)
    