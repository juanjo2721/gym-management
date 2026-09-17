import tkinter as tk
from tkinter import messagebox


def abrir_pantalla_principal(usuario):
    ventana_principal = tk.Tk()
    ventana_principal.title("Sistema de Gestión para Gimnasio")
    ventana_principal.geometry("700x450")
    ventana_principal.resizable(False, False)

    titulo = tk.Label(
        ventana_principal,
        text="Sistema de Gestión para Gimnasio",
        font=("Arial", 20, "bold")
    )
    titulo.pack(pady=20)

    bienvenida = tk.Label(
        ventana_principal,
        text=f"Bienvenido/a, {usuario}",
        font=("Arial", 12)
    )
    bienvenida.pack(pady=5)

    frame_botones = tk.Frame(ventana_principal)
    frame_botones.pack(pady=30)

    btn_usuarios = tk.Button(frame_botones, text="Usuarios", width=20, height=2)
    btn_usuarios.grid(row=0, column=0, padx=10, pady=10)

    btn_socios = tk.Button(frame_botones, text="Socios", width=20, height=2)
    btn_socios.grid(row=0, column=1, padx=10, pady=10)

    btn_pagos = tk.Button(frame_botones, text="Pagos y Cuotas", width=20, height=2)
    btn_pagos.grid(row=1, column=0, padx=10, pady=10)

    btn_asistencia = tk.Button(frame_botones, text="Asistencia", width=20, height=2)
    btn_asistencia.grid(row=1, column=1, padx=10, pady=10)

    def cerrar_sesion():
        respuesta = messagebox.askyesno("Cerrar sesión", "¿Desea cerrar sesión?")
        if respuesta:
            ventana_principal.destroy()

    btn_cerrar = tk.Button(
        ventana_principal,
        text="Cerrar sesión",
        width=20,
        command=cerrar_sesion
    )
    btn_cerrar.pack(pady=20)

    ventana_principal.mainloop()