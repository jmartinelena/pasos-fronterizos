from airflow.providers.mysql.hooks.mysql import MySqlHook

def cargar_paso(id, ti=None):
    """Función que carga la información obtenida por el paso previo de scrapeo.
        parámetro id: string que referencia al task anterior de scrapeo.
        parámetro ti: task instance para utilizar XCom."""
    paso = ti.xcom_pull(task_ids=id)
    print(paso)
    
    hook = MySqlHook(mysql_conn_id='mysql_pasos')
    with hook.get_conn() as conn:
        with conn.cursor() as cursor: 
            if paso['tipo_de_paso'] == 'Ruta':
                cursor.execute("""CALL upsert_data(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NULL, NULL, NULL);""", 
                               [paso['fecha_scaneo'], paso['ultima_actualizacion'], paso['paso'], paso['pais'], 
                                paso['provincia'], paso['estado'], paso['tipo_de_paso'], 
                                paso['temperatura'], paso['tiempo'], paso['viento'], paso['visibilidad']])
            elif paso['tipo_de_paso'] == 'Rio':
                cursor.execute("""CALL upsert_data(%s, %s, %s, %s, %s, %s, %s, NULL, NULL, NULL, NULL, %s, %s, %s);""", 
                               [paso['fecha_scaneo'], paso['ultima_actualizacion'], paso['paso'], paso['pais'], 
                                paso['provincia'], paso['estado'], paso['tipo_de_paso'], 
                                paso['altura_del_río'], paso['alerta'], paso['evacuación']])
        conn.commit()