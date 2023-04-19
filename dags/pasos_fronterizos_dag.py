from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.mysql.operators.mysql import MySqlOperator

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
    creacion_tabla = MySqlOperator(
        task_id = 'creacion_tabla',
        mysql_conn_id = 'mysql_pasos',
        sql = """
            CREATE TABLE IF NOT EXISTS pasos_fronterizos(
                id INT AUTO_INCREMENT PRIMARY KEY,
                paso VARCHAR(100) NOT NULL,
                pais VARCHAR(20) NOT NULL,
                provincia VARCHAR(20) NOT NULL,
                estado VARCHAR(20) NOT NULL,
                tipo VARCHAR(20) NOT NULL,
                temperatura INT,
                tiempo VARCHAR(100),
                viento VARCHAR(100),
                visibilidad VARCHAR(100),
                altura_del_rio INT,
                alerta_del_rio INT,
                evacuacion_del_rio INT
            );"""
    )