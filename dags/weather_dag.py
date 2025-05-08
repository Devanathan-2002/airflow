from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime,timedelta

default_args = {
    'owner':'airflow',
    'retries':1,
    'retry_delay':2,
    'start_date': datetime(2025, 5, 8),
}


with DAG(
    dag_id='weather_dag',
    default_args=default_args,
    schedule_interval='*/5 * * * *',
    catchup=False
) as dag:
    
    task1=BashOperator(task_id='weather_dag_1',bash_command='bash /workspaces/airflow/dags/wrapper.sh ')


    task1