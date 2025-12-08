# data-pipelines-gcp

This repository contains infrastructure code (Terraform) and data pipelines (Airflow DAGs, Python scripts) for GCP.

## Data Pipelines

### 1. Streaming Pipeline (Dataflow)
- **DAG**: `dags/streaming_pipeline.py`
- **Script**: `dags/scripts/streaming_beam.py`
- **Description**: Reads JSON messages from a Pub/Sub subscription `streaming-data-sub`, parses them, and streams them into BigQuery table `data_warehouse.streaming_data`.
- **Testing**: Use `dags/scripts/publish_messages.py` to publish dummy data to the topic.

### 2. Batch Pipeline (Spark on Dataproc)
- **DAG**: `dags/spark_batch_pipeline.py`
- **Script**: `dags/scripts/process_data.py`
- **Description**: Submits a PySpark job to an existing Dataproc cluster. The job reads a CSV from GCS, performs aggregations, and writes results to BigQuery.

### 3. Batch Pipeline (BigQuery ELT)
- **DAG**: `dags/bq_elt_pipeline.py`
- **SQL**: `dags/sql/transform_data.sql`
- **Description**: Loads raw CSV data from GCS into a BigQuery staging table, then executes a SQL query to transform and summarize the data into a final table.

## Infrastructure

Infrastructure is managed via Terraform in the `terraform/` directory.

### Setup
1. `cd terraform`
2. `terraform init`
3. `terraform apply -var="project_id=YOUR_PROJECT_ID"`

## Airflow Configuration

Ensure the following Airflow Variables are set in your environment:
- `gcp_project_id`
- `dataflow_temp_bucket`
- `dataproc_staging_bucket`