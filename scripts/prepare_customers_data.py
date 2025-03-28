"""
scripts/data_preparation/prepare_customers_data.py

This script reads customer data from the data/raw folder, cleans the data, 
and writes the cleaned version to the data/prepared folder.

Tasks:
- Remove duplicates
- Handle missing values
- Remove outliers
- Ensure consistent formatting

-----------------------------------
How to Run:
1. Open a terminal in the main root project folder.
2. Activate the local project virtual environment.
3. Choose the correct commands for your OS to run this script:

Example (Windows/PowerShell) - do NOT include the > prompt:
> .venv\Scripts\activate
> py scripts\data_preparation\prepare_customers_data.py

Example (Mac/Linux) - do NOT include the $ prompt:
$ source .venv/bin/activate
$ python3 scripts/data_preparation/prepare_customers_data.py
----------------------------------- 
"""

# Standard library imports
import pathlib
import sys
import pandas as pd

# for local imports, temporarily add project root to Python sys.path
PROJECT_ROOT = str(pathlib.Path(__file__).resolve().parent.parent.parent)
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(PROJECT_ROOT)

# Local application/library specific imports
from utils.logger import logger

# Constants
DATA_DIR: pathlib.Path = PROJECT_ROOT.joinpath("data")
RAW_DATA_DIR: pathlib.Path = DATA_DIR.joinpath("raw")
PREPARED_DATA_DIR: pathlib.Path = DATA_DIR.joinpath("prepared")

# -------------------
# Reusable Functions
# -------------------

def load_data(file_name: str, file_path: pathlib.Path) -> pd.DataFrame:
    """
    Read a CSV file from the raw data directory and return a pandas DataFrame.
    
    Args: 
        file_name (str): The name of the CSV file to read.
        file_path (pathlib.Path): The path to the CSV file.
    
    Returns: 
        pd.DataFrame: The data from the CSV file.
    """
    logger.info(f"Reading data from {file_name}...")
    file_path = RAW_DATA_DIR.joinpath(file_name)
    logger.info(f"File path: {file_path}")
    df = pd.read_csv(file_path)
    logger.info(f"Data loaded. Shape: {df.shape}")
    return df

def save_data(df: pd.DataFrame, file_name: str, file_path: pathlib.Path) -> None:
    """
    Save a pandas DataFrame to a CSV file in the prepared data directory.
    
    Args:
        df (pd.DataFrame): The data to save.
        file_name (str): The name of the CSV file to save.
        file_path (pathlib.Path): The path to the CSV file.
    """
    logger.info(f"Saving data to {file_name}...")
    file_path = PREPARED_DATA_DIR.joinpath(file_name)
    logger.info(f"File path: {file_path}")
    df.to_csv(file_path, index=False)
    logger.info("Data saved.")

def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove duplicate rows from a DataFrame.
    
    Args:
        df (pd.DataFrame): The data to clean.
    
    Returns:
        pd.DataFrame: The cleaned data.
    """
    logger.info("Removing duplicate rows...")
    df = df.drop_duplicates()
    logger.info(f"Data shape after removing duplicates: {df.shape}")
    return df

def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Handle missing values in a DataFrame.
    This logic is specific to the actual data and business requirements.
    Args:
        df (pd.DataFrame): Input DataFrame.
    
    Returns:
        pd.DataFrame: DataFrame with missing values handled.
    """
    logger.info("Handling missing values...")
    # Log missing values count before handling
    missing_values_before = df.isna().sum().sum()
    logger.info(f"Missing values count before handling: {missing_values_before}")

    # Fill or drop missing values based on business rules
    # Fill missing values in 'Name' 
    df['Name'] = df['Name'].fillna('Unknown')
    # Drop rows with missing values in 'CustomerID'
    df = df.dropna(subset=['CustomerID'])
    logger.info(f"{len(df)} rows after handling missing values.")
    return df

def remove_outliers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove outliers from a DataFrame.
    Args:
        df (pd.DataFrame): Input DataFrame.
    
    Returns:
        pd.DataFrame: DataFrame with outliers removed.
    """
    logger.info(f"FUNCTION START: remove_outliers with dataframe shape={df.shape}")
    initial_count = len(df)
    # Add logic to remove outliers
    # For example, remove rows where a certain column is outside a valid range
    df = df[(df['AmountSpent'] > 200) & (df['AmountSpent'] < 10000)]

    removed_count = initial_count - len(df)
    logger.info(f"Removed {removed_count} outlier rows.")
    logger.info(f"FUNCTION END: remove_outliers with dataframe shape={df.shape}")
    return df

def main() -> None:
    """
    Main function for processing customer data.
    """
    logger.info("==================================")
    logger.info("STARTING prepare_customers_data.py")
    logger.info("==================================")

    logger.info(f"Root project folder: {PROJECT_ROOT}")
    logger.info(f"data / raw folder: {RAW_DATA_DIR}")
    logger.info(f"data / prepared folder: {PREPARED_DATA_DIR}")
    logger.info(f"scripts folder: {PROJECT_ROOT.joinpath('scripts')}")
    logger.info(f"utils folder: {PROJECT_ROOT.joinpath('utils')}")

    # Load the data
    input_file = load_data("customers.csv", RAW_DATA_DIR)
    output_file = "customers_cleaned.csv"

    # Read raw data
    df = load_data(input_file)

    # Log initial data shape
    logger.info(f"Initial data shape: {df.shape}")

    # CLean column names
    original_columns = df.columns.tolist()
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    logger.info(f"Cleaned column names: {original_columns} -> {df.columns.tolist()}")

    # Log if any column names changed
    changed_columns = [col for col in original_columns if col not in df.columns]
    if changed_columns:
        logger.info(f"Cleaned column names: {', '.join(changed_columns)}")

    # Remove duplicates
    df = remove_duplicates(df)

    # Handle missing values
    df = handle_missing_values(df) 

    # Remove outliers
    df = remove_outliers(df)

    # Save the cleaned data
    save_data(df, output_file, PREPARED_DATA_DIR)

    logger.info("==================================")
    logger.info("FINISHED prepare_customers_data.py")
    logger.info("==================================")

# -------------------
# Conditional Execution Block
# -------------------

if __name__ == "__main__":
    main()

    