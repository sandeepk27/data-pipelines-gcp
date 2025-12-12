resource "google_sql_database_instance" "instance" {
  name             = var.instance_name
  database_version = var.database_version
  region           = var.region

  settings {
    tier = var.tier
  }

  deletion_protection  = false # For practice environment
}

resource "google_sql_database" "database" {
  name     = var.database_name
  instance = google_sql_database_instance.instance.name
}

resource "google_sql_user" "users" {
  name     = var.user_name
  instance = google_sql_database_instance.instance.name
  password = var.user_password
}
