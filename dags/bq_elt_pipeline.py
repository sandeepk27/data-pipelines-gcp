from airflow import DAG
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='bq_elt_pipeline',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
    tags=['batch', 'bigquery', 'elt'],
) as dag:

    PROJECT_ID = '{{ var.value.gcp_project_id }}'
    RAW_BUCKET = f"{PROJECT_ID}-raw-data"

    # 1. Load Raw Data from GCS to BigQuery Staging Table
    load_csv = GCSToBigQueryOperator(
        task_id='load_csv_to_bq',
        bucket=RAW_BUCKET,
        source_objects=['daily_data/*.csv'],
        destination_project_dataset_table=f'{PROJECT_ID}.data_warehouse.raw_daily_load',
        write_disposition='WRITE_TRUNCATE',
        source_format='CSV',
        autodetect=True,
    )

    # 2. Transform Data using SQL
    transform_data = BigQueryInsertJobOperator(
        task_id="transform_data",
        configuration={
            "query": {
                "query": "{% include 'sql/transform_data.sql' %}",
                "useLegacySql": False,
                "priority": "BATCH",
            }
        },
        params={'project_id': PROJECT_ID}
    )

    load_csv >> transform_data
