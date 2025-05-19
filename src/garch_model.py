import pandas as pd
import numpy as np
from arch import arch_model
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('garch_model.log'),
        logging.StreamHandler()
    ]
)

def fit_garch_model():
    """
    Fit a GARCH(1,1) model to NIFTY 50 log returns and forecast volatility.
    Input: data/nifty50_processed_single.csv
    Output: data/garch_forecast.csv
    """
    logger = logging.getLogger(__name__)
    logger.info("Starting GARCH modeling")

    try:
        # Load processed data
        input_path = "data/nifty50_processed_single.csv"
        df = pd.read_csv(input_path)
        logger.info(f"Loaded data from {input_path}")

        # Ensure log returns are available
        df = df.dropna(subset=['log_return'])
        returns = df['log_return'] * 100  # Scale for GARCH

        # Fit GARCH(1,1) model
        model = arch_model(returns, vol='Garch', p=1, q=1, dist='normal')
        garch_fit = model.fit(disp='off')
        logger.info("Fitted GARCH(1,1) model")
        logger.info(garch_fit.summary())

        # Forecast volatility for next 30 days
        forecast = garch_fit.forecast(horizon=30)
        forecast_vol = np.sqrt(forecast.variance.iloc[-1]) / 100  # Rescale

        # Create forecast DataFrame
        last_date = pd.to_datetime(df['Date'].iloc[-1])
        forecast_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=30, freq='D')
        forecast_df = pd.DataFrame({
            'Date': forecast_dates,
            'Forecasted_Volatility': forecast_vol
        })
        forecast_df['Date'] = forecast_df['Date'].dt.strftime('%Y-%m-%d')

        # Save forecast
        output_path = "data/garch_forecast.csv"
        forecast_df.to_csv(output_path, index=False)
        logger.info(f"Saved GARCH forecast to {output_path}")

    except Exception as e:
        logger.error(f"Failed to fit GARCH model: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        fit_garch_model()
    except Exception as e:
        logging.error(f"Script execution failed: {str(e)}")
        exit(1)
        