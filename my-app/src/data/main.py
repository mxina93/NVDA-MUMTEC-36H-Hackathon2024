import pandas as pd
import os
import sys
import numpy as np
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt


# Add the project root to the Python path to allow imports from the data package
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)


iso_forest = IsolationForest()

def main():
    # Define file paths
    input_file = os.path.join(project_root, 'data', 'ai4i2020.csv')
    output_file = os.path.join(project_root, 'output', 'anomalies.csv')

    # Read the CSV file
    print(f"Reading data from {input_file}\n")
    data = pd.read_csv(input_file)
    print(data.head(5),"\nData loaded successfully\n")


    # extract relevant features
    features_columns = ["Air temperature [K]", "Process temperature [K]", "Rotational speed [rpm]", "Torque [Nm]" ]

    features = data[features_columns]

    # fit data to features
    iso_forest.fit(features)

    # predict anomalies based on model
    anomalies = iso_forest.predict(features)

    # add anomalies to dataframe
    data['Anomaly'] = anomalies

    # calculate how much of the data is anomalous
    n_anomaly = len(data[data['Anomaly']== -1])
    n_total = len(data)
    percentage_an = n_anomaly/n_total * 100


    if percentage_an < 20:
        print("Risk of hardware failure is low.")
    elif percentage_an > 20 and percentage_an < 40:
        print("Risk of hardware failure is medium")
    else:
        print("Risk of hardware failure is high")

if __name__ == "__main__":
    main()
