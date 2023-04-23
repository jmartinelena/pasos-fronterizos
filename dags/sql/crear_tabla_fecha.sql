CREATE TABLE IF NOT EXISTS fecha(
	fecha_id INT PRIMARY KEY AUTO_INCREMENT,
    fecha_scaneo DATETIME UNIQUE NOT NULL,
    ultima_actualizacion DATETIME NOT NULL
    );