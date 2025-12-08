# Terraform Infrastructure for Data Pipelines

This directory contains Terraform code to provision the basic infrastructure for data pipelines on GCP.

## Resources Created

- **Google Cloud Storage (GCS)**:
    - `<project_id>-dataproc-staging`: Staging bucket for Dataproc.
    - `<project_id>-dataflow-staging`: Staging bucket for Dataflow.
    - `<project_id>-dataflow-temp`: Temp bucket for Dataflow.
    - `<project_id>-raw-data`: Bucket for storing raw data.
- **BigQuery**:
    - `data_warehouse` dataset.
- **Dataproc**:
    - A Spark cluster named `spark-cluster-<environment>`.

## Prerequisites

1.  [Install Terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli).
2.  [Install Google Cloud SDK](https://cloud.google.com/sdk/docs/install).
3.  Authenticate with GCP:
    ```bash
    gcloud auth application-default login
    ```

## Usage

1.  Initialize Terraform:
    ```bash
    terraform init
    ```

2.  Plan the deployment:
    ```bash
    terraform plan -var="project_id=YOUR_PROJECT_ID"
    ```

3.  Apply the changes:
    ```bash
    terraform apply -var="project_id=YOUR_PROJECT_ID"
    ```

## Modules

- `modules/gcs`: Generic module for creating GCS buckets.
- `modules/bigquery`: Generic module for creating BigQuery datasets.
- `modules/dataproc`: Generic module for creating Dataproc clusters.
