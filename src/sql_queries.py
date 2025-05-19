from pyspark.sql import SparkSession
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('sql_queries.log'),
        logging.StreamHandler()
    ]
)

def run_sql_queries():
    """
    Run SQL queries on processed NIFTY 50 data using Spark SQL.
    Input: data/nifty50_processed_single.csv
    """
    logger = logging.getLogger(__name__)
    logger.info("Starting SQL queries")

    try:
        # Initialize Spark session
        spark = SparkSession.builder \
            .appName("NIFTY50VolatilitySQLQueries") \
            .getOrCreate()

        # Load processed data
        input_path = "data/nifty50_processed_single.csv"
        df = spark.read.csv(input_path, header=True, inferSchema=True)
        logger.info(f"Loaded data from {input_path}")

        # Register DataFrame as a SQL table
        df.createOrReplaceTempView("nifty50")

        # Query 1: Top 10 high-volatility days (range-based)
        logger.info("Query 1: Top 10 high-volatility days")
        high_vol_days = spark.sql("""
            SELECT Date, range_volatility, Close
            FROM nifty50
            WHERE range_volatility IS NOT NULL
            ORDER BY range_volatility DESC
            LIMIT 10
        """)
        high_vol_days.show()

        # Query 2: Days with high trading volume
        logger.info("Query 2: Top 10 days with highest trading volume")
        high_volume_days = spark.sql("""
            SELECT Date, Shares_Traded, Turnover
            FROM nifty50
            WHERE Shares_Traded IS NOT NULL
            ORDER BY Shares_Traded DESC
            LIMIT 10
        """)
        high_volume_days.show()

        # Query 3: Average volatility by year
        logger.info("Query 3: Average range-based volatility by year")
        avg_vol_by_year = spark.sql("""
            SELECT YEAR(Date) as year, AVG(range_volatility) as avg_volatility
            FROM nifty50
            WHERE range_volatility IS NOT NULL
            GROUP BY YEAR(Date)
            ORDER BY year
        """)
        avg_vol_by_year.show()

        # Stop Spark session
        spark.stop()

    except Exception as e:
        logger.error(f"Failed to run SQL queries: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        run_sql_queries()
    except Exception as e:
        logging.error(f"Script execution failed: {str(e)}")
        exit(1)
        