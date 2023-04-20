from airflow.providers.mysql.hooks.mysql import MySqlHook

def cargar_paso(id, ti=None):
    paso = ti.xcom_pull(task_ids=id)
    print(paso)
    
    hook = MySqlHook(mysql_conn_id='mysql_pasos')
    with hook.get_conn() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                DELETE FROM pasos_fronterizos WHERE fecha_scaneo = %s AND paso = %s;""", [paso['fecha_scaneo'], paso['paso']])
            
            if paso['tipo_de_paso'] == 'Ruta':
                cursor.execute("""
                    INSERT INTO 
                        pasos_fronterizos(paso, pais, provincia, estado, tipo, fecha_scaneo, ultima_actualizacion, temperatura, tiempo, viento, visibilidad)
                    VALUES
                        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);""", 
                        [paso['paso'], paso['pais'], paso['provincia'], paso['estado'], paso['tipo_de_paso'],
                        paso['fecha_scaneo'], paso['ultima_actualizacion'],
                        paso['temperatura'], paso['tiempo'], paso['viento'], paso['visibilidad']])
            elif paso['tipo_de_paso'] == 'Rio':
                cursor.execute("""
                    INSERT INTO 
                        pasos_fronterizos(paso, pais, provincia, estado, tipo, fecha_scaneo, ultima_actualizacion, altura_del_rio, alerta_del_rio, evacuacion_del_rio)
                    VALUES
                        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);""", 
                        [paso['paso'], paso['pais'], paso['provincia'], paso['estado'], paso['tipo_de_paso'],
                        paso['fecha_scaneo'], paso['ultima_actualizacion'],
                        paso['altura_del_río'], paso['alerta'], paso['evacuación']])
        conn.commit()