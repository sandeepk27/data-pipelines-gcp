from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count

def run_job(input_path, output_table, temp_bucket):
    spark = SparkSession.builder \
        .appName("AggregationJob") \
        .getOrCreate()

    # Read CSV
    df = spark.read.csv(input_path, header=True, inferSchema=True)

    # Simple Aggregation: Count records by 'category'
    # Assuming the CSV has a 'category' column. If not, this is just a template.
    if 'category' in df.columns:
        agg_df = df.groupBy("category").count()
    else:
        # Fallback if no category column
        agg_df = df.groupBy(df.columns[0]).count()

    # Write to BigQuery
    # Note: Writing to BQ from Dataproc requires the BigQuery connector
    agg_df.write \
        .format("bigquery") \
        .option("table", output_table) \
        .option("temporaryGcsBucket", temp_bucket) \
        .mode("overwrite") \
        .save()

    spark.stop()

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        print("Usage: process_data.py <input_path> <output_table> <temp_bucket>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_table = sys.argv[2]
    temp_bucket = sys.argv[3]

    run_job(input_path, output_table, temp_bucket)
