variable "dataset_id" {
  description = "The ID of the dataset"
  type        = string
}

variable "friendly_name" {
  description = "A descriptive name for the dataset"
  type        = string
  default     = null
}

variable "description" {
  description = "A user-friendly description of the dataset"
  type        = string
  default     = null
}

variable "location" {
  description = "The regional location for the dataset"
  type        = string
  default     = "US"
}

variable "default_table_expiration_ms" {
  description = "The default lifetime of all tables in the dataset, in milliseconds"
  type        = number
  default     = null
}

variable "labels" {
  description = "A set of key/value label pairs to assign to the dataset"
  type        = map(string)
  default     = {}
}

variable "delete_contents_on_destroy" {
  description = "If set to true, delete all the tables in the dataset when destroying the resource"
  type        = bool
  default     = false
}
