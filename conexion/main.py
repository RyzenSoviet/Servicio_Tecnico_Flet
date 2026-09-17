import flet as ft
import mysql.connector
import data_access as db


BG = '#080a0d'
SURFACE = '#11151a'
SURFACE_ALT = '#171c22'
BORDER = '#29313b'
TEXT = '#f3f5f7'
MUTED = '#96a0ad'
ACCENT = '#f0b24b'


def main(page: ft.Page):
    page.title = 'Servicio Técnico'
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = BG
    page.padding = 0

    contenido = ft.Column(expand=True, scroll=ft.ScrollMode.AUTO, spacing=22)

    def aviso(txt):
        page.snack_bar = ft.SnackBar(ft.Text(txt, color=TEXT))
        page.snack_bar.open = True
        page.update()

    def campo(control, width=220):
        control.width = width
        control.color = TEXT
        control.border_color = BORDER
        control.focused_border_color = ACCENT
        control.label_style = ft.TextStyle(color=MUTED)
        return control

    def panel(content, padding=18):
        return ft.Container(
            content=content,
            bgcolor=SURFACE,
            border_radius=10,
            padding=padding,
        )

    def cabecera(titulo, subtitulo, icono):
        return ft.Row(
            [
                ft.Container(
                    content=ft.Icon(icono, color=ACCENT, size=28),
                    bgcolor=SURFACE_ALT,
                    border_radius=9,
                    padding=12,
                ),
                ft.Column(
                    [
                        ft.Text(titulo, size=28, weight=ft.FontWeight.BOLD, color=TEXT),
                        ft.Text(subtitulo, size=13, color=MUTED),
                    ],
                    spacing=3,
                ),
            ],
            spacing=14,
        )

    def titulo_panel(titulo, subtitulo):
        return ft.Column(
            [
                ft.Text(titulo, size=16, weight=ft.FontWeight.BOLD, color=TEXT),
                ft.Text(subtitulo, size=12, color=MUTED),
            ],
            spacing=4,
        )

    def boton(texto, on_click):
        return ft.Button(texto, on_click=on_click)

    def clientes_view():
        contenido.controls.clear()
        edit = {'id': None}
        nombre = campo(ft.TextField(label='Nombre'))
        tel = campo(ft.TextField(label='Teléfono'))
        email = campo(ft.TextField(label='Email'))
        direccion = campo(ft.TextField(label='Dirección'), 280)
        buscar = campo(ft.TextField(label='Buscar por nombre o email', prefix_icon=ft.Icons.SEARCH), 320)
        tabla = ft.DataTable(
            columns=[ft.DataColumn(ft.Text(x, color=MUTED)) for x in ['ID', 'Nombre', 'Teléfono', 'Email', 'Dirección', 'Acciones']],
            rows=[],
        )

        def limpiar():
            edit['id'] = None
            for control in (nombre, tel, email, direccion):
                control.value = ''

        def cargar(_=None):
            tabla.rows.clear()
            for r in db.clientes(buscar.value or ''):
                def ed(_, r=r):
                    edit['id'] = r['id_cliente']
                    nombre.value = r['nombre']
                    tel.value = r['telefono']
                    email.value = r['email']
                    direccion.value = r['direccion']
                    page.update()

                def bor(_, r=r):
                    try:
                        db.eliminar_cliente(r['id_cliente'])
                        aviso('Cliente eliminado')
                        cargar()
                    except Exception as e:
                        aviso('No se puede eliminar: ' + str(e))

                acciones = ft.Row([
                    ft.IconButton(ft.Icons.EDIT, icon_color=ACCENT, on_click=ed),
                    ft.IconButton(ft.Icons.DELETE, icon_color='#e57373', on_click=bor),
                ], spacing=0)
                tabla.rows.append(ft.DataRow(cells=[
                    ft.DataCell(ft.Text(str(r[k]), color=TEXT))
                    for k in ['id_cliente', 'nombre', 'telefono', 'email', 'direccion']
                ] + [ft.DataCell(acciones)]))
            page.update()

        def guardar(_):
            if not all([nombre.value, tel.value, email.value, direccion.value]):
                return aviso('Completa todos los campos')
            try:
                if edit['id']:
                    db.editar_cliente(edit['id'], nombre.value, tel.value, email.value, direccion.value)
                else:
                    db.crear_cliente(nombre.value, tel.value, email.value, direccion.value)
                limpiar()
                cargar()
                aviso('Cliente guardado')
            except Exception as e:
                aviso('Error: ' + str(e))

        buscar.on_change = cargar
        formulario = panel(ft.Column([
            titulo_panel('Datos del cliente', 'Completa la información para registrar o actualizar un cliente.'),
            ft.Row([nombre, tel, email, direccion], wrap=True, spacing=12),
            ft.Row([boton('Guardar cliente', guardar)], alignment=ft.MainAxisAlignment.END),
        ], spacing=16))
        listado = panel(ft.Column([
            ft.Row([titulo_panel('Clientes registrados', 'Consulta y administra los clientes de la base de datos.'), buscar], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Row([tabla], scroll=ft.ScrollMode.AUTO),
        ], spacing=16))
        contenido.controls.extend([cabecera('Clientes', 'Directorio de clientes y datos de contacto.', ft.Icons.PEOPLE), formulario, listado])
        cargar()

    def equipos_view():
        contenido.controls.clear()
        edit = {'id': None}
        cli = campo(ft.Dropdown(label='Cliente'), 240)
        tipo = campo(ft.TextField(label='Tipo'))
        marca = campo(ft.TextField(label='Marca'))
        modelo = campo(ft.TextField(label='Modelo'))
        serie = campo(ft.TextField(label='N° serie'))
        estado = campo(ft.Dropdown(label='Estado', options=[ft.dropdown.Option(x) for x in ['Ingresado', 'En diagnóstico', 'En reparación', 'Listo', 'Entregado']]), 190)
        buscar = campo(ft.TextField(label='Buscar por serie, marca o modelo', prefix_icon=ft.Icons.SEARCH), 320)
        tabla = ft.DataTable(
            columns=[ft.DataColumn(ft.Text(x, color=MUTED)) for x in ['ID', 'Cliente', 'Equipo', 'Serie', 'Estado', 'Acciones']],
            rows=[],
        )

        def opciones():
            cli.options = [ft.dropdown.Option(str(x['id_cliente']), x['nombre']) for x in db.opciones_clientes()]

        def limpiar():
            edit['id'] = None
            cli.value = None
            for control in (tipo, marca, modelo, serie):
                control.value = ''
            estado.value = 'Ingresado'

        def cargar(_=None):
            opciones()
            tabla.rows.clear()
            for r in db.equipos(buscar.value or ''):
                def ed(_, r=r):
                    edit['id'] = r['id_equipo']
                    cli.value = str(r['id_cliente'])
                    tipo.value = r['tipo']
                    marca.value = r['marca']
                    modelo.value = r['modelo']
                    serie.value = r['numero_serie']
                    estado.value = r['estado']
                    page.update()

                def bor(_, r=r):
                    try:
                        db.eliminar_equipo(r['id_equipo'])
                        aviso('Equipo eliminado')
                        cargar()
                    except Exception as e:
                        aviso('No se puede eliminar: ' + str(e))

                acciones = ft.Row([
                    ft.IconButton(ft.Icons.EDIT, icon_color=ACCENT, on_click=ed),
                    ft.IconButton(ft.Icons.DELETE, icon_color='#e57373', on_click=bor),
                ], spacing=0)
                tabla.rows.append(ft.DataRow(cells=[
                    ft.DataCell(ft.Text(str(r['id_equipo']), color=TEXT)),
                    ft.DataCell(ft.Text(r['cliente'], color=TEXT)),
                    ft.DataCell(ft.Text(r['marca'] + ' ' + r['modelo'], color=TEXT)),
                    ft.DataCell(ft.Text(r['numero_serie'], color=TEXT)),
                    ft.DataCell(ft.Text(r['estado'], color=TEXT)),
                    ft.DataCell(acciones),
                ]))
            page.update()

        def guardar(_):
            if not all([cli.value, tipo.value, marca.value, modelo.value, serie.value, estado.value]):
                return aviso('Completa todos los campos')
            try:
                args = (int(cli.value), tipo.value, marca.value, modelo.value, serie.value, estado.value)
                db.editar_equipo(edit['id'], *args) if edit['id'] else db.crear_equipo(*args)
                limpiar()
                cargar()
                aviso('Equipo guardado')
            except Exception as e:
                aviso('Error: ' + str(e))

        buscar.on_change = cargar
        formulario = panel(ft.Column([
            titulo_panel('Datos del equipo', 'Asocia el equipo a un cliente y registra su estado actual.'),
            ft.Row([cli, tipo, marca, modelo, serie, estado], wrap=True, spacing=12),
            ft.Row([boton('Guardar equipo', guardar)], alignment=ft.MainAxisAlignment.END),
        ], spacing=16))
        listado = panel(ft.Column([
            ft.Row([titulo_panel('Equipos registrados', 'Consulta el inventario técnico y su estado de reparación.'), buscar], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Row([tabla], scroll=ft.ScrollMode.AUTO),
        ], spacing=16))
        contenido.controls.extend([cabecera('Equipos', 'Inventario y seguimiento de equipos en servicio.', ft.Icons.COMPUTER), formulario, listado])
        cargar()

    def cambiar(e):
        clientes_view() if e.control.selected_index == 0 else equipos_view()

    nav = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        expand=True,
        destinations=[
            ft.NavigationRailDestination(icon=ft.Icons.PEOPLE_OUTLINE, selected_icon=ft.Icons.PEOPLE, label='Clientes'),
            ft.NavigationRailDestination(icon=ft.Icons.COMPUTER_OUTLINED, selected_icon=ft.Icons.COMPUTER, label='Equipos'),
        ],
        on_change=cambiar,
        bgcolor=SURFACE,
        indicator_color='#3a2c18',
    )
    marca = ft.Container(
        content=ft.Column([
            ft.Text('FLET / SERVICE', size=11, weight=ft.FontWeight.BOLD, color=ACCENT),
            ft.Text('Panel técnico', size=20, weight=ft.FontWeight.BOLD, color=TEXT),
            ft.Divider(color=BORDER),
        ], spacing=6),
        padding=18,
    )
    lateral = ft.Container(
        content=ft.Column([marca, nav], expand=True, spacing=18),
        width=220,
        height=float('inf'),
        bgcolor=SURFACE,
    )

    page.add(ft.Row([
        lateral,
        ft.Container(content=contenido, expand=True, padding=30),
    ], expand=True, spacing=0))
    try:
        clientes_view()
    except mysql.connector.Error as e:
        contenido.controls = [ft.Text('No se pudo conectar a MySQL.', color='#e57373'), ft.Text(str(e), color=MUTED)]
        page.update()


ft.run(main)
