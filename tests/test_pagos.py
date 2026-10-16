import unittest
from datetime import date, timedelta

from app.database import (
    actualizar_pagos_vencidos,
    buscar_miembro_por_cedula,
    calcular_fecha_vencimiento,
    listar_pagos,
    obtener_tipos_membresia,
    registrar_miembro,
    registrar_pago,
)
from tests.test_login import BaseDatosTemporal


class TestCalculoVencimiento(unittest.TestCase):

    def test_vencimiento_en_dias(self):
        resultado = calcular_fecha_vencimiento(date(2026, 9, 14), 15, "dias")
        self.assertEqual(resultado, date(2026, 9, 29))

    def test_vencimiento_mensual(self):
        resultado = calcular_fecha_vencimiento(date(2026, 9, 17), 1, "meses")
        self.assertEqual(resultado, date(2026, 10, 17))

    def test_vencimiento_fin_de_mes(self):
        resultado = calcular_fecha_vencimiento(date(2026, 1, 31), 1, "meses")
        self.assertEqual(resultado, date(2026, 2, 28))

    def test_vencimiento_cambio_de_anio(self):
        resultado = calcular_fecha_vencimiento(date(2026, 11, 15), 3, "meses")
        self.assertEqual(resultado, date(2027, 2, 15))

    def test_unidad_invalida(self):
        with self.assertRaises(ValueError):
            calcular_fecha_vencimiento(date(2026, 1, 1), 1, "semanas")


class TestPagos(BaseDatosTemporal):

    def setUp(self):
        super().setUp()
        registrar_miembro("Ana", "Gomez", "1111111", "", "")
        self.id_miembro = buscar_miembro_por_cedula("1111111")[0]
        self.tipos = {tipo[1]: tipo for tipo in obtener_tipos_membresia()}

    def test_tipos_membresia_iniciales(self):
        self.assertIn("Mensual", self.tipos)
        self.assertEqual(self.tipos["Mensual"][4], 150000)

    def test_buscar_miembro_inexistente(self):
        self.assertIsNone(buscar_miembro_por_cedula("9999999"))

    def test_registrar_pago_calcula_vencimiento(self):
        registrado, _ = registrar_pago(
            self.id_miembro,
            self.tipos["Mensual"][0],
            150000,
            date(2026, 9, 17),
            "pagado"
        )
        self.assertTrue(registrado)

        pago = listar_pagos(id_miembro=self.id_miembro)[0]
        self.assertEqual(pago[3], "Mensual")
        self.assertEqual(pago[7], "2026-10-17")
        self.assertEqual(pago[8], "pagado")

    def test_registrar_pago_estado_invalido(self):
        registrado, _ = registrar_pago(
            self.id_miembro, self.tipos["Mensual"][0], 150000, date.today(), "otro"
        )
        self.assertFalse(registrado)

    def test_registrar_pago_monto_invalido(self):
        registrado, _ = registrar_pago(
            self.id_miembro, self.tipos["Mensual"][0], 0, date.today(), "pagado"
        )
        self.assertFalse(registrado)

    def test_registrar_pago_miembro_inexistente(self):
        registrado, _ = registrar_pago(
            9999, self.tipos["Mensual"][0], 150000, date.today(), "pagado"
        )
        self.assertFalse(registrado)

    def test_pendiente_pasa_a_vencido(self):
        inicio_pasado = date.today() - timedelta(days=40)
        registrar_pago(
            self.id_miembro, self.tipos["Mensual"][0], 150000, inicio_pasado, "pendiente"
        )
        registrar_pago(
            self.id_miembro, self.tipos["Mensual"][0], 150000, date.today(), "pendiente"
        )

        actualizados = actualizar_pagos_vencidos()
        estados = sorted(pago[8] for pago in listar_pagos(id_miembro=self.id_miembro))

        self.assertEqual(actualizados, 1)
        self.assertEqual(estados, ["pendiente", "vencido"])


if __name__ == "__main__":
    unittest.main()
