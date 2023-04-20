from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.mysql.operators.mysql import MySqlOperator

from scrape_paso import scrape_paso
from cargar_paso import cargar_paso

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
    render_template_as_native_obj=True
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
                fecha_scaneo DATETIME NOT NULL,
                ultima_actualizacion DATETIME NOT NULL,
                temperatura DECIMAL(5,2),
                tiempo VARCHAR(100),
                viento VARCHAR(100),
                visibilidad VARCHAR(100),
                altura_del_rio DECIMAL(5,2),
                alerta_del_rio DECIMAL(5,2),
                evacuacion_del_rio DECIMAL(5,2)
            );"""
    )

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

        creacion_tabla >> scrapear_paso >> carga_paso