from airflow.providers.mysql.hooks.mysql import MySqlHook

def agregar_sp_upsert():
    hook = MySqlHook(mysql_conn_id='mysql_pasos')
    with hook.get_conn() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""DROP PROCEDURE IF EXISTS upsert_data;""")

            cursor.execute("""
                            CREATE PROCEDURE upsert_data(
								IN fechaScaneo DATETIME, IN ultimaActualizacion DATETIME, IN nombrePaso VARCHAR(100), 
                                IN paisLimitrofe VARCHAR(20), IN provinciaPaso VARCHAR(20), IN estadoPaso VARCHAR(20),
    							IN tipoPaso VARCHAR(20), IN temperaturaPaso DECIMAL(5,2), IN tiempoPaso VARCHAR(100), 
                                IN vientoPaso VARCHAR(100), IN visibilidadPaso VARCHAR(100),
    							IN alturaRio DECIMAL(5,2), IN alertaRio DECIMAL(5,2), IN evacuacionRio DECIMAL(5,2))
							BEGIN
								DECLARE fechaId INT;
							    DECLARE locacionId INT;
							    DECLARE tipoId INT;

								INSERT INTO 
									fecha(fecha_scaneo, ultima_actualizacion)
								VALUES 
									(fechaScaneo, ultimaActualizacion)
								ON DUPLICATE KEY UPDATE
									ultima_actualizacion = ultimaActualizacion;

								INSERT IGNORE INTO
									locacion(nombre_paso, provincia, pais_limitrofe)
								VALUES
									(nombrePaso, provinciaPaso, paisLimitrofe);

								SELECT fecha_id INTO fechaId FROM fecha 
                                	WHERE fecha_scaneo = fechaScaneo AND ultima_actualizacion = ultimaActualizacion;
								SELECT locacion_id INTO locacionId FROM locacion WHERE nombre_paso = nombrePaso;

								INSERT INTO
									tipo(fecha_id, locacion_id, tipo, temperatura, tiempo, viento, visibilidad, 
                                    altura_del_rio, alerta_del_rio, evacuacion_del_rio)
								VALUES
									(fechaId, locacionId, tipoPaso, temperaturaPaso, tiempoPaso, vientoPaso, visibilidadPaso, 
                                    alturaRio, alertaRio, evacuacionRio)
								ON DUPLICATE KEY UPDATE
									tipo = tipoPaso, temperatura = temperaturaPaso, tiempo = tiempoPaso, viento = vientoPaso, 
                                    visibilidad = visibilidadPaso,
							        altura_del_rio = alturaRio, alerta_del_rio = alertaRio, evacuacion_del_rio = evacuacionRio;

								SELECT tipo_id INTO tipoId FROM tipo WHERE locacion_id = locacionId AND fecha_id = fechaId;

								INSERT INTO 
									pasos(fecha_id, locacion_id, tipo_id, estado)
								VALUES
									(fechaId, locacionId, tipoId, estadoPaso)
								ON DUPLICATE KEY UPDATE
									estado = estadoPaso;
							END""")
        conn.commit()