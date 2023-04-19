from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'Juan Martin Elena',
    'retries': 5,
    'retry_delay': timedelta(seconds=30)
}

with DAG(
    dag_id = 'pasos_fronterizos',
    description='DAG que scanea el estado de los 10 pasos fronterizos argentinos mas concurridos.',
    default_args = default_args,
    catchup=False,
    start_date=datetime(2023,4,19),
    schedule='@hourly'
) as dag:
    pass