import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk

from app.database import OBJETIVOS_ENTRENAMIENTO, registrar_miembro, SEXOS
from app.estilos import (
    centrar_ventana,
    COLOR_BOTON,
    COLOR_BOTON_CERRAR,
    COLOR_BOTON_LIMPIAR,
    COLOR_BOTON_TEXTO,
    COLOR_FONDO,
    COLOR_PRINCIPAL,
    COLOR_SUBTITULO_ENCABEZADO,
    COLOR_TARJETA,
    COLOR_TEXTO,
    COLOR_TEXTO_SUAVE,
    COLOR_TITULO_ENCABEZADO,
)


def leer_fecha(texto):
    """
    Convierte una fecha en formato dd/mm/aaaa a date.

    Retorna:
        date | None: La fecha, o None si el texto no es una fecha válida.
    """
    try:
        return datetime.strptime(texto.strip(), "%d/%m/%Y").date()
    except ValueError:
        return None


def abrir_ventana_miembros(ventana_principal):
    ventana = tk.Toplevel(ventana_principal)
    ventana.title("Agregar miembro")
    centrar_ventana(ventana, 960, 600)
    ventana.resizable(False, False)
    ventana.configure(bg=COLOR_FONDO)

    encabezado = tk.Frame(
        ventana,
        bg=COLOR_PRINCIPAL,
        height=90
    )
    encabezado.pack(fill="x")

    titulo = tk.Label(
        encabezado,
        text="Agregar nuevo miembro",
        font=("Arial", 21, "bold"),
        bg=COLOR_PRINCIPAL,
        fg=COLOR_TITULO_ENCABEZADO
    )
    titulo.pack(pady=(18, 4))

    subtitulo = tk.Label(
        encabezado,
        text="Complete los datos del miembro. Los campos con * son obligatorios",
        font=("Arial", 10),
        bg=COLOR_PRINCIPAL,
        fg=COLOR_SUBTITULO_ENCABEZADO
    )
    subtitulo.pack()

    formulario = tk.Frame(
        ventana,
        bg=COLOR_TARJETA,
        padx=30,
        pady=20
    )
    formulario.pack(fill="both", expand=True, padx=30, pady=25)

    entradas = {}
    combos = {}

    def crear_seccion(texto, columna):
        seccion = tk.Label(
            formulario,
            text=texto,
            font=("Arial", 12, "bold"),
            bg=COLOR_TARJETA,
            fg=COLOR_PRINCIPAL,
            anchor="w"
        )
        seccion.grid(row=0, column=columna, columnspan=2, sticky="w", pady=(0, 6))

    def crear_etiqueta(texto, fila, columna):
        etiqueta = tk.Label(
            formulario,
            text=texto,
            font=("Arial", 10, "bold"),
            bg=COLOR_TARJETA,
            fg=COLOR_TEXTO,
            anchor="w"
        )
        etiqueta.grid(row=fila, column=columna, sticky="w", padx=(0, 12), pady=5)

    def crear_entrada(texto, clave, fila, columna):
        crear_etiqueta(texto, fila, columna)

        entrada = tk.Entry(
            formulario,
            font=("Arial", 11),
            width=24
        )
        entrada.grid(row=fila, column=columna + 1, sticky="ew", pady=5, ipady=3)

        entradas[clave] = entrada

    def crear_combo(texto, clave, valores, fila, columna):
        crear_etiqueta(texto, fila, columna)

        combo = ttk.Combobox(
            formulario,
            values=valores,
            state="readonly",
            font=("Arial", 11),
            width=22
        )
        combo.grid(row=fila, column=columna + 1, sticky="ew", pady=5)

        combos[clave] = combo

    # Columna izquierda: datos personales y de contacto
    crear_seccion("Datos personales", 0)
    crear_entrada("Nombre *", "nombre", 1, 0)
    crear_entrada("Apellido *", "apellido", 2, 0)
    crear_entrada("Cédula *", "cedula", 3, 0)
    crear_entrada("Nacimiento (dd/mm/aaaa)", "fecha_nacimiento", 4, 0)
    crear_combo("Sexo", "sexo", SEXOS, 5, 0)
    crear_entrada("Teléfono", "telefono", 6, 0)
    crear_entrada("Correo electrónico", "correo", 7, 0)
    crear_entrada("Dirección", "direccion", 8, 0)

    separador = tk.Frame(formulario, bg=COLOR_FONDO, width=2)
    separador.grid(row=0, column=2, rowspan=9, sticky="ns", padx=20)

    # Columna derecha: entrenamiento, emergencia y salud
    crear_seccion("Entrenamiento y salud", 3)
    crear_combo("Objetivo", "objetivo", OBJETIVOS_ENTRENAMIENTO, 1, 3)
    crear_entrada("Contacto de emergencia", "contacto_emergencia", 2, 3)
    crear_entrada("Teléfono de emergencia", "telefono_emergencia", 3, 3)

    crear_etiqueta("Observaciones médicas", 4, 3)

    texto_observaciones = tk.Text(
        formulario,
        font=("Arial", 10),
        width=24,
        height=6,
        wrap="word"
    )
    texto_observaciones.grid(row=5, column=3, columnspan=2, rowspan=3, sticky="nsew", pady=5)

    ayuda_observaciones = tk.Label(
        formulario,
        text="Lesiones, alergias, enfermedades o medicación",
        font=("Arial", 8),
        bg=COLOR_TARJETA,
        fg=COLOR_TEXTO_SUAVE,
        anchor="w"
    )
    ayuda_observaciones.grid(row=8, column=3, columnspan=2, sticky="nw")

    formulario.columnconfigure(1, weight=1)
    formulario.columnconfigure(4, weight=1)

    def limpiar_formulario():
        for entrada in entradas.values():
            entrada.delete(0, tk.END)

        for combo in combos.values():
            combo.set("")

        texto_observaciones.delete("1.0", tk.END)
        entradas["nombre"].focus()

    def guardar_miembro():
        valores = {clave: entrada.get().strip() for clave, entrada in entradas.items()}

        if not valores["nombre"] or not valores["apellido"] or not valores["cedula"]:
            messagebox.showwarning(
                "Campos obligatorios",
                "Debe completar nombre, apellido y cédula."
            )
            return

        if valores["correo"] and "@" not in valores["correo"]:
            messagebox.showwarning(
                "Correo inválido",
                "Ingrese un correo electrónico válido."
            )
            return

        fecha_nacimiento = None

        if valores["fecha_nacimiento"]:
            fecha_nacimiento = leer_fecha(valores["fecha_nacimiento"])

            if fecha_nacimiento is None:
                messagebox.showwarning(
                    "Fecha inválida",
                    "Ingrese la fecha de nacimiento con el formato dd/mm/aaaa."
                )
                return

        registrado, mensaje = registrar_miembro(
            valores["nombre"],
            valores["apellido"],
            valores["cedula"],
            valores["telefono"],
            valores["correo"],
            fecha_nacimiento=fecha_nacimiento,
            sexo=combos["sexo"].get(),
            direccion=valores["direccion"],
            objetivo=combos["objetivo"].get(),
            contacto_emergencia=valores["contacto_emergencia"],
            telefono_emergencia=valores["telefono_emergencia"],
            observaciones_medicas=texto_observaciones.get("1.0", tk.END).strip()
        )

        if registrado:
            messagebox.showinfo("Registro exitoso", mensaje)
            limpiar_formulario()
        else:
            messagebox.showerror("Error", mensaje)

    botones = tk.Frame(
        formulario,
        bg=COLOR_TARJETA
    )
    botones.grid(
        row=9,
        column=0,
        columnspan=5,
        pady=(20, 0)
    )

    boton_guardar = tk.Button(
        botones,
        text="Guardar miembro",
        font=("Arial", 11, "bold"),
        bg=COLOR_BOTON,
        fg=COLOR_BOTON_TEXTO,
        width=18,
        height=2,
        borderwidth=0,
        cursor="hand2",
        command=guardar_miembro
    )
    boton_guardar.grid(row=0, column=0, padx=8)

    boton_limpiar = tk.Button(
        botones,
        text="Limpiar",
        font=("Arial", 11, "bold"),
        bg=COLOR_BOTON_LIMPIAR,
        fg=COLOR_PRINCIPAL,
        width=14,
        height=2,
        borderwidth=0,
        cursor="hand2",
        command=limpiar_formulario
    )
    boton_limpiar.grid(row=0, column=1, padx=8)

    boton_cerrar = tk.Button(
        botones,
        text="Cerrar",
        font=("Arial", 11, "bold"),
        bg=COLOR_BOTON_CERRAR,
        fg=COLOR_TEXTO_SUAVE,
        width=14,
        height=2,
        borderwidth=0,
        cursor="hand2",
        command=ventana.destroy
    )
    boton_cerrar.grid(row=0, column=2, padx=8)

    entradas["nombre"].focus()
