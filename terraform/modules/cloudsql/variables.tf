variable "instance_name" {
  description = "Name of the Cloud SQL instance"
  type        = string
}

variable "database_version" {
  description = "Database version (e.g. POSTGRES_14)"
  type        = string
  default     = "POSTGRES_14"
}

variable "region" {
  description = "Region for the instance"
  type        = string
  default     = "us-central1"
}

variable "tier" {
  description = "Machine tier (e.g. db-f1-micro)"
  type        = string
  default     = "db-f1-micro"
}

variable "database_name" {
  description = "Name of the database to create"
  type        = string
  default     = "ecommerce_db"
}

variable "user_name" {
  description = "Database user name"
  type        = string
  default     = "admin"
}

variable "user_password" {
  description = "Database user password"
  type        = string
}
