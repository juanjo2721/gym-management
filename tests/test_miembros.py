import sqlite3
import tkinter as tk
import unittest
from datetime import date
from unittest import mock

from app import database
from app.database import buscar_miembro_por_cedula, registrar_miembro
from app.vistas.miembros import abrir_ventana_miembros
from tests.test_login import BaseDatosTemporal


def obtener_miembro_completo(cedula):
    """
    Lee todas las columnas de un miembro directamente de la base temporal.
    """
    conexion = sqlite3.connect(database.DB_NAME)

    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT nombre, apellido, cedula, telefono, correo,
                   fecha_registro, estado
            FROM miembros
            WHERE cedula = ?
        """, (cedula,))

        return cursor.fetchone()

    finally:
        conexion.close()


def contar_miembros():
    conexion = sqlite3.connect(database.DB_NAME)

    try:
        return conexion.execute("SELECT COUNT(*) FROM miembros").fetchone()[0]

    finally:
        conexion.close()


class TestRegistrarMiembro(BaseDatosTemporal):

    def test_registrar_miembro_correcto(self):
        registrado, mensaje = registrar_miembro(
            "Ana", "Gomez", "1111111", "0981000000", "ana@email.com"
        )

        self.assertTrue(registrado)
        self.assertEqual(mensaje, "Miembro registrado correctamente.")

    def test_guarda_todos_los_datos(self):
        registrar_miembro(
            "Ana", "Gomez", "1111111", "0981000000", "ana@email.com"
        )

        miembro = obtener_miembro_completo("1111111")

        self.assertEqual(
            miembro[:5],
            ("Ana", "Gomez", "1111111", "0981000000", "ana@email.com")
        )

    def test_fecha_registro_es_hoy(self):
        registrar_miembro("Ana", "Gomez", "1111111", "", "")

        miembro = obtener_miembro_completo("1111111")

        self.assertEqual(miembro[5], date.today().isoformat())

    def test_estado_inicial_activo(self):
        registrar_miembro("Ana", "Gomez", "1111111", "", "")

        miembro = obtener_miembro_completo("1111111")

        self.assertEqual(miembro[6], "activo")

    def test_elimina_espacios_en_los_datos(self):
        registrar_miembro(
            "  Ana ", " Gomez  ", " 1111111 ", " 0981000000 ", " ana@email.com "
        )

        miembro = obtener_miembro_completo("1111111")

        self.assertEqual(
            miembro[:5],
            ("Ana", "Gomez", "1111111", "0981000000", "ana@email.com")
        )

    def test_telefono_y_correo_opcionales(self):
        registrado, _ = registrar_miembro("Ana", "Gomez", "1111111", "", "")

        miembro = obtener_miembro_completo("1111111")

        self.assertTrue(registrado)
        self.assertEqual(miembro[3], "")
        self.assertEqual(miembro[4], "")

    def test_cedula_duplicada(self):
        registrar_miembro("Ana", "Gomez", "1111111", "", "")
        registrado, mensaje = registrar_miembro("Otra", "Persona", "1111111", "", "")

        self.assertFalse(registrado)
        self.assertIn("cédula", mensaje)
        self.assertEqual(contar_miembros(), 1)

    def test_cedula_duplicada_con_espacios(self):
        registrar_miembro("Ana", "Gomez", "1111111", "", "")
        registrado, _ = registrar_miembro("Otra", "Persona", " 1111111 ", "", "")

        self.assertFalse(registrado)
        self.assertEqual(contar_miembros(), 1)

    def test_registrar_varios_miembros(self):
        registrar_miembro("Ana", "Gomez", "1111111", "", "")
        registrar_miembro("Luis", "Benitez", "2222222", "", "")

        self.assertEqual(contar_miembros(), 2)

    def test_error_de_base_de_datos(self):
        conexion = sqlite3.connect(database.DB_NAME)
        conexion.execute("DROP TABLE pagos_cuotas")
        conexion.execute("DROP TABLE asistencias")
        conexion.execute("DROP TABLE miembros")
        conexion.commit()
        conexion.close()

        registrado, mensaje = registrar_miembro("Ana", "Gomez", "1111111", "", "")

        self.assertFalse(registrado)
        self.assertIn("Error al registrar el miembro", mensaje)


class TestBuscarMiembroPorCedula(BaseDatosTemporal):

    def test_buscar_miembro_existente(self):
        registrar_miembro("Ana", "Gomez", "1111111", "", "")

        miembro = buscar_miembro_por_cedula("1111111")

        self.assertIsNotNone(miembro)
        self.assertEqual(miembro[1:], ("Ana", "Gomez", "1111111", "activo"))

    def test_buscar_con_espacios(self):
        registrar_miembro("Ana", "Gomez", "1111111", "", "")

        self.assertIsNotNone(buscar_miembro_por_cedula("  1111111  "))

    def test_buscar_miembro_inexistente(self):
        self.assertIsNone(buscar_miembro_por_cedula("9999999"))


class TestFormularioMiembros(unittest.TestCase):
    """
    Prueba la validación del formulario de miembros sin mostrar ventanas:
    se simulan los cuadros de mensaje y el registro en la base de datos.
    """

    CAMPOS = ("nombre", "apellido", "cedula", "telefono", "correo")

    @classmethod
    def setUpClass(cls):
        try:
            cls.raiz = tk.Tk()
        except tk.TclError:
            raise unittest.SkipTest("No hay entorno gráfico disponible.")

        cls.raiz.withdraw()

    @classmethod
    def tearDownClass(cls):
        cls.raiz.destroy()

    def setUp(self):
        parche_mensajes = mock.patch("app.vistas.miembros.messagebox")
        parche_registro = mock.patch(
            "app.vistas.miembros.registrar_miembro",
            return_value=(True, "Miembro registrado correctamente.")
        )

        self.messagebox = parche_mensajes.start()
        self.registrar = parche_registro.start()
        self.addCleanup(parche_mensajes.stop)
        self.addCleanup(parche_registro.stop)

        abrir_ventana_miembros(self.raiz)
        self.ventana = self.raiz.winfo_children()[-1]
        self.addCleanup(self.cerrar_ventana)

        widgets = self.listar_widgets(self.ventana)
        entradas = [w for w in widgets if isinstance(w, tk.Entry)]
        self.entradas = dict(zip(self.CAMPOS, entradas))
        self.botones = {
            w.cget("text"): w for w in widgets if isinstance(w, tk.Button)
        }

    def cerrar_ventana(self):
        if self.ventana.winfo_exists():
            self.ventana.destroy()

    def listar_widgets(self, widget):
        resultado = []

        for hijo in widget.winfo_children():
            resultado.append(hijo)
            resultado.extend(self.listar_widgets(hijo))

        return resultado

    def completar(self, **valores):
        for clave, valor in valores.items():
            self.entradas[clave].insert(0, valor)

    def guardar(self):
        self.botones["Guardar miembro"].invoke()

    def test_formulario_tiene_todos_los_campos(self):
        self.assertEqual(len(self.entradas), len(self.CAMPOS))
        self.assertIn("Guardar miembro", self.botones)
        self.assertIn("Limpiar", self.botones)
        self.assertIn("Cerrar", self.botones)

    def test_guardar_datos_validos(self):
        self.completar(
            nombre="Ana",
            apellido="Gomez",
            cedula="1111111",
            telefono="0981000000",
            correo="ana@email.com"
        )

        self.guardar()

        self.registrar.assert_called_once_with(
            "Ana", "Gomez", "1111111", "0981000000", "ana@email.com"
        )
        self.messagebox.showinfo.assert_called_once()

    def test_guardar_elimina_espacios(self):
        self.completar(nombre="  Ana ", apellido=" Gomez ", cedula=" 1111111 ")

        self.guardar()

        self.registrar.assert_called_once_with("Ana", "Gomez", "1111111", "", "")

    def test_registro_exitoso_limpia_formulario(self):
        self.completar(nombre="Ana", apellido="Gomez", cedula="1111111")

        self.guardar()

        for entrada in self.entradas.values():
            self.assertEqual(entrada.get(), "")

    def test_campos_obligatorios_vacios(self):
        self.guardar()

        self.messagebox.showwarning.assert_called_once()
        self.registrar.assert_not_called()

    def test_falta_cada_campo_obligatorio(self):
        datos = {"nombre": "Ana", "apellido": "Gomez", "cedula": "1111111"}

        for faltante in datos:
            with self.subTest(faltante=faltante):
                self.botones["Limpiar"].invoke()
                self.messagebox.reset_mock()
                self.completar(
                    **{clave: valor for clave, valor in datos.items() if clave != faltante}
                )

                self.guardar()

                self.messagebox.showwarning.assert_called_once()
                self.registrar.assert_not_called()

    def test_campo_obligatorio_solo_espacios(self):
        self.completar(nombre="   ", apellido="Gomez", cedula="1111111")

        self.guardar()

        self.messagebox.showwarning.assert_called_once()
        self.registrar.assert_not_called()

    def test_correo_invalido(self):
        self.completar(
            nombre="Ana", apellido="Gomez", cedula="1111111", correo="ana.email.com"
        )

        self.guardar()

        titulo = self.messagebox.showwarning.call_args[0][0]
        self.assertEqual(titulo, "Correo inválido")
        self.registrar.assert_not_called()

    def test_error_al_registrar_conserva_datos(self):
        self.registrar.return_value = (False, "La cédula ingresada ya está registrada.")
        self.completar(nombre="Ana", apellido="Gomez", cedula="1111111")

        self.guardar()

        self.messagebox.showerror.assert_called_once_with(
            "Error", "La cédula ingresada ya está registrada."
        )
        self.assertEqual(self.entradas["cedula"].get(), "1111111")

    def test_boton_limpiar(self):
        self.completar(
            nombre="Ana",
            apellido="Gomez",
            cedula="1111111",
            telefono="0981000000",
            correo="ana@email.com"
        )

        self.botones["Limpiar"].invoke()

        for entrada in self.entradas.values():
            self.assertEqual(entrada.get(), "")

    def test_boton_cerrar(self):
        self.botones["Cerrar"].invoke()

        self.assertFalse(self.ventana.winfo_exists())


if __name__ == "__main__":
    unittest.main()
