import sqlite3
import tkinter as tk
import unittest
from datetime import date, timedelta
from tkinter import ttk
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


class TestCamposAdicionalesMiembro(BaseDatosTemporal):

    def leer_campos_adicionales(self, cedula):
        conexion = sqlite3.connect(database.DB_NAME)

        try:
            return conexion.execute("""
                SELECT fecha_nacimiento, sexo, direccion, objetivo,
                       contacto_emergencia, telefono_emergencia,
                       observaciones_medicas
                FROM miembros
                WHERE cedula = ?
            """, (cedula,)).fetchone()

        finally:
            conexion.close()

    def test_guarda_campos_adicionales(self):
        registrado, _ = registrar_miembro(
            "Ana", "Gomez", "1111111", "", "",
            fecha_nacimiento=date(1995, 4, 12),
            sexo="Femenino",
            direccion=" Av. España 123 ",
            objetivo="Ganar masa muscular",
            contacto_emergencia="Luis Gomez",
            telefono_emergencia="0981111111",
            observaciones_medicas="Lesión de rodilla"
        )

        self.assertTrue(registrado)
        self.assertEqual(
            self.leer_campos_adicionales("1111111"),
            ("1995-04-12", "Femenino", "Av. España 123", "Ganar masa muscular",
             "Luis Gomez", "0981111111", "Lesión de rodilla")
        )

    def test_campos_adicionales_opcionales(self):
        registrar_miembro("Ana", "Gomez", "1111111", "", "")

        campos = self.leer_campos_adicionales("1111111")

        self.assertIsNone(campos[0])
        self.assertEqual(campos[1:], ("", "", "", "", "", ""))

    def test_fecha_nacimiento_futura(self):
        registrado, _ = registrar_miembro(
            "Ana", "Gomez", "1111111", "", "",
            fecha_nacimiento=date.today() + timedelta(days=1)
        )

        self.assertFalse(registrado)
        self.assertEqual(contar_miembros(), 0)

    def test_sexo_invalido(self):
        registrado, _ = registrar_miembro("Ana", "Gomez", "1111111", "", "", sexo="X")
        self.assertFalse(registrado)

    def test_objetivo_invalido(self):
        registrado, _ = registrar_miembro(
            "Ana", "Gomez", "1111111", "", "", objetivo="Otro más"
        )
        self.assertFalse(registrado)

    def test_migra_base_existente_sin_perder_datos(self):
        conexion = sqlite3.connect(database.DB_NAME)
        conexion.executescript("""
            DROP TABLE pagos_cuotas;
            DROP TABLE asistencias;
            DROP TABLE miembros;
            CREATE TABLE miembros (
                id_miembro INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL,
                cedula TEXT NOT NULL UNIQUE,
                telefono TEXT,
                correo TEXT,
                fecha_registro TEXT NOT NULL,
                estado TEXT NOT NULL
            );
            INSERT INTO miembros (
                nombre, apellido, cedula, telefono, correo, fecha_registro, estado
            )
            VALUES ('Vieja', 'Base', '5555555', '', '', '2026-01-01', 'activo');
        """)
        conexion.close()

        database.crear_tablas()

        self.assertIsNotNone(buscar_miembro_por_cedula("5555555"))
        registrado, _ = registrar_miembro(
            "Ana", "Gomez", "1111111", "", "", objetivo="Bajar de peso"
        )
        self.assertTrue(registrado)
        self.assertEqual(self.leer_campos_adicionales("1111111")[3], "Bajar de peso")


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

    CAMPOS = (
        "nombre",
        "apellido",
        "cedula",
        "fecha_nacimiento",
        "telefono",
        "correo",
        "direccion",
        "contacto_emergencia",
        "telefono_emergencia",
    )

    COMBOS = ("sexo", "objetivo")

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
        entradas = [w for w in widgets if type(w) is tk.Entry]
        combos = [w for w in widgets if isinstance(w, ttk.Combobox)]
        self.entradas = dict(zip(self.CAMPOS, entradas))
        self.combos = dict(zip(self.COMBOS, combos))
        self.observaciones = next(w for w in widgets if isinstance(w, tk.Text))
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

    def llamada_esperada(self, nombre, apellido, cedula, telefono="", correo="", **adicionales):
        datos = {
            "fecha_nacimiento": None,
            "sexo": "",
            "direccion": "",
            "objetivo": "",
            "contacto_emergencia": "",
            "telefono_emergencia": "",
            "observaciones_medicas": "",
        }
        datos.update(adicionales)

        return mock.call(nombre, apellido, cedula, telefono, correo, **datos)

    def test_formulario_tiene_todos_los_campos(self):
        self.assertEqual(len(self.entradas), len(self.CAMPOS))
        self.assertEqual(len(self.combos), len(self.COMBOS))
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

        self.assertEqual(
            self.registrar.call_args,
            self.llamada_esperada("Ana", "Gomez", "1111111", "0981000000", "ana@email.com")
        )
        self.messagebox.showinfo.assert_called_once()

    def test_guardar_campos_adicionales(self):
        self.completar(
            nombre="Ana",
            apellido="Gomez",
            cedula="1111111",
            fecha_nacimiento="12/04/1995",
            direccion="Av. España 123",
            contacto_emergencia="Luis Gomez",
            telefono_emergencia="0981111111"
        )
        self.combos["sexo"].set("Femenino")
        self.combos["objetivo"].set("Bajar de peso")
        self.observaciones.insert("1.0", "  Asma leve \n")

        self.guardar()

        self.assertEqual(
            self.registrar.call_args,
            self.llamada_esperada(
                "Ana", "Gomez", "1111111",
                fecha_nacimiento=date(1995, 4, 12),
                sexo="Femenino",
                direccion="Av. España 123",
                objetivo="Bajar de peso",
                contacto_emergencia="Luis Gomez",
                telefono_emergencia="0981111111",
                observaciones_medicas="Asma leve"
            )
        )

    def test_fecha_nacimiento_invalida(self):
        self.completar(
            nombre="Ana", apellido="Gomez", cedula="1111111", fecha_nacimiento="1995-04-12"
        )

        self.guardar()

        titulo = self.messagebox.showwarning.call_args[0][0]
        self.assertEqual(titulo, "Fecha inválida")
        self.registrar.assert_not_called()

    def test_guardar_elimina_espacios(self):
        self.completar(nombre="  Ana ", apellido=" Gomez ", cedula=" 1111111 ")

        self.guardar()

        self.assertEqual(
            self.registrar.call_args,
            self.llamada_esperada("Ana", "Gomez", "1111111")
        )

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

        self.combos["objetivo"].set("Bajar de peso")
        self.observaciones.insert("1.0", "Asma leve")

        self.botones["Limpiar"].invoke()

        for entrada in self.entradas.values():
            self.assertEqual(entrada.get(), "")

        self.assertEqual(self.combos["objetivo"].get(), "")
        self.assertEqual(self.observaciones.get("1.0", tk.END).strip(), "")

    def test_boton_cerrar(self):
        self.botones["Cerrar"].invoke()

        self.assertFalse(self.ventana.winfo_exists())


if __name__ == "__main__":
    unittest.main()
