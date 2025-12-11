import os
import argparse
import sqlalchemy
from google.cloud import bigquery
import pandas as pd

def seed_database(project_id, db_user, db_pass, db_name, db_host, limit=1000):
    """
    Reads data from BigQuery public dataset and writes to Cloud SQL.
    """

    # 1. Read from BigQuery
    bq_client = bigquery.Client(project=project_id)
    query = f"""
        SELECT
            order_id, user_id, status, gender, created_at, returned_at, shipped_at, delivered_at, num_of_item
        FROM
            `bigquery-public-data.thelook_ecommerce.orders`
        LIMIT {limit}
    """
    print("Querying BigQuery...")
    df = bq_client.query(query).to_dataframe()
    print(f"Fetched {len(df)} rows.")

    # 2. Write to Cloud SQL (PostgreSQL)
    # connection string format: postgresql+pg8000://<user>:<password>@<public_ip>/<dbname>
    # Note: For production, use Cloud SQL Proxy or Private IP.

    db_uri = f"postgresql+pg8000://{db_user}:{db_pass}@{db_host}/{db_name}"
    engine = sqlalchemy.create_engine(db_uri)

    print("Writing to Cloud SQL...")
    try:
        df.to_sql('orders', engine, if_exists='replace', index=False)
        print("Successfully seeded 'orders' table.")
    except Exception as e:
        print(f"Error writing to DB: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--project_id", required=True)
    parser.add_argument("--db_user", required=True)
    parser.add_argument("--db_pass", required=True)
    parser.add_argument("--db_name", required=True)
    parser.add_argument("--db_host", required=True)

    args = parser.parse_args()

    seed_database(args.project_id, args.db_user, args.db_pass, args.db_name, args.db_host)
