import unittest
from database import verificar_usuario


class TestLogin(unittest.TestCase):

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


if __name__ == "__main__":
    unittest.main()
