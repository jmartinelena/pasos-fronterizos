from airflow.providers.mysql.hooks.mysql import MySqlHook

def agregar_fk_pasos():
    hook = MySqlHook(mysql_conn_id='mysql_pasos')
    with hook.get_conn() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""DROP PROCEDURE IF EXISTS add_constraint;""")

            cursor.execute("""
                            CREATE PROCEDURE add_constraint()
                            BEGIN
                                IF NOT EXISTS (
                                    SELECT NULL 
                                    FROM information_schema.TABLE_CONSTRAINTS
                                    WHERE
                                        CONSTRAINT_SCHEMA = 'pasos_fronterizos' AND
                                        CONSTRAINT_NAME   = 'pasos_ibfk_1' AND
                                        CONSTRAINT_TYPE   = 'FOREIGN KEY'
                                )
                                THEN
                                    ALTER TABLE pasos ADD CONSTRAINT pasos_ibfk_1 FOREIGN KEY (tipo_id) REFERENCES tipo(tipo_id);
                                END IF;
                            END""")
            
            cursor.execute("""CALL add_constraint();""")
        conn.commit()
