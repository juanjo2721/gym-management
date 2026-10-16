import sqlite3
from datetime import date


DB_NAME = "gym_management.db"


def conectar():
    """
    Establece la conexión con la base de datos SQLite.

    Retorna:
        sqlite3.Connection: Objeto de conexión a la base de datos.
    """
    return sqlite3.connect(DB_NAME)


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