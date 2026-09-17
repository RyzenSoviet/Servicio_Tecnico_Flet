from connect import db_cursor

def query(sql, params=()):
    with db_cursor(True) as (_, cur):
        cur.execute(sql, params); return cur.fetchall()

def execute(sql, params=()):
    with db_cursor() as (conn, cur):
        cur.execute(sql, params); conn.commit(); return cur.lastrowid

def clientes(buscar=''):
    t=f'%{buscar}%'; return query('SELECT * FROM clientes_ser WHERE nombre LIKE %s OR email LIKE %s ORDER BY id_cliente',(t,t))
def crear_cliente(n,tel,email,dir): return execute('INSERT INTO clientes_ser(nombre,telefono,email,direccion) VALUES(%s,%s,%s,%s)',(n,tel,email,dir))
def editar_cliente(i,n,tel,email,dir): return execute('UPDATE clientes_ser SET nombre=%s,telefono=%s,email=%s,direccion=%s WHERE id_cliente=%s',(n,tel,email,dir,i))
def eliminar_cliente(i): return execute('DELETE FROM clientes_ser WHERE id_cliente=%s',(i,))
def equipos(buscar=''):
    t=f'%{buscar}%'; return query('''SELECT e.*,c.nombre cliente FROM equipos_ser e JOIN clientes_ser c ON c.id_cliente=e.id_cliente WHERE e.numero_serie LIKE %s OR e.marca LIKE %s OR e.modelo LIKE %s ORDER BY e.id_equipo''',(t,t,t))
def crear_equipo(c,tipo,marca,modelo,serie,estado): return execute('INSERT INTO equipos_ser(id_cliente,tipo,marca,modelo,numero_serie,estado) VALUES(%s,%s,%s,%s,%s,%s)',(c,tipo,marca,modelo,serie,estado))
def editar_equipo(i,c,tipo,marca,modelo,serie,estado): return execute('UPDATE equipos_ser SET id_cliente=%s,tipo=%s,marca=%s,modelo=%s,numero_serie=%s,estado=%s WHERE id_equipo=%s',(c,tipo,marca,modelo,serie,estado,i))
def eliminar_equipo(i): return execute('DELETE FROM equipos_ser WHERE id_equipo=%s',(i,))
def opciones_clientes(): return query('SELECT id_cliente,nombre FROM clientes_ser ORDER BY nombre')
