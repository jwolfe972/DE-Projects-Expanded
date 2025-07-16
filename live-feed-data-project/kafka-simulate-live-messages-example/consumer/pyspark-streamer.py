from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql import Window
import os
import findspark
import datetime
from pathlib import Path
from io import BytesIO
from pyspark.sql.types import StructType, StructField, StringType


############################### VARIABLES ##############################################
os.environ['JAVA_HOME'] = 'C:\\Java\\jdk-11'
os.environ['SPARK_HOME'] = 'C:\\Spark\\spark-3.5.6-bin-hadoop3'
os.environ['HADOOP_HOME'] = 'C:\\Spark\\spark-3.5.6-bin-hadoop3'
os.environ['LOCAL_IP'] = 'localhost'
findspark.init()
#####################################################################################################################

schema = StructType() \
    .add('person', StringType())\
    .add('text', StringType())
url = "jdbc:postgresql://localhost:5432/de-projects-db"

def write_to_postgres(batch_df, batch_id):
    try:
        print(f"\n=== Batch {batch_id} ===")
      #  batch_df.show(truncate=False)
        batch_df.write \
            .format("jdbc") \
            .option("url", url) \
            .option("dbtable", "live_data_tbl") \
            .option("user", "user") \
            .option("password", "password") \
            .option("driver", "org.postgresql.Driver") \
            .mode("append") \
            .save()
    except Exception as e:
        print(f'Error reading {batch_id}: {e}')


if __name__ == "__main__":
    url = "jdbc:postgresql://localhost:5432/de-projects-db"
    properties = {
        'user': 'user',
        'password': 'password',
        'driver': 'org.postgresql.Driver'
    }
    spark = SparkSession.builder \
        .appName('Pyspark Streaming App') \
        .master("local[*]") \
        .config("spark.driver.memory", "2g") \
        .config("spark.jars", "C:\\Spark\\spark-3.5.6-bin-hadoop3\\jars\\spark-sql-kafka-0-10_2.12-3.5.0.jar,"
                              "C:\\Spark\\spark-3.5.6-bin-hadoop3\\jars\\kafka-clients-3.4.1.jar,"
                              "C:\\Spark\\spark-3.5.6-bin-hadoop3\\jars\\spark-tags_2.12-3.5.0.jar,"
                              "C:\\Spark\\spark-3.5.6-bin-hadoop3\\jars\\spark-token-provider-kafka-0-10_2.12-3.5.0.jar,"
                              "C:\\Spark\\spark-3.5.6-bin-hadoop3\\jars\\jsr305-3.0.0.jar,"
                              "C:\\Spark\\spark-3.5.6-bin-hadoop3\\jars\\commons-pool2-2.11.1.jar,"
                              "C:\\Spark\\spark-3.5.6-bin-hadoop3\\jars\\postgresql-42.7.7.jar") \
        .getOrCreate()

    spark.conf.set("spark.sql.legacy.parquet.nanosAsLong", "true")
    spark.conf.set("spark.sql.session.timeZone", "UTC")
    spark.conf.set("spark.sql.shuffle.partitions", "10")

    print(spark.version)

    df = spark.readStream.format('kafka').option("kafka.bootstrap.servers", "localhost:29092,localhost:29093,localhost:29094")\
        .option('subscribe', 'Ppl-Text') \
        .option("startingOffsets", "earliest") \
        .option("group.id", "main-group") \
        .load()\
        .selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)") \
        .select(F.from_json(F.col("value"), schema).alias("data")) \
        .select("data.*")

    # df.writeStream \
    #     .format("console") \
    #     .option("truncate", "false") \
    #     .option("checkpointLocation", f"C:\\Users\\hu78i\\Documents\\GitHub\\DE-Projects-Expanded\\live-feed-data-project\\kafka-simulate-live-messages-example\\consumer\\ppl-text")\
    #     .start() \
    #     .awaitTermination()

    df.writeStream \
        .foreachBatch(write_to_postgres) \
        .option("checkpointLocation", f"C:\\Users\\hu78i\\Documents\\GitHub\\DE-Projects-Expanded\\live-feed-data-project\\kafka-simulate-live-messages-example\\consumer\\ppl-text-v2+")\
        .start() \
        .awaitTermination()


