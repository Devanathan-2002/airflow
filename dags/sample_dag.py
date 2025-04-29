from airflow import DAG
from airflow.operators.python import PythonOperator
import pytz
from datetime import datetime
import os

def write_file():
    desktop_path = '/workspaces/airflow/temp/'
    filename = os.path.join(desktop_path, 'airflow_output.txt')
    in_timezn=pytz.timezone("Asia/Kolkata")
    current_time = datetime.now(in_timezn).strftime("%Y-%m-%d %H:%M:%S")
    with open(filename, 'a') as f:
        f.write(f"Hello from Airflow at {current_time}\n")

default_args = {
    'start_date': datetime(2024, 4, 28),
}

with DAG(
    dag_id='sample_dag_1',
    default_args=default_args,
    schedule_interval='* * * * *', 
    catchup=False
) as dag:
    
    task1 = PythonOperator(
        task_id='write_file_task',
        python_callable=write_file
    )

task1
