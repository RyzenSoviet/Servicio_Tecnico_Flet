# Servicio Técnico Flet

## Aplicación interna (trabajadores)
1. Instala dependencias: `pip install -r requirements.txt`
2. Revisa que `.env` tenga los datos de conexión correctos.
3. Ejecuta: `python main.py`

La app Flet administra clientes y equipos conectándose a `aaron_cancino_test` mediante `connect.py`.

## Portal HTML (clientes)
El HTML está en `templates/index.html`, pero **no se conecta directamente a MySQL** porque eso expondría las credenciales en el navegador. La conexión segura la realiza `web_app.py` usando el mismo `connect.py` y `.env` de la app Flet.

1. Instala dependencias: `pip install -r requirements.txt`
2. Ejecuta: `python web_app.py`
3. Abre en el navegador: `http://127.0.0.1:5000`
4. El cliente consulta con su correo registrado + número de serie.

El portal lee datos reales de `clientes_ser`, `equipos_ser`, `ordenes_servicio_ser`, `tecnicos_ser` y `detalle_orden_ser`. No permite editar ni eliminar información.

> No ejecutes `01_creacion.sql` sobre tu base actual si ya tienes las tablas y datos creados en DBeaver.
