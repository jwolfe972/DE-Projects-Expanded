import os
from pyspark.sql import SparkSession
import findspark
findspark.init()

from pyspark.sql.types import StructType, StringType, TimestampType
import pyspark.sql.functions as F
os.environ["HADOOP_HOME"] = "C:\Hadoop"
os.environ['SPARK_HOME'] = 'C:\Spark\spark-3.5.5-bin-hadoop3'
os.environ['JAVA_HOME'] = 'C:\Program Files\Microsoft\jdk-17.0.15.6-hotspot'


HADOOP_HOME = os.environ['HADOOP_HOME']




def print_batch(batch_df, epoch_id):
    print(f"\n--- Batch {epoch_id} ---")
    batch_df.show(truncate=False)

spark = SparkSession.builder \
    .appName("Test_App") \
    .master("local[*]") \
    .config("spark.jars", "C:\\Spark\\spark-3.5.6-bin-hadoop3\\jars\\spark-sql-kafka-0-10_2.12-3.5.0") \
    .config("spark.hadoop.home.dir", "C:\\Hadoop") \
    .getOrCreate()




schema = StructType() \
    .add("person", StringType()) \
    .add("text", StringType())



df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka1:29092,kafka2:29093,kafka3:29094") \
    .option("subscribe", "Faker-Example") \
    .load()



parsed_df = df.selectExpr("CAST(value AS STRING)") \
    .select(F.from_json(F.col("value"), schema).alias("data")) \
    .select("data.*")



query = parsed_df.writeStream \
    .outputMode("append") \
    .foreachBatch(print_batch) \
    .start() \
    .awaitTermination()