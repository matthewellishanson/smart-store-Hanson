"""
Module 6: OLAP Goal Script (uses cubed results)
File: scripts/olap_goals_customers_by_purchase_frequency.py

This script uses our precomputed cubed data set to get the information 
we need to answer a specific business goal. 

GOAL: Analyze sales data to determine which customers make the most frequent purchases, and which months and days of the week are the most profitable.

ACTION: This can help inform decisions about reducing operating hours 
or focusing marketing efforts on less profitable days.

PROCESS: 
Group transactions by the date of sale and customer ID.
Average the number of sales per customer per month.
Sum SaleAmount for each month.
Identify the day with the lowest total revenue.

This example assumes a cube data set with the following column names (yours will differ).
DayOfWeek,Month,product_id,customer_id,sale_amount_usd_sum,sale_amount_usd_mean,sale_id_count,sale_ids
Friday,June,101,1001,6344.96,6344.96,1,[582]
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

def load_olap_cube(file_path: pathlib.Path) -> pd.DataFrame:
    """Load the precomputed OLAP cube data."""
    try:
        cube_df = pd.read_csv(file_path)
        logger.info(f"OLAP cube data successfully loaded from {file_path}.")
        return cube_df
    except Exception as e:
        logger.error(f"Error loading OLAP cube data: {e}")
        raise

def analyze_customer_purchase_frequency(cube_df: pd.DataFrame) -> pd.DataFrame:
    """
    Analyze customer purchase frequency and identify the day with the lowest total revenue.
    """
    try:
        # Group by Month and customer_id, then calculate the average number of sales per customer per month
        purchase_frequency = (
            cube_df.groupby(['Month', 'customer_id'])
            .agg({'transaction_id_count': 'mean'})
            .reset_index()
        )
        
        # Calculate total sales amount for each month
        monthly_sales = (
            cube_df.groupby(['Month'])
            .agg({'sale_amount_sum': 'sum'})
            .reset_index()
        )
        
        # Merge the two dataframes on Month
        analysis_df = pd.merge(purchase_frequency, monthly_sales, on='Month')
        
        # Identify the day with the lowest total revenue
        lowest_revenue_day = cube_df.groupby('DayOfWeek')['sale_amount_sum'].sum().idxmin()
        
        logger.info("Customer purchase frequency analysis completed.")
        return analysis_df, lowest_revenue_day
    except Exception as e:
        logger.error(f"Error analyzing customer purchase frequency: {e}")
        raise

def visualize_sales_by_weekday(sales_by_weekday: pd.DataFrame) -> None:
    """
    Visualize sales by weekday using a bar plot.
    """
    try:
        plt.figure(figsize=(10, 6))
        sns.barplot(x='DayOfWeek', y='sale_amount_sum', data=sales_by_weekday, palette='viridis')
        plt.title('Sales Amount by Day of the Week')
        plt.xlabel('Day of the Week')
        plt.ylabel('Total Sales Amount (USD)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(RESULTS_OUTPUT_DIR.joinpath("sales_by_weekday.png"))
        logger.info("Sales by weekday visualization saved.")
    except Exception as e:
        logger.error(f"Error visualizing sales by weekday: {e}")
        raise

def main() -> None:
    """Main function for analyzing customer purchase frequency."""
    logger.info("Starting analysis of customer purchase frequency...")
    
    # Load the OLAP cube data
    olap_cube_df = load_olap_cube(CUBED_FILE)
    
    # Analyze customer purchase frequency
    analysis_df, lowest_revenue_day = analyze_customer_purchase_frequency(olap_cube_df)
    
    # Save the analysis results to a CSV file
    analysis_df.to_csv(RESULTS_OUTPUT_DIR.joinpath("customer_purchase_frequency_analysis.csv"), index=False)
    logger.info(f"Analysis results saved to {RESULTS_OUTPUT_DIR.joinpath('customer_purchase_frequency_analysis.csv')}")
    
    # Visualize sales by weekday
    visualize_sales_by_weekday(olap_cube_df)
    
    logger.info(f"The day with the lowest total revenue is: {lowest_revenue_day}")

if __name__ == "__main__":
    main()
