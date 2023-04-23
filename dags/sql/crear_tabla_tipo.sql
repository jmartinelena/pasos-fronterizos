CREATE TABLE IF NOT EXISTS tipo(
	tipo_id INT AUTO_INCREMENT PRIMARY KEY,
    fecha_id INT UNIQUE,
    locacion_id INT UNIQUE,
    tipo VARCHAR(20),
    temperatura DECIMAL(5,2),
    tiempo VARCHAR(100),
	viento VARCHAR(100),
	visibilidad VARCHAR(100),
	altura_del_rio DECIMAL(5,2),
	alerta_del_rio DECIMAL(5,2),
	evacuacion_del_rio DECIMAL(5,2),
    FOREIGN KEY(fecha_id) REFERENCES fecha(fecha_id),
    FOREIGN KEY(locacion_id) REFERENCES locacion(locacion_id));
    
ALTER TABLE pasos ADD CONSTRAINT FOREIGN KEY(tipo_id) REFERENCES tipo(tipo_id);