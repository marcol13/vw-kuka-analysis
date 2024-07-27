import json
import argparse
import pandas as pd
import numpy as np

from src.models.recording import Recording
from src.models.statistics import Statistics
from src.services.group_data import create_df

from sklearn.preprocessing import StandardScaler

# multiply_dict = {
#     "given_laser_power": 15,
#     "given_wire_speed": 15,
#     "real_wire_speed": 5,
#     "binzel_motor_0_current": 0.1,
#     "binzel_motor_1_current": 0.1,
#     "scansonic_head_angle": 1,
#     "scansonic_tip_depth": 10,
#     "wire_speed_projection": 10,
#     "inverse_wire_speed_projection": 10
# }

# THRESHOLD = 0

def preprocess_data(filename: str):
    with open(filename, 'r') as file:
        data = json.load(file)
    
    return Recording.preprocess(data, filename.split("/")[-1].replace(".json", ""))

def calculate_stats(data: list):
    stats = Statistics(1, 1)
    for frame in data:
        stats.save_file_statistics(frame)
    
    return stats.calculate_statistics()

def calculate_difference(mean_data: list, mean_stats: list, std_stats: list, multiply: int):
    scaler = StandardScaler()
    standard_data = scaler.fit_transform(np.array(mean_data).reshape(-1, 1))
    standard_mean_stats = scaler.transform(np.array(mean_stats).reshape(-1, 1))
    standard_std_stats = scaler.transform(np.array(std_stats).reshape(-1, 1))

    bounrdies = [(mean - std, mean + std) for mean, std in zip(standard_mean_stats, standard_std_stats)]
    diff = []
    for (data, (lower, upper)) in zip(standard_data, bounrdies):
        if data < lower:
            diff.append((lower - data) ** 2)
        elif data > upper:
            diff.append((data - upper) ** 2)

    return sum(diff) * multiply / len(diff) if len(diff) > 0 else 0

def predict_tip(filename: str):
    data = preprocess_data(filename)
    df = create_df(data)
    df_stats = pd.DataFrame(calculate_stats([df])[None])
    max_data = df_stats.loc["max"].values
    model = (data[0]["robot"], data[0]["program"], "".join([str(x) for x in data[0]["model"]]))

    with open("stats.json", 'r') as file:
        stats = json.load(file)
    stats = pd.DataFrame(stats)

    stats_model = stats[[str(model)]].dropna()

    max_stats = []

    for row in stats_model.index.tolist():
        temp = stats_model.loc[row].values[0]
        max_stats.append(temp["max"])

    max_stats = max_stats[:len(max_data)]

    m_data = np.max([m['inverse_wire_speed_projection'] for m in max_data])
    m_stats = np.max([m['inverse_wire_speed_projection'] for m in max_stats])

    if m_data > m_stats * 2:
        return True
    return False
    

# def predict_tip(filename: str):
#     data = preprocess_data(filename)
#     df = create_df(data)
#     df_stats = pd.DataFrame(calculate_stats([df])[None])
#     mean_data = df_stats.loc["mean"].values
#     model = (data[0]["robot"], data[0]["program"], "".join([str(x) for x in data[0]["model"]]))

#     with open("stats.json", 'r') as file:
#         stats = json.load(file)
#     stats = pd.DataFrame(stats)

#     stats_model = stats[[str(model)]].dropna()

#     mean_stats = []
#     std_stats = []

#     for row in stats_model.index.tolist():
#         temp = stats_model.loc[row].values[0]
#         mean_stats.append(temp["mean"])
#         std_stats.append(temp["stdev"])
    
#     mean_stats = mean_stats[:len(mean_data)]
#     std_stats = std_stats[:len(mean_data)]

#     total_sum = 0
#     for var in multiply_dict:
#         m_data = [m[var] for m in mean_data]
#         m_stats = [m[var] for m in mean_stats]
#         s_stats = [m[var] for m in std_stats]
#         total_sum += calculate_difference(m_data, m_stats, s_stats, multiply_dict[var])
        
#     print(total_sum)
#     if total_sum > THRESHOLD:
#         return True
#     return False


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', type=str, help='Path to the JSON file with KUKA robot data')
    args = parser.parse_args()
    
    prediction = predict_tip(args.filename)
    print(f"Prediction: {prediction}")
    