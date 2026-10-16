import os
import sqlite3
import tempfile
import unittest

from app import database
from app.database import verificar_usuario


class BaseDatosTemporal(unittest.TestCase):
    """
    Crea una base de datos temporal para cada prueba, de modo que los tests
    no dependan ni modifiquen gym_management.db.
    """

    def setUp(self):
        descriptor, self.ruta_db = tempfile.mkstemp(suffix=".db")
        os.close(descriptor)

        self.db_original = database.DB_NAME
        database.DB_NAME = self.ruta_db
        database.crear_tablas()

        conexion = sqlite3.connect(self.ruta_db)
        conexion.executemany("""
            INSERT INTO usuarios (nombre, usuario, contrasena, rol, estado)
            VALUES (?, ?, ?, ?, ?)
        """, [
            ("Administrador", "admin", "admin123", "administrador", "activo"),
            ("Ex empleado", "inactivo", "clave123", "recepcionista", "inactivo"),
        ])
        conexion.commit()
        conexion.close()

    def tearDown(self):
        database.DB_NAME = self.db_original
        os.remove(self.ruta_db)


class TestLogin(BaseDatosTemporal):

    def test_login_correcto(self):
        resultado = verificar_usuario("admin", "admin123")
        self.assertIsNotNone(resultado)

    def test_login_contrasena_incorrecta(self):
        resultado = verificar_usuario("admin", "incorrecta")
        self.assertIsNone(resultado)

    def test_login_usuario_inexistente(self):
        resultado = verificar_usuario("usuariofalso", "admin123")
        self.assertIsNone(resultado)

    def test_campos_vacios(self):
        resultado = verificar_usuario("", "")
        self.assertIsNone(resultado)

    def test_login_usuario_inactivo(self):
        resultado = verificar_usuario("inactivo", "clave123")
        self.assertIsNone(resultado)


if __name__ == "__main__":
    unittest.main()
