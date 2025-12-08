import time
import json
import random
import datetime
from google.cloud import pubsub_v1
import argparse

def publish_messages(project_id, topic_name):
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_name)

    print(f"Publishing messages to {topic_path}...")

    names = ["Alice", "Bob", "Charlie", "Diana", "Eve"]

    for i in range(100):
        data = {
            "id": i,
            "name": random.choice(names),
            "timestamp": datetime.datetime.now().isoformat()
        }
        data_str = json.dumps(data)
        data_bytes = data_str.encode("utf-8")

        try:
            publish_future = publisher.publish(topic_path, data=data_bytes)
            publish_future.result()  # Verify the publish succeeded
            print(f"Published message: {data_str}")
        except Exception as e:
            print(f"An error occurred: {e}")

        time.sleep(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Publish dummy data to Pub/Sub")
    parser.add_argument("--project_id", required=True, help="GCP Project ID")
    parser.add_argument("--topic_name", required=True, help="Pub/Sub Topic Name")
    args = parser.parse_args()

    publish_messages(args.project_id, args.topic_name)
