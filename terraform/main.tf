// Enable necessary APIs
resource "google_project_service" "dataproc_api" {
  service            = "dataproc.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "dataflow_api" {
  service            = "dataflow.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "bigquery_api" {
  service            = "bigquery.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "pubsub_api" {
  service            = "pubsub.googleapis.com"
  disable_on_destroy = false
}

// GCS Buckets
module "dataproc_staging_bucket" {
  source      = "./modules/gcs"
  bucket_name = "${var.project_id}-dataproc-staging"
  location    = var.region
}

module "dataflow_staging_bucket" {
  source      = "./modules/gcs"
  bucket_name = "${var.project_id}-dataflow-staging"
  location    = var.region
}

module "dataflow_temp_bucket" {
  source      = "./modules/gcs"
  bucket_name = "${var.project_id}-dataflow-temp"
  location    = var.region
}

module "raw_data_bucket" {
  source      = "./modules/gcs"
  bucket_name = "${var.project_id}-raw-data"
  location    = var.region
}

// BigQuery Dataset
module "data_warehouse" {
  source        = "./modules/bigquery"
  dataset_id    = "data_warehouse"
  friendly_name = "Data Warehouse"
  description   = "Central data warehouse for processed data"
  location      = var.region

  depends_on = [google_project_service.bigquery_api]
}

// Dataproc Cluster (Spark)
module "dataproc_cluster" {
  source         = "./modules/dataproc"
  cluster_name   = "spark-cluster-${var.environment}"
  region         = var.region
  staging_bucket = module.dataproc_staging_bucket.bucket_name

  master_machine_type = "n1-standard-2"
  worker_machine_type = "n1-standard-2"
  worker_num_instances = 2

  depends_on = [
    google_project_service.dataproc_api,
    module.dataproc_staging_bucket
  ]
}

// Upload PySpark script to Dataproc Staging Bucket
resource "google_storage_bucket_object" "pyspark_script" {
  name   = "scripts/process_data.py"
  source = "../dags/scripts/process_data.py"
  bucket = module.dataproc_staging_bucket.bucket_name

  depends_on = [module.dataproc_staging_bucket]
}

// Pub/Sub for Streaming
module "pubsub_streaming" {
  source            = "./modules/pubsub"
  topic_name        = "streaming-data-topic"
  subscription_name = "streaming-data-sub"

  depends_on = [google_project_service.pubsub_api]
}
