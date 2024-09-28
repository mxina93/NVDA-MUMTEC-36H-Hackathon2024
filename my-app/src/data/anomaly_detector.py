import pandas as pd
from typing import List, Tuple

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

def predict_hardware_failure(anomalies: pd.DataFrame, columns: List[str]) -> Tuple[pd.DataFrame, str]:
    """
    Predict potential hardware failures based on detected anomalies.
    
    Args:
        anomalies (pd.DataFrame): DataFrame containing the detected anomalies.
        columns (List[str]): List of column names that were checked for anomalies.
    
    Returns:
        Tuple[pd.DataFrame, str]: DataFrame with risk scores and a prediction message.
    """
    if anomalies.empty:
        return anomalies, "No anomalies detected. Low risk of hardware failure."

    # Calculate risk score for each anomaly
    for column in columns:
        if column in anomalies.columns:
            mean = data[column].mean()
            std = data[column].std()
            anomalies[f'{column}_risk_score'] = abs((anomalies[column] - mean) / std)

    # Calculate overall risk score
    anomalies['overall_risk_score'] = anomalies[[f'{col}_risk_score' for col in columns if f'{col}_risk_score' in anomalies.columns]].mean(axis=1)

    # Determine risk level
    max_risk = anomalies['overall_risk_score'].max()
    if max_risk > 3:
        prediction = "High risk of imminent hardware failure. Immediate inspection recommended."
    elif max_risk > 2:
        prediction = "Moderate risk of hardware failure. Schedule an inspection soon."
    else:
        prediction = "Low risk of hardware failure, but continue monitoring."

    return anomalies, prediction
