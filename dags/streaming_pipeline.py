from airflow import DAG
from airflow.providers.google.cloud.operators.dataflow import DataflowCreatePythonJobOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='streaming_dataflow_pipeline',
    default_args=default_args,
    schedule_interval='@once',  # Streaming pipelines are usually triggered once and run forever
    catchup=False,
    tags=['streaming', 'dataflow'],
) as dag:

    # NOTE: You need to set these variables or use Airflow Variables
    PROJECT_ID = '{{ var.value.gcp_project_id }}'
    REGION = 'us-central1'
    BUCKET_NAME = '{{ var.value.dataflow_temp_bucket }}'

    start_streaming_job = DataflowCreatePythonJobOperator(
        task_id="start_streaming_job",
        py_file="dags/scripts/streaming_beam.py",
        job_name="streaming-beam-job",
        location=REGION,
        options={
            "input_subscription": f"projects/{PROJECT_ID}/subscriptions/streaming-data-sub",
            "output_table": f"{PROJECT_ID}.data_warehouse.streaming_data",
            "project": PROJECT_ID,
            "region": REGION,
            "temp_location": f"gs://{BUCKET_NAME}/temp",
            "staging_location": f"gs://{BUCKET_NAME}/staging",
            "streaming": True,
        },
    )
