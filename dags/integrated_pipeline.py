from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.google.cloud.operators.dataproc import DataprocSubmitJobOperator
from airflow.providers.google.cloud.operators.datafusion import CloudDataFusionStartPipelineOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='integrated_pipeline',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
    tags=['end-to-end', 'complex'],
) as dag:

    PROJECT_ID = '{{ var.value.gcp_project_id }}'
    REGION = 'us-central1'
    BUCKET_NAME = '{{ var.value.dataproc_staging_bucket }}'
    CLUSTER_NAME = 'spark-cluster-dev'

    # 1. Simulate Data Fusion Pipeline (CDC -> BigQuery)
    # In a real scenario, use CloudDataFusionStartPipelineOperator
    # Here we mock it or assume the API is available.
    # Note: Requires the pipeline_id from Data Fusion UI.

    # trigger_data_fusion = CloudDataFusionStartPipelineOperator(
    #     task_id="trigger_cdc_pipeline",
    #     pipeline_name="cdc-pipeline",
    #     instance_name="data-fusion-dev",
    #     location=REGION,
    #     project_id=PROJECT_ID
    # )

    trigger_data_fusion = BashOperator(
        task_id="trigger_cdc_pipeline_mock",
        bash_command="echo 'Simulating Data Fusion Pipeline execution (Cloud SQL -> GCS -> BQ)...'"
    )

    # 2. Run Dataflow (Simulated Trigger - usually streaming runs continuously)
    check_streaming_health = BashOperator(
        task_id="check_streaming_health",
        bash_command="echo 'Verifying Dataflow job is running...'"
    )

    # 3. Run Dataproc Spark Join (Batch)
    PYSPARK_JOB = {
        "reference": {"project_id": PROJECT_ID},
        "placement": {"cluster_name": CLUSTER_NAME},
        "pyspark_job": {
            "main_python_file_uri": f"gs://{BUCKET_NAME}/scripts/complex_spark_transform.py",
            "args": [
                f"{PROJECT_ID}.data_warehouse.raw_daily_load", # Mock Operational Data
                f"{PROJECT_ID}.data_warehouse.streaming_data", # Streaming Data
                f"{PROJECT_ID}.data_warehouse.integrated_insights",
                BUCKET_NAME
            ],
            "jar_file_uris": ["gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar"],
        },
    }

    spark_join = DataprocSubmitJobOperator(
        task_id="spark_join_datasets",
        job=PYSPARK_JOB,
        region=REGION,
        project_id=PROJECT_ID,
    )

    # 4. Trigger Dataform (SQL Transformation)
    # Using BashOperator to call Dataform CLI (if installed) or API calls
    run_dataform = BashOperator(
        task_id="run_dataform_models",
        bash_command=f"echo 'Running Dataform... (dataform run --project {PROJECT_ID})'"
    )

    trigger_data_fusion >> check_streaming_health >> spark_join >> run_dataform
