output "dataproc_cluster_name" {
  value = module.dataproc_cluster.cluster_name
}

output "bigquery_dataset_id" {
  value = module.data_warehouse.dataset_id
}

output "raw_data_bucket_url" {
  value = module.raw_data_bucket.bucket_url
}

output "pubsub_topic" {
  value = module.pubsub_streaming.topic_name
}

output "pubsub_subscription" {
  value = module.pubsub_streaming.subscription_name
}
