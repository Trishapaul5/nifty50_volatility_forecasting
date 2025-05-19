import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('visualize.log'),
        logging.StreamHandler()
    ]
)

def visualize_data():
    """
    Visualize NIFTY 50 data using Plotly and Seaborn.
    Inputs: data/nifty50_processed_single.csv, data/garch_forecast.csv
    Outputs: Visualizations saved as PNG (Seaborn) and HTML (Plotly) files
    """
    logger = logging.getLogger(__name__)
    logger.info("Starting visualization")

    # Log the current working directory
    current_dir = os.getcwd()
    logger.info(f"Current working directory: {current_dir}")

    # Define absolute path for plots directory
    plots_dir = os.path.abspath("plots")
    if not os.path.exists(plots_dir):
        os.makedirs(plots_dir)
    logger.info(f"Plots directory: {plots_dir}")

    try:
        # Load processed data
        df = pd.read_csv("data/nifty50_processed_single.csv")
        df['Date'] = pd.to_datetime(df['Date'])
        print("Processed Data Columns:", df.columns.tolist())
        logger.info("Loaded processed data")

        # Load forecast data
        forecast_df = pd.read_csv("data/garch_forecast.csv")
        forecast_df['Date'] = pd.to_datetime(forecast_df['Date'])
        print("Forecast Data Columns:", forecast_df.columns.tolist())
        logger.info("Loaded forecast data")

        # Plot 1: Closing Price Trend (Plotly, save as HTML)
        try:
            fig1 = px.line(df, x='Date', y='Close', title='NIFTY 50 Closing Price (2014-2024)')
            logger.info("Created closing price trend plot")
            closing_price_path = os.path.join(plots_dir, "closing_price_trend.html")
            fig1.write_html(closing_price_path)
            logger.info(f"Saved closing price trend plot (HTML) to {closing_price_path}")
            if os.path.exists(closing_price_path):
                logger.info(f"Verified: closing_price_trend.html exists at {closing_price_path}")
            else:
                logger.error(f"Error: closing_price_trend.html was not created at {closing_price_path}")
        except Exception as plot_error:
            logger.error(f"Failed to create/save closing price trend plot: {str(plot_error)}")
            raise

        # Plot 2: Range-Based Volatility (Seaborn)
        plt.figure(figsize=(12, 6))
        sns.lineplot(data=df, x='Date', y='range_volatility')
        plt.title('Range-Based Volatility (High-Low)')
        range_volatility_path = os.path.join(plots_dir, "range_volatility.png")
        plt.savefig(range_volatility_path)
        plt.close()
        logger.info(f"Saved range-based volatility plot to {range_volatility_path}")

        # Plot 3: Volume vs. Volatility (Seaborn)
        plt.figure(figsize=(12, 6))
        sns.scatterplot(data=df, x='Shares_Traded', y='range_volatility', hue='Turnover', size='Turnover')
        plt.title('Trading Volume vs. Range-Based Volatility')
        volume_volatility_path = os.path.join(plots_dir, "volume_vs_volatility.png")
        plt.savefig(volume_volatility_path)
        plt.close()
        logger.info(f"Saved volume vs. volatility plot to {volume_volatility_path}")

        # Plot 4: Forecasted Volatility (Plotly, save as HTML)
        try:
            fig2 = px.line(forecast_df, x='Date', y='Forecasted_Volatility', title='30-Day Forecasted Volatility (GARCH)')
            logger.info("Created forecasted volatility plot")
            forecast_volatility_path = os.path.join(plots_dir, "forecasted_volatility.html")
            fig2.write_html(forecast_volatility_path)
            logger.info(f"Saved forecasted volatility plot (HTML) to {forecast_volatility_path}")
            if os.path.exists(forecast_volatility_path):
                logger.info(f"Verified: forecasted_volatility.html exists at {forecast_volatility_path}")
            else:
                logger.error(f"Error: forecasted_volatility.html was not created at {forecast_volatility_path}")
        except Exception as plot_error:
            logger.error(f"Failed to create/save forecasted volatility plot: {str(plot_error)}")
            raise

    except Exception as e:
        logger.error(f"Failed to visualize data: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        visualize_data()
    except Exception as e:
        logging.error(f"Script execution failed: {str(e)}")
        exit(1)