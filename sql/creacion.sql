CREATE TABLE clientes_ser (
 id_cliente INT NOT NULL AUTO_INCREMENT,
 nombre VARCHAR(80) NOT NULL,
 telefono VARCHAR(20) NOT NULL,
 email VARCHAR(120) NOT NULL,
 direccion VARCHAR(150) DEFAULT NULL,
 fecha_registro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
 PRIMARY KEY (id_cliente), UNIQUE KEY email (email),
 CONSTRAINT chk_cliente_nombre CHECK (CHAR_LENGTH(TRIM(nombre)) >= 3)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE tecnicos_ser (
 id_tecnico INT NOT NULL AUTO_INCREMENT,
 nombre VARCHAR(80) NOT NULL,
 especialidad VARCHAR(80) NOT NULL,
 telefono VARCHAR(20) DEFAULT NULL,
 activo TINYINT(1) NOT NULL DEFAULT 1,
 PRIMARY KEY (id_tecnico),
 CONSTRAINT chk_tecnico_nombre CHECK (CHAR_LENGTH(TRIM(nombre)) >= 3)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE equipos_ser (
 id_equipo INT NOT NULL AUTO_INCREMENT,
 id_cliente INT NOT NULL,
 tipo VARCHAR(50) NOT NULL,
 marca VARCHAR(50) NOT NULL,
 modelo VARCHAR(80) NOT NULL,
 numero_serie VARCHAR(80) NOT NULL,
 estado VARCHAR(30) NOT NULL DEFAULT 'Ingresado',
 fecha_ingreso DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
 PRIMARY KEY (id_equipo), UNIQUE KEY numero_serie (numero_serie), KEY fk_equipo_cliente (id_cliente),
 CONSTRAINT fk_equipo_cliente FOREIGN KEY (id_cliente) REFERENCES clientes_ser(id_cliente) ON DELETE RESTRICT ON UPDATE CASCADE,
 CONSTRAINT chk_equipo_estado CHECK (estado IN ('Ingresado','En diagnóstico','En reparación','Listo','Entregado'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE ordenes_servicio_ser (
 id_orden INT NOT NULL AUTO_INCREMENT,
 id_equipo INT NOT NULL,
 id_tecnico INT DEFAULT NULL,
 fecha_recepcion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
 fecha_entrega DATETIME DEFAULT NULL,
 diagnostico VARCHAR(255) DEFAULT NULL,
 descripcion_falla VARCHAR(255) NOT NULL,
 estado VARCHAR(30) NOT NULL DEFAULT 'Ingresada',
 costo_mano_obra DECIMAL(10,2) NOT NULL DEFAULT 0.00,
 PRIMARY KEY (id_orden), KEY fk_orden_equipo (id_equipo), KEY fk_orden_tecnico (id_tecnico),
 CONSTRAINT fk_orden_equipo FOREIGN KEY (id_equipo) REFERENCES equipos_ser(id_equipo) ON DELETE RESTRICT ON UPDATE CASCADE,
 CONSTRAINT fk_orden_tecnico FOREIGN KEY (id_tecnico) REFERENCES tecnicos_ser(id_tecnico) ON DELETE SET NULL ON UPDATE CASCADE,
 CONSTRAINT chk_orden_estado CHECK (estado IN ('Ingresada','En diagnóstico','En reparación','Lista','Entregada','Cancelada')),
 CONSTRAINT chk_orden_fechas CHECK (fecha_entrega IS NULL OR fecha_entrega >= fecha_recepcion),
 CONSTRAINT chk_orden_mano_obra CHECK (costo_mano_obra >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE repuestos_ser (
 id_repuesto INT NOT NULL AUTO_INCREMENT,
 nombre VARCHAR(100) NOT NULL,
 stock INT NOT NULL DEFAULT 0,
 precio DECIMAL(10,2) NOT NULL DEFAULT 0.00,
 PRIMARY KEY (id_repuesto), UNIQUE KEY nombre (nombre),
 CONSTRAINT chk_repuesto_precio CHECK (precio >= 0), CONSTRAINT chk_repuesto_stock CHECK (stock >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE detalle_orden_ser (
 id_detalle INT NOT NULL AUTO_INCREMENT,
 id_orden INT NOT NULL,
 id_repuesto INT NOT NULL,
 cantidad INT NOT NULL,
 precio_unitario DECIMAL(10,2) NOT NULL,
 PRIMARY KEY (id_detalle), UNIQUE KEY uq_detalle_orden_repuesto (id_orden,id_repuesto), KEY fk_detalle_repuesto (id_repuesto),
 CONSTRAINT fk_detalle_orden FOREIGN KEY (id_orden) REFERENCES ordenes_servicio_ser(id_orden) ON DELETE CASCADE ON UPDATE CASCADE,
 CONSTRAINT fk_detalle_repuesto FOREIGN KEY (id_repuesto) REFERENCES repuestos_ser(id_repuesto) ON DELETE RESTRICT ON UPDATE CASCADE,
 CONSTRAINT chk_detalle_cantidad CHECK (cantidad > 0), CONSTRAINT chk_detalle_precio CHECK (precio_unitario >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
