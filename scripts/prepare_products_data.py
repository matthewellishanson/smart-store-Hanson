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
PROJECT_ROOT = str(pathlib.Path(__file__).resolve().parent.parent.parent)
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

def load_data(file_name: str, file_path: pathlib.Path) -> pd.DataFrame:
    """
    Read a CSV file from the raw data directory and return a pandas DataFrame.
    
    Args: 
        file_name (str): The name of the CSV file to read.
        file_path (pathlib.Path): The path to the CSV file.
    
    Returns: 
        pd.DataFrame: The data from the CSV file.
    """
    logger.info(f"Loading data from {file_path}")
    return pd.read_csv(file_path.joinpath(file_name))