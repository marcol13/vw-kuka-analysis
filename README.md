<div align="center">

# AI TO ANALYZE DATA FROM KUKA INDUSTRIAL ROBOTS 🤖

  <p align="center">
    This prototype model is designed to detect and predict anomalies related to the malfunction of industrial robots. Its primary objective is to notify workers of potential wear and tear or equipment failures. By employing advanced data analysis techniques and statistical modeling, the phenomena outlined below have been meticulously observed and incorporated into the algorithm's development.
  </p>

</div>


## Overview

The Anomaly Detection and Prediction in Industrial Robots project aims to enhance the reliability and efficiency of robotic systems in industrial settings. The prototype model developed in this project utilizes advanced data analysis and statistical modeling techniques to identify and predict anomalies associated with the malfunction of industrial robots. By detecting signs of wear and tear or potential equipment failures early, the system can proactively inform workers, enabling timely maintenance and reducing downtime

**Benefits**:

- **Increased Efficiency**: Minimizes unexpected downtime by predicting failures early, allowing for scheduled maintenance.
- **Enhanced Safety**: Reduces the risk of accidents by identifying malfunctioning components promptly.
- **Cost Savings**: Lowers maintenance costs through efficient resource allocation and reduced unplanned repairs.
- **Improved Longevity**: Extends the lifespan of industrial robots by ensuring they operate within optimal parameters.

## Technologies Used

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Jupyter Notebook](https://img.shields.io/badge/jupyter-%23FA0F00.svg?style=for-the-badge&logo=jupyter&logoColor=white)


## Getting started

### Prerequisites

1. It is required to have installed python at least in version `3.9`.

```
$ python --version
v3.11.7
```


### Installation

1. Unzip project and change directory
2. Create a Virtual Environment
- On Windows:
```bash
python -m venv venv

.\venv\Scripts\activate
```
- On Linux/Mac:
```bash
python3 -m venv venv

source venv/bin/activate
```

3. Install requirements
```
pip install -r requirements.txt
```

## Usage

There are two scripts designed to perform predictions based on specific data inputs. All information are automatically preprocessed to ensure seamless integration with the predictive model. However, it is important to note that this is a prototype, and there may still be some inaccuracies. Therefore, it is advised not to use this system for special edge cases or critical decision-making scenarios.

### Predict tip depth anomaly

- **File**: `./predict_tip.py`
- **Input**: path to KUKA data file in JSON format
- **Output**: binary decision if there is an anomaly or not
- **Params**: `--filename` path to file in JSON format that includes data about KUKA workflow

**Example**
```bash
python predict_tip.py --filename raw_data/KAA3G1224240R04_20240127_061510-FOLGE37.json
```


Here is a more formal version of your text:

In this case, the objective was to determine whether a tip depth anomaly exists within a singular data file. The primary challenge in this task is the limited amount of faulty training data, which restricts the application of more sophisticated methods. During data extraction, it was observed that all instances of anomalies exhibited a significant peak in the inversion of the preset wire advance speed, which was not present in average data files. Therefore, the sole criterion used for prediction is a sufficiently large maximal peak in this variable.

**Other ideas**:

- Data Segmentation and Analysis: Segment the data into one-second chunks and calculate a set of statistics for each segment. These statistics can be used to measure the distance between 'average' workflows and those containing anomalies. Certain variables may hold more significance than others, and this can be accounted for using algorithms such as `Random Forest`, `Support Vector Machines` (SVM), or even basic `Artificial Neural Networks` (ANN).


### Predict anomalies related with engine current and preset wire advance speed

- **File**: `./predict_anomalies.py`
- **Input**: path to directory full of KUKA data file in JSON format. Files should  include a wider range of dates for better performance. Also all workflows should be take before any replacement.
- **Output**: predicted day of failure.
- **Params**: `--type` -> "SPEED_MAPPING" if you want to check wire speed problem, or "ENGINE_CURRENT" for binzel engines current anomalies. `--directory` -> path to directory with KUKA workflows data. 

**Example**
```bash
python predict_anomalies.py --type ENGINE_CURRENT --directory test
```

In both cases, the datasets lacked sufficient anomaly data. I attempted to predict the approximate date when certain robot components should be replaced. Due to the limited data available, especially for certain programs, I employed a Linear Regression model to estimate the anomaly date. During data extraction, I observed that, on average, parts tend to wear out at a consistent rate, which is why I selected this method.

**Other ideas**:

- `Recurrent Neural Networks` (RNNs): Algorithms like `Long Short-Term Memory `(LSTM) networks and `Gated Recurrent Units` (GRUs) are particularly well-suited for time series analysis due to their ability to effectively capture temporal dependencies and patterns in sequential data. They can model complex relationships over time. However, in this case, employing RNNs was not feasible due to a lack of sufficient data, which is crucial for training these models effectively.

- Small `Transformer` Models: Even in their compact versions, transformer models are highly effective for time series analysis. They can handle long-range dependencies and capture complex patterns within the data. By utilizing self-attention mechanisms, these models can weigh the importance of different time steps, providing a comprehensive understanding of the sequence. However, as with RNNs, the application of transformer models in this scenario was not practical due to the insufficient amount of data necessary for effective model training.


## Industrial use

In an ideal scenario, these algorithms could be employed as real-time analyzers of KUKA workflows. There is significant potential for integrating these solutions using cloud computing technologies, such as those provided by AWS. Specifically, `AWS Lambda` could be utilized to execute prediction functions through scheduled tasks or event-driven triggers, such as those from `Simple Notification Service` (SNS). Historical data could be efficiently managed and stored in `DynamoDB`, given its suitability for document-based data structures. Additionally, `AWS CloudWatch Alarms` or other SNS services could be leveraged to notify engineers of potential faults and risks, thereby enhancing the overall reliability and responsiveness of the system.



## Author

[Marcin Krueger](https://github.com/marcol13) - for "Be the Best" VW 2024