INSERT INTO clientes_ser (nombre,telefono,email,direccion,fecha_registro) VALUES
('Camila Rojas','912345678','camila.rojas@gmail.com','Av. Central 120','2026-09-07 12:08:11'),
('Diego Muñoz','923456781','diego.munoz@example.com','Pasaje Norte 45','2026-09-07 12:08:11'),
('Valentina Soto','934567812','valentina.soto@example.com','Los Alerces 88','2026-09-07 12:08:11'),
('Matías Pérez','945678123','matias.perez@example.com','Las Flores 210','2026-09-07 12:08:11'),
('Sofía González','956781234','sofia.gonzalez@example.com','El Molino 32','2026-09-07 12:08:11');
INSERT INTO tecnicos_ser (nombre,especialidad,telefono) VALUES
('Nicolás Fuentes','Notebooks y PC','967111222'),('Fernanda Silva','Telefonía móvil','968222333'),('Tomás Herrera','Consolas','969333444');
INSERT INTO equipos_ser (id_cliente,tipo,marca,modelo,numero_serie,estado) VALUES
(1,'Notebook','Lenovo','IdeaPad 3','SN-LEN-1001','En diagnóstico'),
(2,'Celular','Samsung','Galaxy A54','SN-SAM-1002','Ingresado'),
(3,'Notebook','HP','15-DY','SN-HP-1003','En reparación'),
(4,'Consola','Sony','PlayStation 5','SN-SON-1004','Ingresado'),
(5,'Notebook','Acer','Aspire 5','SN-ACE-1005','Reparado');
INSERT INTO repuestos_ser (nombre,stock,precio) VALUES
('SSD 500GB',12,39990),('Batería Samsung A54',8,45990),('Pasta térmica',25,5990),('Ventilador notebook 5V',6,18990);
INSERT INTO ordenes_servicio_ser (id_equipo,id_tecnico,estado,descripcion_falla,costo_mano_obra) VALUES
(1,1,'En diagnóstico','Equipo lento y demora al iniciar',15000),(2,2,'Ingresada','Batería dura pocas horas',12000),(3,1,'En reparación','Se apaga por temperatura',18000),(4,3,'Ingresada','No muestra imagen',20000);
INSERT INTO detalle_orden_ser (id_orden,id_repuesto,cantidad,precio_unitario) VALUES
(1,1,1,39990),(2,2,1,45990),(3,3,1,5990),(3,4,1,18990);
