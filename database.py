import sqlite3
from datetime import date


DB_NAME = "gym_management.db"


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
                estado TEXT NOT NULL
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
        """)

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


def registrar_miembro(nombre, apellido, cedula, telefono, correo):
    """
    Registra un nuevo miembro en la base de datos.

    Parámetros:
        nombre (str): Nombre del miembro.
        apellido (str): Apellido del miembro.
        cedula (str): Número de cédula.
        telefono (str): Teléfono de contacto.
        correo (str): Correo electrónico.

    Retorna:
        tuple: True y mensaje si se registra correctamente.
               False y mensaje si ocurre un error.
    """
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
                estado
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            nombre.strip(),
            apellido.strip(),
            cedula.strip(),
            telefono.strip(),
            correo.strip(),
            fecha_registro,
            "activo"
        ))

        conexion.commit()

        return True, "Miembro registrado correctamente."

    except sqlite3.IntegrityError:
        return False, "La cédula ingresada ya está registrada."

    except sqlite3.Error as error:
        return False, f"Error al registrar el miembro: {error}"

    finally:
        conexion.close()