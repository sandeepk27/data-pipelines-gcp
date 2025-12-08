resource "google_storage_bucket" "bucket" {
  name          = var.bucket_name
  location      = var.location
  force_destroy = var.force_destroy
  storage_class = var.storage_class

  uniform_bucket_level_access = true

  versioning {
    enabled = var.versioning_enabled
  }

  labels = var.labels
}
