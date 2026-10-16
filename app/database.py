import calendar
import os
import sqlite3
from datetime import date, timedelta


RAIZ_PROYECTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DB_NAME = os.path.join(RAIZ_PROYECTO, "data", "gym_management.db")

ESTADOS_PAGO = ("pagado", "pendiente", "vencido")

UNIDADES_DURACION = ("dias", "meses")

ESTADOS_TIPO_MEMBRESIA = ("activo", "inactivo")

SEXOS = ("Femenino", "Masculino", "Otro")

OBJETIVOS_ENTRENAMIENTO = (
    "Bajar de peso",
    "Ganar masa muscular",
    "Salud y mantenimiento",
    "Rendimiento deportivo",
    "Rehabilitación",
    "Otro",
)

# Columnas agregadas a miembros después de la primera versión. Se crean
# automáticamente en bases existentes al ejecutar crear_tablas().
COLUMNAS_ADICIONALES_MIEMBROS = (
    "fecha_nacimiento",
    "sexo",
    "direccion",
    "objetivo",
    "contacto_emergencia",
    "telefono_emergencia",
    "observaciones_medicas",
)

TIPOS_MEMBRESIA_INICIALES = [
    # (nombre, duracion_cantidad, duracion_unidad, precio)
    ("Diaria", 1, "dias", 20000),
    ("Quincenal", 15, "dias", 80000),
    ("Mensual", 1, "meses", 150000),
    ("Trimestral", 3, "meses", 400000),
    ("Anual", 12, "meses", 1400000),
]


def conectar():
    """
    Establece la conexión con la base de datos SQLite.

    Retorna:
        sqlite3.Connection: Objeto de conexión a la base de datos.
    """
    conexion = sqlite3.connect(DB_NAME)
    conexion.execute("PRAGMA foreign_keys = ON")
    return conexion


def crear_tablas():
    """
    Crea las tablas del sistema si todavía no existen.

    Permite generar una base de datos nueva (por ejemplo, para pruebas)
    con la misma estructura que la base del proyecto.
    """
    conexion = conectar()

    try:
        conexion.executescript("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                usuario TEXT NOT NULL UNIQUE,
                contrasena TEXT NOT NULL,
                rol TEXT NOT NULL,
                estado TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS miembros (
                id_miembro INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL,
                cedula TEXT NOT NULL UNIQUE,
                telefono TEXT,
                correo TEXT,
                fecha_registro TEXT NOT NULL,
                estado TEXT NOT NULL,
                fecha_nacimiento TEXT,
                sexo TEXT,
                direccion TEXT,
                objetivo TEXT,
                contacto_emergencia TEXT,
                telefono_emergencia TEXT,
                observaciones_medicas TEXT
            );

            CREATE TABLE IF NOT EXISTS pagos_cuotas (
                id_pago INTEGER PRIMARY KEY AUTOINCREMENT,
                id_miembro INTEGER NOT NULL,
                monto INTEGER NOT NULL,
                fecha_pago TEXT NOT NULL,
                tipo_membresia TEXT NOT NULL,
                fecha_inicio TEXT NOT NULL,
                fecha_vencimiento TEXT NOT NULL,
                estado_pago TEXT NOT NULL,
                FOREIGN KEY (id_miembro) REFERENCES miembros(id_miembro)
            );

            CREATE TABLE IF NOT EXISTS asistencias (
                id_asistencia INTEGER PRIMARY KEY AUTOINCREMENT,
                id_miembro INTEGER NOT NULL,
                fecha TEXT NOT NULL,
                hora_entrada TEXT NOT NULL,
                observacion TEXT,
                FOREIGN KEY (id_miembro) REFERENCES miembros(id_miembro)
            );

            CREATE TABLE IF NOT EXISTS tipos_membresia (
                id_tipo INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL UNIQUE,
                duracion_cantidad INTEGER NOT NULL,
                duracion_unidad TEXT NOT NULL,
                precio INTEGER NOT NULL,
                estado TEXT NOT NULL
            );
        """)

        cursor = conexion.cursor()

        cursor.execute("PRAGMA table_info(miembros)")
        columnas_existentes = {fila[1] for fila in cursor.fetchall()}

        for columna in COLUMNAS_ADICIONALES_MIEMBROS:
            if columna not in columnas_existentes:
                cursor.execute(f"ALTER TABLE miembros ADD COLUMN {columna} TEXT")

        cursor.execute("SELECT COUNT(*) FROM tipos_membresia")

        if cursor.fetchone()[0] == 0:
            cursor.executemany("""
                INSERT INTO tipos_membresia (
                    nombre,
                    duracion_cantidad,
                    duracion_unidad,
                    precio,
                    estado
                )
                VALUES (?, ?, ?, ?, 'activo')
            """, TIPOS_MEMBRESIA_INICIALES)

        conexion.commit()

    finally:
        conexion.close()


def verificar_usuario(usuario, contrasena):
    """
    Verifica las credenciales ingresadas por el usuario.

    Retorna:
        tuple | None: Datos del usuario si las credenciales son correctas.
    """
    conexion = conectar()

    try:
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT *
            FROM usuarios
            WHERE usuario = ?
            AND contrasena = ?
            AND estado = 'activo'
        """, (usuario, contrasena))

        return cursor.fetchone()

    finally:
        conexion.close()


def registrar_miembro(
    nombre,
    apellido,
    cedula,
    telefono,
    correo,
    fecha_nacimiento=None,
    sexo="",
    direccion="",
    objetivo="",
    contacto_emergencia="",
    telefono_emergencia="",
    observaciones_medicas=""
):
    """
    Registra un nuevo miembro en la base de datos.

    Parámetros:
        nombre (str): Nombre del miembro.
        apellido (str): Apellido del miembro.
        cedula (str): Número de cédula.
        telefono (str): Teléfono de contacto.
        correo (str): Correo electrónico.
        fecha_nacimiento (date | None): Fecha de nacimiento (opcional).
        sexo (str): Uno de SEXOS, o vacío.
        direccion (str): Dirección del miembro.
        objetivo (str): Uno de OBJETIVOS_ENTRENAMIENTO, o vacío.
        contacto_emergencia (str): Nombre de la persona a avisar.
        telefono_emergencia (str): Teléfono de esa persona.
        observaciones_medicas (str): Lesiones, alergias o condiciones.

    Retorna:
        tuple: True y mensaje si se registra correctamente.
               False y mensaje si ocurre un error.
    """
    if sexo and sexo not in SEXOS:
        return False, "El sexo seleccionado no es válido."

    if objetivo and objetivo not in OBJETIVOS_ENTRENAMIENTO:
        return False, "El objetivo seleccionado no es válido."

    if fecha_nacimiento is not None and fecha_nacimiento > date.today():
        return False, "La fecha de nacimiento no puede ser futura."

    conexion = conectar()

    try:
        cursor = conexion.cursor()
        fecha_registro = date.today().isoformat()

        cursor.execute("""
            INSERT INTO miembros (
                nombre,
                apellido,
                cedula,
                telefono,
                correo,
                fecha_registro,
                estado,
                fecha_nacimiento,
                sexo,
                direccion,
                objetivo,
                contacto_emergencia,
                telefono_emergencia,
                observaciones_medicas
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            nombre.strip(),
            apellido.strip(),
            cedula.strip(),
            telefono.strip(),
            correo.strip(),
            fecha_registro,
            "activo",
            fecha_nacimiento.isoformat() if fecha_nacimiento else None,
            sexo,
            direccion.strip(),
            objetivo,
            contacto_emergencia.strip(),
            telefono_emergencia.strip(),
            observaciones_medicas.strip()
        ))

        conexion.commit()

        return True, "Miembro registrado correctamente."

    except sqlite3.IntegrityError:
        return False, "La cédula ingresada ya está registrada."

    except sqlite3.Error as error:
        return False, f"Error al registrar el miembro: {error}"

    finally:
        conexion.close()

def buscar_miembro_por_cedula(cedula):
    """
    Busca un miembro por su número de cédula.

    Retorna:
        tuple | None: (id_miembro, nombre, apellido, cedula, estado)
                      o None si no existe.
    """
    conexion = conectar()

    try:
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT id_miembro, nombre, apellido, cedula, estado
            FROM miembros
            WHERE cedula = ?
        """, (cedula.strip(),))

        return cursor.fetchone()

    finally:
        conexion.close()


def obtener_tipos_membresia():
    """
    Obtiene los tipos de membresía activos.

    Retorna:
        list[tuple]: (id_tipo, nombre, duracion_cantidad, duracion_unidad, precio)
    """
    conexion = conectar()

    try:
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT id_tipo, nombre, duracion_cantidad, duracion_unidad, precio
            FROM tipos_membresia
            WHERE estado = 'activo'
            ORDER BY id_tipo
        """)

        return cursor.fetchall()

    finally:
        conexion.close()


def calcular_fecha_vencimiento(fecha_inicio, cantidad, unidad):
    """
    Calcula la fecha de vencimiento de una membresía.

    Los meses se suman por calendario: si el día no existe en el mes de
    destino se usa el último día de ese mes (31/01 + 1 mes = 28/02).

    Parámetros:
        fecha_inicio (date): Fecha de inicio de la membresía.
        cantidad (int): Duración de la membresía.
        unidad (str): 'dias' o 'meses'.

    Retorna:
        date: Fecha de vencimiento.
    """
    if unidad == "dias":
        return fecha_inicio + timedelta(days=cantidad)

    if unidad == "meses":
        total_meses = fecha_inicio.month - 1 + cantidad
        anio = fecha_inicio.year + total_meses // 12
        mes = total_meses % 12 + 1
        dia = min(fecha_inicio.day, calendar.monthrange(anio, mes)[1])
        return date(anio, mes, dia)

    raise ValueError(f"Unidad de duración no válida: {unidad}")


def registrar_pago(id_miembro, id_tipo, monto, fecha_inicio, estado_pago):
    """
    Registra un pago de cuota calculando su fecha de vencimiento según
    el tipo de membresía.

    Parámetros:
        id_miembro (int): Miembro que realiza el pago.
        id_tipo (int): Tipo de membresía elegido.
        monto (int): Monto cobrado.
        fecha_inicio (date): Fecha de inicio de la membresía.
        estado_pago (str): 'pagado', 'pendiente' o 'vencido'.

    Retorna:
        tuple: True y mensaje si se registra correctamente.
               False y mensaje si ocurre un error.
    """
    if estado_pago not in ESTADOS_PAGO:
        return False, "El estado del pago no es válido."

    if monto <= 0:
        return False, "El monto debe ser mayor a cero."

    conexion = conectar()

    try:
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT nombre, duracion_cantidad, duracion_unidad
            FROM tipos_membresia
            WHERE id_tipo = ?
        """, (id_tipo,))
        tipo = cursor.fetchone()

        if tipo is None:
            return False, "El tipo de membresía no existe."

        nombre_tipo, cantidad, unidad = tipo
        fecha_vencimiento = calcular_fecha_vencimiento(fecha_inicio, cantidad, unidad)

        cursor.execute("""
            INSERT INTO pagos_cuotas (
                id_miembro,
                monto,
                fecha_pago,
                tipo_membresia,
                fecha_inicio,
                fecha_vencimiento,
                estado_pago
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            id_miembro,
            monto,
            date.today().isoformat(),
            nombre_tipo,
            fecha_inicio.isoformat(),
            fecha_vencimiento.isoformat(),
            estado_pago
        ))

        conexion.commit()

        return True, "Pago registrado correctamente."

    except sqlite3.IntegrityError:
        return False, "El miembro seleccionado no existe."

    except sqlite3.Error as error:
        return False, f"Error al registrar el pago: {error}"

    finally:
        conexion.close()


def actualizar_pagos_vencidos():
    """
    Marca como 'vencido' los pagos pendientes cuya fecha de vencimiento
    ya pasó.

    Retorna:
        int: Cantidad de pagos actualizados.
    """
    conexion = conectar()

    try:
        cursor = conexion.cursor()

        cursor.execute("""
            UPDATE pagos_cuotas
            SET estado_pago = 'vencido'
            WHERE estado_pago = 'pendiente'
            AND fecha_vencimiento < ?
        """, (date.today().isoformat(),))

        conexion.commit()

        return cursor.rowcount

    finally:
        conexion.close()


def listar_pagos(id_miembro=None, limite=100):
    """
    Lista los pagos registrados, del más reciente al más antiguo.

    Parámetros:
        id_miembro (int | None): Si se indica, solo lista los pagos de ese miembro.
        limite (int): Cantidad máxima de pagos a retornar.

    Retorna:
        list[tuple]: (id_pago, miembro, cedula, tipo_membresia, monto,
                      fecha_pago, fecha_inicio, fecha_vencimiento, estado_pago)
    """
    conexion = conectar()

    try:
        cursor = conexion.cursor()

        consulta = """
            SELECT
                p.id_pago,
                m.nombre || ' ' || m.apellido,
                m.cedula,
                p.tipo_membresia,
                p.monto,
                p.fecha_pago,
                p.fecha_inicio,
                p.fecha_vencimiento,
                p.estado_pago
            FROM pagos_cuotas p
            JOIN miembros m ON m.id_miembro = p.id_miembro
        """
        parametros = []

        if id_miembro is not None:
            consulta += " WHERE p.id_miembro = ?"
            parametros.append(id_miembro)

        consulta += " ORDER BY p.fecha_inicio DESC, p.id_pago DESC LIMIT ?"
        parametros.append(limite)

        cursor.execute(consulta, parametros)

        return cursor.fetchall()

    finally:
        conexion.close()


def listar_tipos_membresia():
    """
    Lista todos los tipos de membresía, activos e inactivos, para la
    pantalla de configuración.

    Retorna:
        list[tuple]: (id_tipo, nombre, duracion_cantidad, duracion_unidad,
                      precio, estado)
    """
    conexion = conectar()

    try:
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT id_tipo, nombre, duracion_cantidad, duracion_unidad, precio, estado
            FROM tipos_membresia
            ORDER BY id_tipo
        """)

        return cursor.fetchall()

    finally:
        conexion.close()


def validar_tipo_membresia(nombre, duracion_cantidad, duracion_unidad, precio):
    """
    Valida los datos de un tipo de membresía.

    Retorna:
        str | None: Mensaje de error, o None si los datos son válidos.
    """
    if not nombre.strip():
        return "El nombre del tipo de membresía es obligatorio."

    if duracion_unidad not in UNIDADES_DURACION:
        return "La unidad de duración no es válida."

    if duracion_cantidad <= 0:
        return "La duración debe ser mayor a cero."

    if precio <= 0:
        return "El precio debe ser mayor a cero."

    return None


def crear_tipo_membresia(nombre, duracion_cantidad, duracion_unidad, precio):
    """
    Crea un nuevo tipo de membresía en estado activo.

    Parámetros:
        nombre (str): Nombre del tipo (Semanal, Mensual, etc.).
        duracion_cantidad (int): Cantidad de días o meses que dura.
        duracion_unidad (str): 'dias' o 'meses'.
        precio (int): Precio sugerido en guaraníes.

    Retorna:
        tuple: True y mensaje si se crea correctamente.
               False y mensaje si ocurre un error.
    """
    error = validar_tipo_membresia(nombre, duracion_cantidad, duracion_unidad, precio)

    if error:
        return False, error

    conexion = conectar()

    try:
        conexion.execute("""
            INSERT INTO tipos_membresia (
                nombre,
                duracion_cantidad,
                duracion_unidad,
                precio,
                estado
            )
            VALUES (?, ?, ?, ?, 'activo')
        """, (nombre.strip(), duracion_cantidad, duracion_unidad, precio))

        conexion.commit()

        return True, "Tipo de membresía creado correctamente."

    except sqlite3.IntegrityError:
        return False, "Ya existe un tipo de membresía con ese nombre."

    except sqlite3.Error as error:
        return False, f"Error al crear el tipo de membresía: {error}"

    finally:
        conexion.close()


def actualizar_tipo_membresia(id_tipo, nombre, duracion_cantidad, duracion_unidad, precio):
    """
    Modifica los datos de un tipo de membresía existente.

    Los pagos ya registrados no cambian, porque guardan el nombre, el monto
    y las fechas al momento del registro.

    Retorna:
        tuple: True y mensaje si se actualiza correctamente.
               False y mensaje si ocurre un error.
    """
    error = validar_tipo_membresia(nombre, duracion_cantidad, duracion_unidad, precio)

    if error:
        return False, error

    conexion = conectar()

    try:
        cursor = conexion.cursor()

        cursor.execute("""
            UPDATE tipos_membresia
            SET nombre = ?,
                duracion_cantidad = ?,
                duracion_unidad = ?,
                precio = ?
            WHERE id_tipo = ?
        """, (nombre.strip(), duracion_cantidad, duracion_unidad, precio, id_tipo))

        if cursor.rowcount == 0:
            return False, "El tipo de membresía no existe."

        conexion.commit()

        return True, "Tipo de membresía actualizado correctamente."

    except sqlite3.IntegrityError:
        return False, "Ya existe un tipo de membresía con ese nombre."

    except sqlite3.Error as error:
        return False, f"Error al actualizar el tipo de membresía: {error}"

    finally:
        conexion.close()


def cambiar_estado_tipo_membresia(id_tipo, estado):
    """
    Activa o desactiva un tipo de membresía. Los inactivos no se ofrecen
    al registrar pagos, pero se conservan para el historial.

    Retorna:
        tuple: True y mensaje si se actualiza correctamente.
               False y mensaje si ocurre un error.
    """
    if estado not in ESTADOS_TIPO_MEMBRESIA:
        return False, "El estado no es válido."

    conexion = conectar()

    try:
        cursor = conexion.cursor()

        cursor.execute("""
            UPDATE tipos_membresia
            SET estado = ?
            WHERE id_tipo = ?
        """, (estado, id_tipo))

        if cursor.rowcount == 0:
            return False, "El tipo de membresía no existe."

        conexion.commit()

        return True, f"Tipo de membresía marcado como {estado}."

    finally:
        conexion.close()
