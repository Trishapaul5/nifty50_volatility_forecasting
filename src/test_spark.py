from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("TestSpark").getOrCreate()
print("Spark Version:", spark.version)
print("Java Version:", spark._jvm.System.getProperty("java.version"))
spark.stop()  # Ensure session is closed

