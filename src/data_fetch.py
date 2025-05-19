import pandas as pd
import os
import glob
import logging
from datetime import datetime
import sys
import codecs

# Configure logging with UTF-8 encoding to handle ₹ symbol
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# File handler
file_handler = logging.FileHandler('data_fetch.log', encoding='utf-8')
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

# Console handler with UTF-8 encoding
console_handler = logging.StreamHandler(stream=sys.stdout)
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
console_handler.setStream(codecs.getwriter('utf-8')(sys.stdout.buffer))
logger.addHandler(console_handler)

def process_nse_data(input_dir="C:/Users/user/Downloads/nifty50_csvs", output_path="data/nifty50_historical.csv", csv_pattern="*.csv"):
    """
    Merge multiple NSE NIFTY 50 CSV files into a single CSV with Date, Close, High, Low, Shares Traded, and Turnover.

    Parameters:
    - input_dir (str): Directory containing NSE CSV files
    - output_path (str): Path to save combined CSV
    - csv_pattern (str): Pattern to match CSV files (e.g., '*.csv')

    Returns:
    - pandas.DataFrame: Combined data with specified columns

    Raises:
    - ValueError: If no CSV files are found or data is empty
    - KeyError: If required columns are missing
    - Exception: For other processing errors
    """
    logger.info(f"Processing NSE CSV files from {input_dir}")

    try:
        # Ensure output directory exists
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            logger.info(f"Created directory: {output_dir}")

        # Find all CSV files
        csv_files = glob.glob(os.path.join(input_dir, csv_pattern))
        if not csv_files:
            logger.error(f"No CSV files found matching {csv_pattern} in {input_dir}")
            raise ValueError(f"No CSV files found matching {csv_pattern}")

        # Read and combine CSVs
        dfs = []
        for csv_file in csv_files:
            logger.info(f"Reading {csv_file}")
            df = pd.read_csv(csv_file)
            
            # Check for required columns (with trailing spaces)
            required_columns = ['Date ', 'Close ', 'High ', 'Low ', 'Shares Traded ', 'Turnover (₹ Cr)']
            for col in required_columns:
                if col not in df.columns:
                    logger.error(f"Required column '{col}' not found in {csv_file}. Found columns: {df.columns}")
                    raise KeyError(f"Required column '{col}' not found in {csv_file}")
            
            # Select columns
            df = df[required_columns].copy()
            
            # Rename columns to remove trailing spaces and simplify
            df.columns = ['Date', 'Close', 'High', 'Low', 'Shares_Traded', 'Turnover']
            
            # Convert Date from "DD-MMM-YYYY" (e.g., "01-Jan-2014") to YYYY-MM-DD
            df['Date'] = pd.to_datetime(df['Date'], format='%d-%b-%Y')
            df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
            dfs.append(df)

        # Concatenate all DataFrames
        combined_data = pd.concat(dfs, ignore_index=True)
        if combined_data.empty:
            logger.error("Combined data is empty")
            raise ValueError("No data available after combining CSVs")

        # Sort by Date and remove duplicates
        combined_data['Date'] = pd.to_datetime(combined_data['Date'])
        combined_data = combined_data.sort_values('Date').drop_duplicates(subset=['Date'], keep='last')
        combined_data['Date'] = combined_data['Date'].dt.strftime('%Y-%m-%d')

        # Save to CSV
        combined_data.to_csv(output_path, index=False)
        logger.info(f"Combined data saved to {output_path}")
        return combined_data

    except Exception as e:
        logger.error(f"Failed to process NSE data: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        process_nse_data()
    except Exception as e:
        logger.error(f"Script execution failed: {str(e)}")
        exit(1)