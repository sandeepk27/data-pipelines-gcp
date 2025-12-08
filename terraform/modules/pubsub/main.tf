resource "google_pubsub_topic" "topic" {
  name = var.topic_name
  labels = var.labels
}

resource "google_pubsub_subscription" "subscription" {
  name  = var.subscription_name
  topic = google_pubsub_topic.topic.name

  ack_deadline_seconds = 20

  labels = var.labels
}
