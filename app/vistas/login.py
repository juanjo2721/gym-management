import tkinter as tk
from tkinter import messagebox

from app.database import verificar_usuario
from app.estilos import (
    centrar_ventana,
    COLOR_BOTON,
    COLOR_BOTON_TEXTO,
    COLOR_FONDO,
    COLOR_PRINCIPAL,
    COLOR_TARJETA,
    COLOR_TEXTO,
    COLOR_TEXTO_SUAVE,
    limpiar_ventana,
)
from app.vistas.pantalla_principal import mostrar_pantalla_principal


def mostrar_login(ventana):
    """
    Muestra la pantalla de inicio de sesión dentro de la ventana recibida.
    """
    limpiar_ventana(ventana)

    ventana.title("Sistema de Gestion para Gimnasio")
    centrar_ventana(ventana, 500, 420)
    ventana.resizable(False, False)
    ventana.configure(bg=COLOR_FONDO)

    def iniciar_sesion(event=None):
        usuario = entrada_usuario.get().strip()
        contrasena = entrada_contrasena.get().strip()

        if usuario == "" or contrasena == "":
            messagebox.showwarning("Campos vacios", "Debe ingresar usuario y contrasena.")
            return

        resultado = verificar_usuario(usuario, contrasena)

        if resultado:
            messagebox.showinfo("Acceso correcto", "Bienvenido al sistema.")
            mostrar_pantalla_principal(
                ventana,
                usuario,
                al_cerrar_sesion=lambda: mostrar_login(ventana)
            )
        else:
            messagebox.showerror("Error", "Usuario o contrasena incorrectos.")

    contenedor = tk.Frame(
        ventana,
        bg=COLOR_TARJETA,
        padx=40,
        pady=35
    )
    contenedor.place(relx=0.5, rely=0.5, anchor="center")

    titulo = tk.Label(
        contenedor,
        text="Sistema de Gestion",
        font=("Arial", 20, "bold"),
        bg=COLOR_TARJETA,
        fg=COLOR_PRINCIPAL
    )
    titulo.pack(pady=(0, 5))

    subtitulo = tk.Label(
        contenedor,
        text="Gimnasio",
        font=("Arial", 13),
        bg=COLOR_TARJETA,
        fg=COLOR_TEXTO_SUAVE
    )
    subtitulo.pack(pady=(0, 25))

    label_usuario = tk.Label(
        contenedor,
        text="Usuario",
        font=("Arial", 11, "bold"),
        bg=COLOR_TARJETA,
        fg=COLOR_TEXTO,
        anchor="w"
    )
    label_usuario.pack(fill="x")

    entrada_usuario = tk.Entry(
        contenedor,
        font=("Arial", 12),
        width=30
    )
    entrada_usuario.pack(pady=(5, 15), ipady=6)

    label_contrasena = tk.Label(
        contenedor,
        text="Contrasena",
        font=("Arial", 11, "bold"),
        bg=COLOR_TARJETA,
        fg=COLOR_TEXTO,
        anchor="w"
    )
    label_contrasena.pack(fill="x")

    entrada_contrasena = tk.Entry(
        contenedor,
        font=("Arial", 12),
        width=30,
        show="*"
    )
    entrada_contrasena.pack(pady=(5, 25), ipady=6)
    entrada_contrasena.bind("<Return>", iniciar_sesion)

    boton_login = tk.Button(
        contenedor,
        text="Ingresar",
        font=("Arial", 12, "bold"),
        bg=COLOR_BOTON,
        fg=COLOR_BOTON_TEXTO,
        width=25,
        height=2,
        borderwidth=0,
        cursor="hand2",
        command=iniciar_sesion
    )
    boton_login.pack()

    pie = tk.Label(
        contenedor,
        text="Acceso exclusivo para usuarios autorizados",
        font=("Arial", 9),
        bg=COLOR_TARJETA,
        fg=COLOR_TEXTO_SUAVE
    )
    pie.pack(pady=(20, 0))

    entrada_usuario.focus()
