from flask import Flask, render_template, request
from connect import db_cursor
import mysql.connector

app = Flask(__name__)


def buscar_estado(email, serie):
    sql = '''
        SELECT c.nombre AS cliente, e.tipo, e.marca, e.modelo, e.numero_serie,
               e.estado AS estado_equipo, e.fecha_ingreso,
               o.id_orden, o.fecha_recepcion, o.fecha_entrega, o.diagnostico,
               o.descripcion_falla, o.estado AS estado_orden, o.costo_mano_obra,
               COALESCE(t.nombre, 'Sin técnico asignado') AS tecnico,
               COALESCE(SUM(d.cantidad * d.precio_unitario), 0) AS total_repuestos
        FROM clientes_ser c
        JOIN equipos_ser e ON e.id_cliente = c.id_cliente
        LEFT JOIN ordenes_servicio_ser o ON o.id_equipo = e.id_equipo
        LEFT JOIN tecnicos_ser t ON t.id_tecnico = o.id_tecnico
        LEFT JOIN detalle_orden_ser d ON d.id_orden = o.id_orden
        WHERE LOWER(c.email) = LOWER(%s) AND e.numero_serie = %s
        GROUP BY c.nombre, e.tipo, e.marca, e.modelo, e.numero_serie,
                 e.estado, e.fecha_ingreso, o.id_orden, o.fecha_recepcion,
                 o.fecha_entrega, o.diagnostico, o.descripcion_falla,
                 o.estado, o.costo_mano_obra, t.nombre
        ORDER BY o.fecha_recepcion DESC
        LIMIT 1
    '''
    with db_cursor(True) as (_, cur):
        cur.execute(sql, (email.strip(), serie.strip()))
        return cur.fetchone()


@app.route('/', methods=['GET', 'POST'])
def inicio():
    resultado = None
    mensaje = None
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        serie = request.form.get('serie', '').strip()
        if not email or not serie:
            mensaje = 'Ingresa tu correo y el número de serie del equipo.'
        else:
            try:
                resultado = buscar_estado(email, serie)
                if not resultado:
                    mensaje = 'No encontramos un equipo que coincida con esos datos.'
            except mysql.connector.Error:
                mensaje = 'No fue posible consultar el sistema en este momento.'
    return render_template('index.html', resultado=resultado, mensaje=mensaje)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)
