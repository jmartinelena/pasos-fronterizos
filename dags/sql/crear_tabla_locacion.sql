CREATE TABLE IF NOT EXISTS locacion(
	locacion_id INT PRIMARY KEY AUTO_INCREMENT,
    nombre_paso VARCHAR(100) UNIQUE NOT NULL,
    provincia VARCHAR(20) NOT NULL,
    pais_limitrofe VARCHAR(20) NOT NULL
    );