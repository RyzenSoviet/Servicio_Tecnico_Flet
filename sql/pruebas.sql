USE servicio_tecnico_db;
SELECT * FROM clientes_ser;
SELECT e.id_equipo,c.nombre,e.tipo,e.marca,e.modelo,e.estado FROM equipos_ser e JOIN clientes_ser c ON c.id_cliente=e.id_cliente;
SELECT * FROM vw_ordenes_resumen;
CALL sp_reporte_cliente(1);
CALL sp_actualizar_estado_orden(1,'En reparación');
-- Transaccional (usar un repuesto con stock disponible):
CALL sp_agregar_repuesto_orden(4,3,1);
-- Prueba inválida de trigger (debe fallar por stock):
-- CALL sp_agregar_repuesto_orden(4,4,999);
