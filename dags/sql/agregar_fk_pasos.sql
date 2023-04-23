DROP PROCEDURE IF EXISTS add_constraint;

DELIMITER $$
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
END$$
DELIMITER ;

CALL add_constraint();