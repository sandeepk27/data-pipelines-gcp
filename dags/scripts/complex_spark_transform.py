from pyspark.sql import SparkSession

def run_job(operational_table, streaming_table, output_table, temp_bucket):
    spark = SparkSession.builder \
        .appName("ComplexJoinJob") \
        .getOrCreate()

    # 1. Read Operational Data (Simulating CDC from BigQuery)
    # In reality, this would likely be the result of Datastream -> GCS -> BQ
    op_df = spark.read \
        .format("bigquery") \
        .option("table", operational_table) \
        .load()

    # 2. Read Streaming Data (Events)
    stream_df = spark.read \
        .format("bigquery") \
        .option("table", streaming_table) \
        .load()

    # 3. Join: Find events related to orders (e.g., correlation via ID or Time window)
    # Since these are disparate public datasets, we'll do a cross join or a dummy join key for demonstration.
    # Let's assume we want to enrich orders with some analytics metadata.

    # Adding a dummy key for join if no direct link exists in public data
    op_df = op_df.withColumn("join_key", (op_df.order_id % 10))
    stream_df = stream_df.withColumn("join_key", (stream_df.id % 10)) # Assuming 'id' exists in stream data

    joined_df = op_df.join(stream_df, "join_key", "inner")

    # 4. Aggregation
    result_df = joined_df.groupBy("status").count()

    # 5. Write Result
    result_df.write \
        .format("bigquery") \
        .option("table", output_table) \
        .option("temporaryGcsBucket", temp_bucket) \
        .mode("overwrite") \
        .save()

    spark.stop()

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 5:
        print("Usage: complex_spark_transform.py <op_table> <stream_table> <output_table> <temp_bucket>")
        sys.exit(1)

    run_job(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
