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
- `cloudsql_public_ip` (After Terraform apply)

## Architecture & Workflows

### 1. Operational to Analytical Pipeline (CDC & Batch)
This pipeline simulates an end-to-end flow from a transactional database to an analytical warehouse.
1.  **Source**: Cloud SQL (Postgres), seeded with `thelook_ecommerce` data.
2.  **Ingestion**: Datastream (CDC) captures changes and writes to GCS.
3.  **Integration**: Cloud Data Fusion reads from GCS, cleans data, and loads to BigQuery (Raw).
4.  **Modeling**: Dataform transforms raw tables into reporting views (`daily_orders`).
5.  **Enrichment**: BigQuery Data Transfer Service brings in external Google Trends data.

### 2. Real-time Intelligence Pipeline (Streaming)
1.  **Source**: Pub/Sub receives events (simulated from `google_analytics`).
2.  **Processing**: Cloud Dataflow (Beam) reads events, aggregates, and writes to BigQuery.
3.  **Advanced Analytics**: Cloud Dataproc (Spark) runs a nightly job to join "Operational" data (Pipeline 1) with "Real-time" data (Pipeline 2) for complex insights.
4.  **Orchestration**: Cloud Composer (Airflow) manages the dependencies and triggers.

### Running the Integrated Demo
1.  **Setup Infra**: `cd terraform && terraform apply`.
2.  **Seed DB**: Trigger the `init_infra_seed` DAG in Airflow.
3.  **Run Pipeline**: Trigger the `integrated_pipeline` DAG.