import tkinter as tk
from tkinter import messagebox

from app.database import registrar_miembro
from app.estilos import (
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


def abrir_ventana_miembros(ventana_principal):
    ventana = tk.Toplevel(ventana_principal)
    ventana.title("Agregar miembro")
    ventana.geometry("600x560")
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
        text="Complete los datos personales y de contacto",
        font=("Arial", 10),
        bg=COLOR_PRINCIPAL,
        fg=COLOR_SUBTITULO_ENCABEZADO
    )
    subtitulo.pack()

    formulario = tk.Frame(
        ventana,
        bg=COLOR_TARJETA,
        padx=35,
        pady=25
    )
    formulario.pack(fill="both", expand=True, padx=30, pady=25)

    entradas = {}

    campos = [
        ("Nombre", "nombre"),
        ("Apellido", "apellido"),
        ("Cédula", "cedula"),
        ("Teléfono", "telefono"),
        ("Correo electrónico", "correo")
    ]

    for fila, (texto, clave) in enumerate(campos):
        etiqueta = tk.Label(
            formulario,
            text=texto,
            font=("Arial", 11, "bold"),
            bg=COLOR_TARJETA,
            fg=COLOR_TEXTO,
            anchor="w"
        )
        etiqueta.grid(
            row=fila,
            column=0,
            sticky="w",
            padx=(0, 15),
            pady=8
        )

        entrada = tk.Entry(
            formulario,
            font=("Arial", 11),
            width=35
        )
        entrada.grid(
            row=fila,
            column=1,
            sticky="ew",
            pady=8,
            ipady=5
        )

        entradas[clave] = entrada

    formulario.columnconfigure(1, weight=1)

    def limpiar_formulario():
        for entrada in entradas.values():
            entrada.delete(0, tk.END)

        entradas["nombre"].focus()

    def guardar_miembro():
        nombre = entradas["nombre"].get().strip()
        apellido = entradas["apellido"].get().strip()
        cedula = entradas["cedula"].get().strip()
        telefono = entradas["telefono"].get().strip()
        correo = entradas["correo"].get().strip()

        if not nombre or not apellido or not cedula:
            messagebox.showwarning(
                "Campos obligatorios",
                "Debe completar nombre, apellido y cédula."
            )
            return

        if correo and "@" not in correo:
            messagebox.showwarning(
                "Correo inválido",
                "Ingrese un correo electrónico válido."
            )
            return

        registrado, mensaje = registrar_miembro(
            nombre,
            apellido,
            cedula,
            telefono,
            correo
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
        row=len(campos),
        column=0,
        columnspan=2,
        pady=(25, 0)
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