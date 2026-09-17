USE servicio_tecnico_db;
DROP VIEW IF EXISTS vw_ordenes_resumen;
CREATE VIEW vw_ordenes_resumen AS
SELECT o.id_orden,c.nombre cliente,e.tipo tipo_equipo,e.marca,e.modelo,e.numero_serie,
 COALESCE(t.nombre,'Sin técnico asignado') tecnico,o.fecha_recepcion,o.estado,o.descripcion_falla,o.costo_mano_obra,
 COALESCE(SUM(d.cantidad*d.precio_unitario),0) total_repuestos,
 o.costo_mano_obra+COALESCE(SUM(d.cantidad*d.precio_unitario),0) total_orden
FROM ordenes_servicio_ser o JOIN equipos_ser e ON e.id_equipo=o.id_equipo JOIN clientes_ser c ON c.id_cliente=e.id_cliente
LEFT JOIN tecnicos_ser t ON t.id_tecnico=o.id_tecnico LEFT JOIN detalle_orden_ser d ON d.id_orden=o.id_orden
GROUP BY o.id_orden,c.nombre,e.tipo,e.marca,e.modelo,e.numero_serie,t.nombre,o.fecha_recepcion,o.estado,o.descripcion_falla,o.costo_mano_obra;

DELIMITER $$
DROP TRIGGER IF EXISTS trg_detalle_stock_bi$$
CREATE TRIGGER trg_detalle_stock_bi BEFORE INSERT ON detalle_orden_ser FOR EACH ROW
BEGIN
 DECLARE disponible INT;
 SELECT stock INTO disponible FROM repuestos_ser WHERE id_repuesto=NEW.id_repuesto FOR UPDATE;
 IF disponible IS NULL OR NEW.cantidad > disponible THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT='Stock insuficiente para el repuesto'; END IF;
END$$
DROP TRIGGER IF EXISTS trg_detalle_descuenta_ai$$
CREATE TRIGGER trg_detalle_descuenta_ai AFTER INSERT ON detalle_orden_ser FOR EACH ROW
BEGIN UPDATE repuestos_ser SET stock=stock-NEW.cantidad WHERE id_repuesto=NEW.id_repuesto; END$$

DROP PROCEDURE IF EXISTS sp_agregar_repuesto_orden$$
CREATE PROCEDURE sp_agregar_repuesto_orden(IN p_orden INT, IN p_repuesto INT, IN p_cantidad INT)
BEGIN
 DECLARE v_precio DECIMAL(10,2);
 DECLARE EXIT HANDLER FOR SQLEXCEPTION BEGIN ROLLBACK; RESIGNAL; END;
 START TRANSACTION;
 SELECT precio INTO v_precio FROM repuestos_ser WHERE id_repuesto=p_repuesto FOR UPDATE;
 IF v_precio IS NULL THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT='Repuesto inexistente'; END IF;
 INSERT INTO detalle_orden_ser(id_orden,id_repuesto,cantidad,precio_unitario) VALUES(p_orden,p_repuesto,p_cantidad,v_precio);
 COMMIT;
END$$
DROP PROCEDURE IF EXISTS sp_actualizar_estado_orden$$
CREATE PROCEDURE sp_actualizar_estado_orden(IN p_orden INT, IN p_estado VARCHAR(30))
BEGIN
 IF p_estado NOT IN ('Ingresada','En diagnóstico','En reparación','Finalizada','Entregada') THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT='Estado de orden no válido'; END IF;
 UPDATE ordenes_servicio_ser SET estado=p_estado, fecha_entrega=IF(p_estado='Entregada',NOW(),fecha_entrega) WHERE id_orden=p_orden;
END$$
DROP PROCEDURE IF EXISTS sp_reporte_cliente$$
CREATE PROCEDURE sp_reporte_cliente(IN p_cliente INT)
BEGIN SELECT * FROM vw_ordenes_resumen WHERE id_orden IN (SELECT o.id_orden FROM ordenes_servicio_ser o JOIN equipos_ser e ON e.id_equipo=o.id_equipo WHERE e.id_cliente=p_cliente); END$$
DELIMITER ;
