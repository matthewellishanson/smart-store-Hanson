"""
scripts/data_preparation/prepare_products_data.py

This script reads product data from the data/raw folder, cleans the data, 
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
> py scripts\data_preparation\prepare_products_data.py

Example (Mac/Linux) - do NOT include the $ prompt:
$ source .venv/bin/activate
$ python3 scripts/data_preparation/prepare_products_data.py
"""

import pathlib
import sys
import pandas as pd

# for local imports, temporarily add project root to Python sys.path
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

# Local application/library specific imports
from utils.logger import logger

# Constants
DATA_DIR: pathlib.Path = PROJECT_ROOT.joinpath("data")
RAW_DATA_DIR: pathlib.Path = DATA_DIR.joinpath("raw")
PREPARED_DATA_DIR: pathlib.Path = DATA_DIR.joinpath("prepared")

# -------------------
# Reusable Functions
# -------------------

def load_data(file_name: str) -> pd.DataFrame:
    """
    Read a CSV file from the raw data directory and return a pandas DataFrame.
    
    Args: 
        file_name (str): The name of the CSV file to read.
    
    Returns: 
        pd.DataFrame: The data from the CSV file.
    """
    logger.info(f"FUNCTION START: load_data with file_name={file_name}")
    file_path = RAW_DATA_DIR.joinpath(file_name)
    logger.info(f"Reading data from {file_path}")
    df = pd.read_csv(file_path)
    logger.info(f"Loaded dataframe with {len(df)} rows and {len(df.columns)} columns")
    
    logger.info(f"Column datatypes: \n{df.dtypes}")
    logger.info(f"Number of unique values: \n{df.nunique()}")
    
    return df

def save_data(df: pd.DataFrame, file_name: str) -> None:
    """
    Save a pandas DataFrame to the prepared data directory as a CSV file.
    
    Args: 
        df (pd.DataFrame): The DataFrame to save.
        file_name (str): The name of the CSV file to save as.
    """
    logger.info(f"FUNCTION START: save_prepared_data with file_name={file_name}, dataframe shape={df.shape}")
    file_path = PREPARED_DATA_DIR.joinpath(file_name)
    df.to_csv(file_path, index=False)
    logger.info(f"Data saved to {file_path}")

def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove duplicate rows from the DataFrame based on the 'ProductID' column."
    
    Args:
        df (pd.DataFrame): Input DataFrame.
    
    Returns:
        pd.DataFrame: DataFrame with duplicates removed.

    """
    # Log the initial shape of the DataFrame, create initial_count variable
    
    logger.info(f"FUNCTION START: remove_duplicates with dataframe shape={df.shape}")
    initial_count = len(df)

    # Use unique logic to remove duplicates
    # Drop duplicates based on 'ProductID' and keep the first occurrence
    if 'ProductID' not in df.columns:
        logger.error("Error: 'productid' column not found in the data!")
        return df  # Return the unmodified DataFrame
    
    df = df.drop_duplicates(subset=["ProductID"])
    df.drop_duplicates(inplace=True)

    logger.info(f"Removed {initial_count - len(df)} duplicate rows")
    logger.info(f"Dataframe shape after removing duplicates: {df.shape}")

    return df

def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Handle missing values in the DataFrame.
    
    Args:
        df (pd.DataFrame): Input DataFrame.
    
    Returns:
        pd.DataFrame: DataFrame with missing values handled.
    """
    logger.info(f"FUNCTION START: handle_missing_values with dataframe shape={df.shape}")
    
    # Log missing values by column before handling
    # NA means missing or "not a number" - ask your AI for details
    missing_by_col = df.isna().sum()
    logger.info(f"Missing values by column before handling:\n{missing_by_col}")

    df['ProductName'].fillna('Unknown Product', inplace=True)
    df['UnitPrice'].fillna(df['UnitPrice'].median(), inplace=True)
    df['Category'].fillna(df['Category'].mode()[0], inplace=True)
    df.dropna(subset=['ProductID'], inplace=True)  # Remove rows without product ID

    # Log missing values by column after handling
    missing_after = df.isna().sum()
    logger.info(f"Missing values by column after handling:\n{missing_after}")
    logger.info(f"Dataframe shape after handling missing values: {df.shape}")
    return df

def remove_outliers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove outliers from the DataFrame based on the 'UnitPrice' column.
    
    Args:
        df (pd.DataFrame): Input DataFrame.
    
    Returns:
        pd.DataFrame: DataFrame with outliers removed.
    """
    logger.info(f"FUNCTION START: remove_outliers with dataframe shape={df.shape}")
    
    # Log initial count of rows in the DataFrame
    initial_count = len(df)

    # # Calculate the IQR for 'UnitPrice'
    Q1 = df['UnitPrice'].quantile(0.25)
    Q3 = df['UnitPrice'].quantile(0.75)
    IQR = Q3 - Q1

    # # Define lower and upper bounds for outliers
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Remove outliers
    df = df[(df['UnitPrice'] >= lower_bound) & (df['UnitPrice'] <= upper_bound)]

    
    removed_count = initial_count - len(df)
    # Log the number of outlier rows removed
    logger.info(f"Removed {removed_count} outlier rows")    
    logger.info(f"Dataframe shape after removing outliers: {df.shape}")
    return df

def standardize_formats(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize formats in the DataFrame.
    
    Args:
        df (pd.DataFrame): Input DataFrame.
    
    Returns:
        pd.DataFrame: DataFrame with standardized formats.
    """
    logger.info(f"FUNCTION START: standardize_formats with dataframe shape={df.shape}")
    
    # Convert 'ProductName' to lowercase
    # df['ProductName'] = df['ProductName'].str.lower()

    # Convert 'Category' to title case
    # df['Category'] = df['Category'].str.title()

    logger.info(f"Dataframe shape after standardizing formats: {df.shape}")
    return df

def validate_data(df: pd.DataFrame) -> None:
    """
    Validate the DataFrame for any issues.
    
    Args:
        df (pd.DataFrame): Input DataFrame.
    
    Returns:
        None
    """
    logger.info(f"FUNCTION START: validate_data with dataframe shape={df.shape}")
    
    # # Check for negative prices
    # if (df['UnitPrice'] < 0).any():
    #     logger.warning("Warning: Negative prices found in 'UnitPrice' column.")

    # Check for missing values
    if df.isnull().values.any():
        logger.warning("Warning: Missing values found in the DataFrame.")

    # Check for duplicates
    if df.duplicated().any():
        logger.warning("Warning: Duplicate rows found in the DataFrame.")

    logger.info(f"Data validation completed with dataframe shape={df.shape}")
    return df

def main() -> None:
    """
    Main function to execute the data preparation steps.
    """
    logger.info("==================================")
    logger.info("STARTING prepare_products_data.py")
    logger.info("==================================")

    logger.info(f"Root project folder: {PROJECT_ROOT}")
    logger.info(f"data / raw folder: {RAW_DATA_DIR}")
    logger.info(f"data / prepared folder: {PREPARED_DATA_DIR}")

    input_file = "products_data.csv"
    output_file = "products_cleaned.csv"
    logger.info(f"Input file: {input_file}")
    logger.info(f"Output file: {output_file}")

    # Read raw data
    df = load_data(input_file)
    logger.info(f"Initial data shape: {df.shape}")

    # Log initial dataframe information
    logger.info(f"Initial dataframe columns: {', '.join(df.columns.tolist())}")
    logger.info(f"Initial dataframe shape: {df.shape}")

    # Clean column names
    original_columns = df.columns.tolist()
    df.columns = df.columns.str.strip().str.replace(' ', '_')
    logger.info(f"Cleaned column names: {original_columns} -> {df.columns.tolist()}")

    # Log if any column names changed
    changed_columns = [f"{old} -> {new}" for old, new in zip(original_columns, df.columns) if old != new]
    if changed_columns:
        logger.info(f"Cleaned column names: {', '.join(changed_columns)}")

    # Process data
    df = remove_duplicates(df)
    df = handle_missing_values(df)
    df = standardize_formats(df)
    df = remove_outliers(df)
    df = validate_data(df)

    # Save the cleaned data
    save_data(df, output_file)

    logger.info("==================================")
    logger.info("FINISHED prepare_products_data.py")
    logger.info("==================================")

# -------------------
# Conditional Execution Block
# -------------------

if __name__ == "__main__":
    main()

