from datetime import datetime, timedelta

from airflow import DAG
from airflow.utils.task_group import TaskGroup
from airflow.operators.python import PythonOperator
from airflow.providers.mysql.operators.mysql import MySqlOperator

from scrape_paso import scrape_paso
from cargar_paso import cargar_paso
from crear_sp_add_constraint import agregar_fk_pasos
from crear_sp_upsert import agregar_sp_upsert

default_args = {
    'owner': 'Juan Martín Elena',
    'retries': 5,
    'retry_delay': timedelta(seconds=30)
}

with DAG(
    dag_id = 'pasos_fronterizos',
    description='DAG que scanea el estado de los 10 pasos fronterizos argentinos mas concurridos.',
    default_args = default_args,
    catchup=False,
    start_date=datetime(2023,4,19),
    schedule='@hourly',
    render_template_as_native_obj=True,
) as dag:
    with TaskGroup(group_id='preparar_db') as preparar_db:
        crear_tabla_pasos = MySqlOperator(
            task_id = 'crear_tabla_pasos',
            mysql_conn_id= 'mysql_pasos',
            sql = "/sql/crear_tabla_pasos.sql"
        )

        crear_tabla_fecha = MySqlOperator(
            task_id = "crear_tabla_fecha",
            mysql_conn_id= 'mysql_pasos',
            sql = "/sql/crear_tabla_fecha.sql"
        )

        crear_tabla_locacion = MySqlOperator(
            task_id = 'crear_tabla_locacion',
            mysql_conn_id= 'mysql_pasos',
            sql = '/sql/crear_tabla_locacion.sql'
        )

        crear_tabla_tipo = MySqlOperator(
            task_id = 'crear_tabla_tipo',
            mysql_conn_id= 'mysql_pasos',
            sql = '/sql/crear_tabla_tipo.sql'
        )

        crear_fk_pasos = PythonOperator(
            task_id = 'agregar_fk_pasos',
            python_callable= agregar_fk_pasos
        )

        crear_sp_upsert = PythonOperator(
            task_id = 'crear_sp_upsert',
            python_callable= agregar_sp_upsert
        )
        
        [crear_tabla_pasos, crear_tabla_fecha, crear_tabla_locacion] >> crear_tabla_tipo >> crear_fk_pasos >> crear_sp_upsert

    urls = ["https://www.argentina.gob.ar/seguridad/pasosinternacionales/detalle/ruta/22/Salvador-Mazza-Yacuiba",
            "https://www.argentina.gob.ar/seguridad/pasosinternacionales/detalle/ruta/24/Puerto-Chalanas-Bermejo",
            "https://www.argentina.gob.ar/seguridad/pasosinternacionales/detalle/ruta/4/Gualeguaych%C3%BA-Fray-Bentos",
            "https://www.argentina.gob.ar/seguridad/pasosinternacionales/detalle/ruta/18/La-Quiaca-Villaz%C3%B3n",
            "https://www.argentina.gob.ar/seguridad/pasosinternacionales/detalle/ruta/23/Aguas-Blancas-Bermejo",
            "https://www.argentina.gob.ar/seguridad/pasosinternacionales/detalle/ruta/12/Bernardo-de-Irigoyen-Dionisio-Cerqueira",
            "https://www.argentina.gob.ar/seguridad/pasosinternacionales/detalle/ruta/29/Sistema-Cristo-Redentor",
            "https://www.argentina.gob.ar/seguridad/pasosinternacionales/detalle/ruta/73/Paso-de-los-Libres-Uruguayana",
            "https://www.argentina.gob.ar/seguridad/pasosinternacionales/detalle/ruta/42/Cardenal-Antonio-Samor%C3%A9",
            "https://www.argentina.gob.ar/seguridad/pasosinternacionales/detalle/rio/82/Puerto-Colon-Puerto-Paysandu"]
    
    timestamp = "{{ ts }}"
    for i in range(len(urls)):
        # Scrapea y carga la información de cada una de las urls.
        scrapear_paso = PythonOperator(
            task_id=f"scrapeo_paso_{i}",
            python_callable= scrape_paso,
            op_args=(urls[i], timestamp),
        )

        carga_paso = PythonOperator(
            task_id = f"cargar_paso_{i}",
            python_callable=cargar_paso,
            op_args=[f"scrapeo_paso_{i}"]
        )

        preparar_db >> scrapear_paso >> carga_paso