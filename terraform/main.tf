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

resource "google_project_service" "sqladmin_api" {
  service            = "sqladmin.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "datafusion_api" {
  service            = "datafusion.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "dataform_api" {
  service            = "dataform.googleapis.com"
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

resource "google_storage_bucket_object" "complex_spark_script" {
  name   = "scripts/complex_spark_transform.py"
  source = "../dags/scripts/complex_spark_transform.py"
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

// Cloud SQL for Transactional Data
module "cloudsql" {
  source           = "./modules/cloudsql"
  instance_name    = "${var.project_id}-sql-instance"
  database_version = "POSTGRES_14"
  region           = var.region
  database_name    = "ecommerce_db"
  user_name        = "admin"
  user_password    = "secretpassword123" # In production, use Secret Manager
}

// Cloud SQL Instance (PostgreSQL)
module "cloudsql_instance" {
  source           = "./modules/cloudsql"
  instance_name    = "ecommerce-db-${var.environment}"
  region           = var.region
  database_version = "POSTGRES_14"
  database_name    = "ecommerce"
  user_name        = "admin"
  user_password    = "SuperSecretPassword123!" # In real life, use Secret Manager

  depends_on = [google_project_service.sqladmin_api]
}

// Data Fusion Instance
resource "google_data_fusion_instance" "basic_instance" {
  name    = "data-fusion-${var.environment}"
  region  = var.region
  type    = "BASIC"
  version = "6.9.1" # Example version

  depends_on = [google_project_service.datafusion_api]
}

// Dataform Repository
resource "google_dataform_repository" "dataform_repo" {
  provider = google-beta
  name     = "ecommerce-data-models"
  region   = var.region

  git_remote_settings {
      url = "https://github.com/my-org/my-repo.git" # Placeholder
      default_branch = "main"
      authentication_token_secret_version = "projects/${var.project_id}/secrets/github-token/versions/1" # Placeholder
  }

  depends_on = [google_project_service.dataform_api]
}

// BigQuery Data Transfer Config (Google Trends - Example)
// Note: This requires manually enabling the transfer service in UI first usually.
resource "google_bigquery_data_transfer_config" "trends_transfer" {
  display_name           = "Google Trends Transfer"
  location               = "US"
  data_source_id         = "google_trends"
  schedule               = "every 24 hours"
  destination_dataset_id = module.data_warehouse.dataset_id
  params = {
    # Parameters vary by data source
  }
  disabled = true # Disabled to prevent accidental costs/errors without valid params
}
