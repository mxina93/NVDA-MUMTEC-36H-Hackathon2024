import pandas as pd

def read_csv(file_path: str) -> pd.DataFrame:
    """
    Read the CSV file and return a pandas DataFrame.
    
    Args:
        file_path (str): Path to the CSV file.
    
    Returns:
        pd.DataFrame: Loaded data as a pandas DataFrame.
    """
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return pd.DataFrame()
    except pd.errors.EmptyDataError:
        print(f"Error: The file at {file_path} is empty")
        return pd.DataFrame()
    except pd.errors.ParserError:
        print(f"Error: Unable to parse the file at {file_path}. Please check if it's a valid CSV.")
        return pd.DataFrame()
