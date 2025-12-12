from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 0,
}

with DAG(
    dag_id='init_infra_seed',
    default_args=default_args,
    schedule_interval='@once',
    catchup=False,
    tags=['setup', 'cloudsql'],
) as dag:

    # In a real environment, fetch these from Secrets Manager or Terraform outputs
    PROJECT_ID = '{{ var.value.gcp_project_id }}'
    DB_USER = 'admin'
    DB_PASS = 'SuperSecretPassword123!'
    DB_NAME = 'ecommerce'
    # DB_HOST needs to be set manually after Terraform apply provides the IP
    DB_HOST = '{{ var.value.cloudsql_public_ip }}'

    seed_task = BashOperator(
        task_id='seed_database',
        bash_command=f"""
        pip install sqlalchemy pg8000 pandas google-cloud-bigquery && \
        python dags/scripts/seed_cloudsql.py \
            --project_id {PROJECT_ID} \
            --db_user {DB_USER} \
            --db_pass {DB_PASS} \
            --db_name {DB_NAME} \
            --db_host {DB_HOST}
        """
    )
