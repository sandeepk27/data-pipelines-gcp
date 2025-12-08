variable "cluster_name" {
  description = "The name of the Dataproc cluster"
  type        = string
}

variable "region" {
  description = "The region to create the cluster in"
  type        = string
}

variable "staging_bucket" {
  description = "The Cloud Storage bucket used for staging by Dataproc"
  type        = string
}

variable "master_num_instances" {
  description = "Number of master nodes"
  type        = number
  default     = 1
}

variable "master_machine_type" {
  description = "Machine type for master nodes"
  type        = string
  default     = "n1-standard-2"
}

variable "master_boot_disk_size_gb" {
  description = "Size of boot disk for master nodes"
  type        = number
  default     = 50
}

variable "worker_num_instances" {
  description = "Number of worker nodes"
  type        = number
  default     = 2
}

variable "worker_machine_type" {
  description = "Machine type for worker nodes"
  type        = string
  default     = "n1-standard-2"
}

variable "worker_boot_disk_size_gb" {
  description = "Size of boot disk for worker nodes"
  type        = number
  default     = 50
}

variable "image_version" {
  description = "The Cloud Dataproc image version to use"
  type        = string
  default     = "2.0-debian10"
}
