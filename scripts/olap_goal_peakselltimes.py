"""
Module 7: OLAP Goal Script (uses cubed results)
File: scripts/olap_goals_peakselltimes.py

This script uses our precomputed cubed data set to get the information 
we need to answer a specific business goal. 

GOAL: Analyze sales data to determine which days of the week are the most profitable, by region and supplier.

ACTION: This can help inform decisions about reducing operating hours 
or focusing marketing efforts on less profitable days.

PROCESS: 
Group transactions by the date of sale and customer ID.
Average the number of sales per customer per day of the week.
Sum SaleAmount for each day of the week.
Identify the day with the lowest total revenue.

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

def analyze_peak_sell_times(cube_df: pd.DataFrame) -> pd.DataFrame:
    """
    Analyze peak sell times by region and supplier.
    
    Args:
        cube_df (pd.DataFrame): The OLAP cube DataFrame.
        
    Returns:
        pd.DataFrame: DataFrame with analysis results.
    """
    # Group by DayOfWeek, Region, and Supplier
    grouped_df = cube_df.groupby(['DayOfWeek', 'region', 'supplier'])['sale_amount_sum'].sum().reset_index()
    
    # Find the day with the highest total revenue for each region and supplier
    peak_sell_times = grouped_df.loc[grouped_df.groupby(['region', 'supplier'])['sale_amount_sum'].idxmax()]
    
    return peak_sell_times

def visualize_peak_sell_times(peak_sell_times: pd.DataFrame) -> None:
    """
    Visualize peak sell times using a bar plot.
    
    Args:
        peak_sell_times (pd.DataFrame): DataFrame with peak sell times.
    """
    plt.figure(figsize=(12, 6))
    sns.barplot(data=peak_sell_times, x='DayOfWeek', y='sale_amount_sum', hue='region')
    plt.title('Peak Sell Times by Region and Supplier')
    plt.xlabel('Day of the Week')
    plt.ylabel('Total Sale Amount')
    plt.legend(title='Region')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Save the plot
    plot_path = RESULTS_OUTPUT_DIR.joinpath("peak_sell_times.png")
    plt.savefig(plot_path)
    logger.info(f"Peak sell times visualization saved to {plot_path}.")
    plt.show()

def main() -> None:
    """Main function to run the analysis."""
    try:
        # Load the OLAP cube data
        olap_cube_df = load_olap_cube(CUBED_FILE)
        
        # Analyze peak sell times
        peak_sell_times = analyze_peak_sell_times(olap_cube_df)
        
        # Save the analysis results to a CSV file
        results_path = RESULTS_OUTPUT_DIR.joinpath("peak_sell_times_analysis.csv")
        peak_sell_times.to_csv(results_path, index=False)
        logger.info(f"Peak sell times analysis saved to {results_path}.")
        
        # Visualize the results
        visualize_peak_sell_times(peak_sell_times)
    
    except Exception as e:
        logger.error(f"Error in main function: {e}")

if __name__ == "__main__":
    main()