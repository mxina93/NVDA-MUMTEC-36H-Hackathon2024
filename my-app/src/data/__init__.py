# This file is used to initialize the data package

# Import necessary modules
from .data_loader import read_csv
from .anomaly_detector import detect_anomalies
from .anomaly_detector import predict_hardware_failure 

# Define package-level variables
__all__ = ['read_csv', 'detect_anomalies']

# Initialize any package-wide configurations or variables
DATA_VERSION = '1.0.0'
DEFAULT_DATA_PATH = '../data/your_file.csv'

# You can add any package initialization code here
def initialize_data_package():
    print(f"Initializing data package version {DATA_VERSION}")

# Run initialization when the package is imported
initialize_data_package()
