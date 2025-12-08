from airflow import DAG
from airflow.providers.google.cloud.operators.dataproc import (
    DataprocSubmitJobOperator,
)
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='spark_batch_pipeline',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
    tags=['batch', 'spark', 'dataproc'],
) as dag:

    PROJECT_ID = '{{ var.value.gcp_project_id }}'
    REGION = 'us-central1'
    CLUSTER_NAME = 'spark-cluster-dev' # Matches the terraform creation
    BUCKET_NAME = '{{ var.value.dataproc_staging_bucket }}'

    PYSPARK_JOB = {
        "reference": {"project_id": PROJECT_ID},
        "placement": {"cluster_name": CLUSTER_NAME},
        "pyspark_job": {
            "main_python_file_uri": f"gs://{BUCKET_NAME}/scripts/process_data.py",
            "args": [
                f"gs://{PROJECT_ID}-raw-data/input.csv",
                f"{PROJECT_ID}.data_warehouse.spark_aggregated_data",
                BUCKET_NAME
            ],
            "jar_file_uris": ["gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar"], # Essential for BQ write
        },
    }

    submit_pyspark = DataprocSubmitJobOperator(
        task_id="submit_pyspark",
        job=PYSPARK_JOB,
        region=REGION,
        project_id=PROJECT_ID,
    )
