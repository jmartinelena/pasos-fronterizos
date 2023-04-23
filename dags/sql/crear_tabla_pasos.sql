CREATE TABLE IF NOT EXISTS pasos(
	pasos_id INT PRIMARY KEY AUTO_INCREMENT,
    fecha_id INT UNIQUE,
    locacion_id INT UNIQUE,
    tipo_id INT UNIQUE,
    estado VARCHAR(20) NOT NULL
    );