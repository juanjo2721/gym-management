import tkinter as tk
from tkinter import messagebox

from app.estilos import (
    centrar_ventana,
    COLOR_FONDO,
    COLOR_PRINCIPAL,
    COLOR_SECUNDARIO,
    COLOR_SUBTITULO_ENCABEZADO,
    COLOR_TARJETA,
    COLOR_TEXTO,
    COLOR_TEXTO_SUAVE,
    COLOR_TITULO_ENCABEZADO,
    limpiar_ventana,
)
from app.vistas.miembros import abrir_ventana_miembros
from app.vistas.pagos import abrir_ventana_pagos


def mostrar_modulo(nombre_modulo):
    """
    Muestra un mensaje informativo para los módulos que aún están en desarrollo.
    """
    messagebox.showinfo(
        "Módulo en desarrollo",
        f"El módulo {nombre_modulo} será desarrollado en los siguientes sprints."
    )


def mostrar_pantalla_principal(ventana_principal, usuario, al_cerrar_sesion):
    """
    Muestra la pantalla principal del sistema después de iniciar sesión.
    """
    limpiar_ventana(ventana_principal)

    ventana_principal.title("Sistema de Gestión para Gimnasio")
    centrar_ventana(ventana_principal, 850, 520)
    ventana_principal.resizable(False, False)
    ventana_principal.configure(bg=COLOR_FONDO)

    encabezado = tk.Frame(
        ventana_principal,
        bg=COLOR_PRINCIPAL,
        height=90
    )
    encabezado.pack(fill="x")

    def cerrar_sesion():
        respuesta = messagebox.askyesno(
            "Cerrar sesión",
            "¿Desea cerrar la sesión actual?"
        )

        if respuesta:
            al_cerrar_sesion()

    boton_cerrar = tk.Button(
        encabezado,
        text="Cerrar sesión",
        font=("Arial", 10, "bold"),
        bg=COLOR_SUBTITULO_ENCABEZADO,
        fg=COLOR_PRINCIPAL,
        width=14,
        borderwidth=0,
        cursor="hand2",
        command=cerrar_sesion
    )
    boton_cerrar.place(relx=1, rely=0.5, x=-20, anchor="e")

    titulo = tk.Label(
        encabezado,
        text="Sistema de Gestión para Gimnasio",
        font=("Arial", 22, "bold"),
        bg=COLOR_PRINCIPAL,
        fg=COLOR_TITULO_ENCABEZADO
    )
    titulo.pack(pady=(18, 0))

    subtitulo = tk.Label(
        encabezado,
        text="Panel principal del sistema",
        font=("Arial", 11),
        bg=COLOR_PRINCIPAL,
        fg=COLOR_SUBTITULO_ENCABEZADO
    )
    subtitulo.pack(pady=(4, 0))

    contenido = tk.Frame(
        ventana_principal,
        bg=COLOR_FONDO
    )
    contenido.pack(
        fill="both",
        expand=True,
        padx=35,
        pady=25
    )

    bienvenida = tk.Label(
        contenido,
        text=f"Bienvenido/a, {usuario}",
        font=("Arial", 14, "bold"),
        bg=COLOR_FONDO,
        fg=COLOR_TEXTO
    )
    bienvenida.pack(anchor="w")

    descripcion = tk.Label(
        contenido,
        text="Seleccione una opción para acceder a los módulos del sistema.",
        font=("Arial", 10),
        bg=COLOR_FONDO,
        fg=COLOR_TEXTO_SUAVE
    )
    descripcion.pack(anchor="w", pady=(4, 20))

    panel = tk.Frame(
        contenido,
        bg=COLOR_TARJETA,
        padx=30,
        pady=25
    )
    panel.pack(fill="x")

    panel_botones = tk.Frame(
        panel,
        bg=COLOR_TARJETA
    )
    panel_botones.pack(anchor="center")

    def crear_boton_modulo(texto, fila, columna, comando=None):
        boton = tk.Button(
            panel_botones,
            text=texto,
            font=("Arial", 12, "bold"),
            bg=COLOR_SECUNDARIO,
            fg=COLOR_PRINCIPAL,
            width=24,
            height=3,
            borderwidth=0,
            cursor="hand2",
            command=comando or (
                lambda: mostrar_modulo(texto)
            )
        )

        boton.grid(
            row=fila,
            column=columna,
            padx=15,
            pady=15
        )

        return boton

    crear_boton_modulo("Usuarios", 0, 0)

    crear_boton_modulo(
        "Miembros",
        0,
        1,
        lambda: abrir_ventana_miembros(ventana_principal)
    )

    crear_boton_modulo(
        "Pagos y Cuotas",
        1,
        0,
        lambda: abrir_ventana_pagos(ventana_principal)
    )

    crear_boton_modulo("Asistencia", 1, 1)

    estado = tk.Label(
        contenido,
        text="Sprint actual: Módulo Pagos y Cuotas en desarrollo",
        font=("Arial", 10, "bold"),
        bg=COLOR_FONDO,
        fg=COLOR_PRINCIPAL
    )
    estado.pack(anchor="w", pady=(25, 5))

    detalle = tk.Label(
        contenido,
        text=(
            "El sistema valida credenciales desde SQLite "
            "y permite gestionar los miembros y sus pagos."
        ),
        font=("Arial", 10),
        bg=COLOR_FONDO,
        fg=COLOR_TEXTO_SUAVE
    )
    detalle.pack(anchor="w")
