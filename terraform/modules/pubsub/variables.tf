variable "topic_name" {
  description = "The name of the Pub/Sub topic"
  type        = string
}

variable "subscription_name" {
  description = "The name of the Pub/Sub subscription"
  type        = string
}

variable "labels" {
  description = "A set of key/value label pairs to assign to the resources"
  type        = map(string)
  default     = {}
}
