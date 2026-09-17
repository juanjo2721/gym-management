import sqlite3

DB_NAME = "gym_management.db"


def conectar():
    """
    Establece la conexion con la base de datos SQLite.

    Retorna:
        sqlite3.Connection: Objeto de conexion a la base de datos.
    """
    conexion = sqlite3.connect(DB_NAME)
    return conexion


def verificar_usuario(usuario, contrasena):
    """
    Verifica las credenciales ingresadas por el usuario.

    Recibe un nombre de usuario y una contrasena. Luego consulta la tabla
    usuarios para comprobar si existe un usuario activo con esas credenciales.

    Parametros:
        usuario (str): Nombre de usuario ingresado en el login.
        contrasena (str): Contrasena ingresada en el login.

    Retorna:
        tuple | None: Retorna los datos del usuario si las credenciales son
        correctas. En caso contrario, retorna None.
    """
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT *
        FROM usuarios
        WHERE usuario = ?
        AND contrasena = ?
        AND estado = 'activo'
    """, (usuario, contrasena))

    resultado = cursor.fetchone()

    conexion.close()
    return resultado