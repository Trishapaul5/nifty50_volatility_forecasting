import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, log, lag, sqrt, pow
from pyspark.sql.window import Window
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('preprocess_spark.log'),
        logging.StreamHandler()
    ]
)

def preprocess_data():
    """
    Preprocess NIFTY 50 data using Spark: compute log returns and range-based volatility.
    Input: data/nifty50_historical.csv
    Output: data/nifty50_processed.csv
    """
    logger = logging.getLogger(__name__)
    logger.info("Starting Spark preprocessing")

    try:
        # Initialize Spark session
        spark = SparkSession.builder \
            .appName("NIFTY50VolatilityPreprocessing") \
            .config("spark.sql.shuffle.partitions", "8") \
            .getOrCreate()

        # Load data
        input_path = "data/nifty50_historical.csv"
        output_path = "data/nifty50_processed.csv"

        # Read CSV
        df = spark.read.csv(input_path, header=True, inferSchema=True)
        logger.info(f"Loaded data from {input_path}")

        # Repartition to avoid single partition bottleneck
        df = df.repartition(8, "Date")  # Partition by Date to distribute data

        # Ensure Date is in correct format and sort
        df = df.withColumn("Date", col("Date").cast("date"))
        df = df.orderBy("Date")

        # Compute log returns: log(Close / lag(Close))
        window = Window.partitionBy().orderBy("Date")  # Partition is handled by repartition
        df = df.withColumn("prev_close", lag("Close").over(window))
        df = df.withColumn("log_return", log(col("Close") / col("prev_close")))
        df = df.drop("prev_close")

        # Compute range-based volatility: (log(High/Low))^2
        df = df.withColumn("range_volatility", pow(log(col("High") / col("Low")), 2))

        # Select relevant columns
        df = df.select("Date", "Close", "High", "Low", "Shares_Traded", "Turnover", "log_return", "range_volatility")

        # Coalesce to a single partition before writing to avoid multiple output files
        df = df.coalesce(1)

        # Save processed data
        df.write.csv(output_path, header=True, mode="overwrite")
        logger.info(f"Saved processed data to {output_path}")

        # Stop Spark session
        spark.stop()

    except Exception as e:
        logger.error(f"Failed to preprocess data: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        preprocess_data()
    except Exception as e:
        logging.error(f"Script execution failed: {str(e)}")
        exit(1)
        