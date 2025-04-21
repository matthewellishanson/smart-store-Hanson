"""
Module 6: OLAP Goal Script (uses cubed results)
File: scripts/olap_goals_sales_by_weekday.py

This script uses our precomputed cubed data set to get the information 
we need to answer a specific business goal. 

GOAL: Analyze sales data to determine which day of the week 
consistently shows the lowest sales revenue. 

ACTION: This can help inform decisions about reducing operating hours 
or focusing marketing efforts on less profitable days.

PROCESS: 
Group transactions by the day of the week.
Sum SaleAmount for each day.
Identify the day with the lowest total revenue.

This example assumes a cube data set with the following column names (yours will differ).
DayOfWeek,product_id,customer_id,sale_amount_usd_sum,sale_amount_usd_mean,sale_id_count,sale_ids
Friday,101,1001,6344.96,6344.96,1,[582]
etc.
"""

import pandas as pd
import sqlite3
import pathlib
import sys
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# For local imports, temporarily add project root to Python sys.path
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from utils.logger import logger  # noqa: E402

# Constants
OLAP_OUTPUT_DIR: pathlib.Path = pathlib.Path("data").joinpath("olap_cubing_outputs")
CUBED_FILE: pathlib.Path = OLAP_OUTPUT_DIR.joinpath("multidimensional_olap_cube.csv")
RESULTS_OUTPUT_DIR: pathlib.Path = pathlib.Path("data").joinpath("results")

# Create output directory for results if it doesn't exist
RESULTS_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)