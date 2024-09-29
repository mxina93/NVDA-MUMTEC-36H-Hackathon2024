import pandas as pd
import os
import sys
from typing import List

# Add the project root to the Python path to allow imports from the data package
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from data import read_csv, detect_anomalies, predict_hardware_failure

def main():
    # Define file paths
    input_file = os.path.join(project_root, 'data', 'ai4i2020.csv')
    output_file = os.path.join(project_root, 'output', 'anomalies.csv')
    
    # Read the CSV file
    print(f"Reading data from {input_file}")
    df = read_csv(input_file)
    
    if df.empty:
        print("Error: Unable to proceed with empty dataset.")
        return
    
    # Print basic information about the dataset
    print("\nDataset Information:")
    print(df.info())
    print("\nDataset Summary Statistics:")
    print(df.describe())
    
    # Get columns to check from user input
    columns_to_check = pd.DataFrame([
    "Air temperature [K]", 
    "Process temperature [K]", 
    "Rotational speed [rpm]", 
    "Torque [Nm]", 
    "Tool wear [min]", 
    "Machine failure", 
    "TWF", 
    "HDF", 
    "PWF", 
    "OSF", 
    "RNF"])
    
    # Detect anomalies
    anomalies = detect_anomalies(df, columns_to_check)
    
    # Predict hardware failure
    anomalies_with_risk, prediction = predict_hardware_failure(anomalies, columns_to_check)
    
    # Not working
    # Print the anomalies with risk scores
    # ("\nDetected Anomalies with Risk Scores:")
    # print(anomalies_with_risk)
    
    # Print the prediction
    print("\nHardware Failure Prediction:")
    print(prediction)
    
    # Save the anomalies with risk scores to a new CSV file
    anomalies_with_risk.to_csv(output_file, index=False)
    print(f"\nAnomalies with risk scores saved to '{output_file}'")

if __name__ == "__main__":
    main()
