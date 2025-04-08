import airflow
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
import pandas as pd
import requests
import configparser

# defining congiguration variables
configparser = configparser.ConfigParser()
configparser.read('data-pipelines-gcp/config/param.ini')
config = configparser['DEFAULT']
sql_path = config.get('sql_file_path')

# Define the default arguments for the DAG
default_args = {
    'start_date': datetime(2025, 4, 8),
    'retries': 1,
    'active_run': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG('test-dag',
         schedule_interval='@daily',
         catchup=False,
         default_args=default_args,
         tags=['test', 'spotify']) as dag:

    task = BashOperator(
        task_id='print_hello',
        bash_command='bq query --use_legacy_sql=false < sql/test.sql'
    )