import pandas as pd
from typing import List

def detect_anomalies(data: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """
    Detect anomalies in specified columns using the IQR method.
    
    Args:
        data (pd.DataFrame): Input DataFrame containing the data.
        columns (List[str]): List of column names to check for anomalies.
    
    Returns:
        pd.DataFrame: DataFrame containing the detected anomalies.
    """
    anomalies = pd.DataFrame()

    for column in columns:
        if column not in data.columns:
            print(f"Warning: Column '{column}' not found in the dataset. Skipping.")
            continue
        
        if not pd.api.types.is_numeric_dtype(data[column]):
            print(f"Warning: Column '{column}' is not numeric. Skipping.")
            continue

        Q1 = data[column].quantile(0.25)
        Q3 = data[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        column_anomalies = data[(data[column] < lower_bound) | (data[column] > upper_bound)]
        anomalies = pd.concat([anomalies, column_anomalies])

    return anomalies.drop_duplicates()
