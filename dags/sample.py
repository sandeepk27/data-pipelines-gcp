from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime
import logging

default_args = {
    'start_date': datetime(2024, 1, 1),
    'retries': 1
}

with DAG('test-dag',
         schedule_interval='@daily',
         catchup=False,
         default_args=default_args,
         tags=['github', 'example']) as dag:

    task = BashOperator(
        task_id='print_hello',
        bash_command='echo Hello from GitHub DAG!'
    )
