import unittest

from app.database import (
    actualizar_tipo_membresia,
    cambiar_estado_tipo_membresia,
    crear_tipo_membresia,
    listar_tipos_membresia,
    obtener_tipos_membresia,
)
from tests.test_login import BaseDatosTemporal


class TestConfiguracionTiposMembresia(BaseDatosTemporal):

    def buscar_tipo(self, nombre):
        for tipo in listar_tipos_membresia():
            if tipo[1] == nombre:
                return tipo
        return None

    def test_crear_tipo_semanal(self):
        creado, _ = crear_tipo_membresia("Semanal", 7, "dias", 50000)
        self.assertTrue(creado)

        tipo = self.buscar_tipo("Semanal")
        self.assertEqual(tipo[2:], (7, "dias", 50000, "activo"))

    def test_crear_tipo_nombre_duplicado(self):
        creado, _ = crear_tipo_membresia("Mensual", 1, "meses", 150000)
        self.assertFalse(creado)

    def test_crear_tipo_datos_invalidos(self):
        self.assertFalse(crear_tipo_membresia("", 7, "dias", 50000)[0])
        self.assertFalse(crear_tipo_membresia("Semanal", 0, "dias", 50000)[0])
        self.assertFalse(crear_tipo_membresia("Semanal", 1, "semanas", 50000)[0])
        self.assertFalse(crear_tipo_membresia("Semanal", 7, "dias", 0)[0])

    def test_actualizar_precio(self):
        mensual = self.buscar_tipo("Mensual")
        actualizado, _ = actualizar_tipo_membresia(mensual[0], "Mensual", 1, "meses", 180000)
        self.assertTrue(actualizado)
        self.assertEqual(self.buscar_tipo("Mensual")[4], 180000)

    def test_actualizar_con_nombre_de_otro_tipo(self):
        mensual = self.buscar_tipo("Mensual")
        actualizado, _ = actualizar_tipo_membresia(mensual[0], "Anual", 1, "meses", 150000)
        self.assertFalse(actualizado)

    def test_actualizar_tipo_inexistente(self):
        actualizado, _ = actualizar_tipo_membresia(9999, "Otro", 1, "meses", 150000)
        self.assertFalse(actualizado)

    def test_desactivar_oculta_en_pagos(self):
        diaria = self.buscar_tipo("Diaria")
        cambiado, _ = cambiar_estado_tipo_membresia(diaria[0], "inactivo")
        self.assertTrue(cambiado)

        nombres_activos = [tipo[1] for tipo in obtener_tipos_membresia()]
        self.assertNotIn("Diaria", nombres_activos)
        self.assertEqual(self.buscar_tipo("Diaria")[5], "inactivo")

        cambiar_estado_tipo_membresia(diaria[0], "activo")
        self.assertIn("Diaria", [tipo[1] for tipo in obtener_tipos_membresia()])

    def test_cambiar_estado_invalido(self):
        diaria = self.buscar_tipo("Diaria")
        self.assertFalse(cambiar_estado_tipo_membresia(diaria[0], "borrado")[0])


if __name__ == "__main__":
    unittest.main()
