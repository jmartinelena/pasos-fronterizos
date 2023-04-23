CREATE TABLE IF NOT EXISTS pasos(
	pasos_id INT PRIMARY KEY AUTO_INCREMENT,
    fecha_id INT,
    locacion_id INT,
    tipo_id INT UNIQUE,
    estado VARCHAR(20) NOT NULL,
    UNIQUE(fecha_id, locacion_id)
    );