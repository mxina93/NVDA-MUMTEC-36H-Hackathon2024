import os
import sys
from typing import List

# Add the project root to the Python path to allow imports from the data package
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from data import read_csv, detect_anomalies

def get_columns_to_check() -> List[str]:
    """Prompt the user to input columns for anomaly detection."""
    print("Enter the names of the columns you want to check for anomalies, separated by commas:")
    columns_input = input().strip()
    return [col.strip() for col in columns_input.split(',')]

def main():
    # Define file paths
    input_file = os.path.join(project_root, 'data', 'your_file.csv')
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
    columns_to_check = get_columns_to_check()
    
    # Detect anomalies
    print(f"\nDetecting anomalies in columns: {', '.join(columns_to_check)}")
    anomalies = detect_anomalies(df, columns_to_check)
    
    # Print the anomalies
    print("\nDetected Anomalies:")
    print(anomalies)
    
    # Save the anomalies to a new CSV file
    anomalies.to_csv(output_file, index=False)
    print(f"\nAnomalies saved to '{output_file}'")

if __name__ == "__main__":
    main()
