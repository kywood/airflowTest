from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
import time

def print_numbers():
    count = 0
    while True:
        print(f"현재 숫자: {count}")
        count += 1
        time.sleep(1)

default_args = {
    'start_date': datetime(2024, 1, 1),
    'catchup': False
}

with DAG(
    dag_id='infinite_print_numbers',
    default_args=default_args,
    schedule_interval='@once',  # 한 번만 실행
    tags=['demo'],
    catchup=False
) as dag:

    infinite_task = PythonOperator(
        task_id='print_forever',
        python_callable=print_numbers,
    )
