import tkinter as tk
from tkinter import messagebox


COLOR_FONDO = "#f4f6f8"
COLOR_PRINCIPAL = "#1f4e79"
COLOR_SECUNDARIO = "#eef3f8"
COLOR_TARJETA = "#ffffff"
COLOR_TEXTO = "#222222"
COLOR_TEXTO_SUAVE = "#666666"
COLOR_BOTON = "#1f4e79"
COLOR_BOTON_HOVER = "#163b5c"


def mostrar_modulo(nombre_modulo):
    """
    Muestra un mensaje informativo para los modulos que aun estan en desarrollo.
    """
    messagebox.showinfo(
        "Modulo en desarrollo",
        f"El modulo {nombre_modulo} sera desarrollado en los siguientes sprints."
    )


def abrir_pantalla_principal(usuario):
    """
    Abre la pantalla principal del sistema luego de un inicio de sesion correcto.

    Parametros:
        usuario (str): Nombre del usuario que inicio sesion.
    """
    ventana_principal = tk.Tk()
    ventana_principal.title("Sistema de Gestion para Gimnasio")
    ventana_principal.geometry("850x520")
    ventana_principal.resizable(False, False)
    ventana_principal.configure(bg=COLOR_FONDO)

    encabezado = tk.Frame(
        ventana_principal,
        bg=COLOR_PRINCIPAL,
        height=90
    )
    encabezado.pack(fill="x")

    titulo = tk.Label(
        encabezado,
        text="Sistema de Gestion para Gimnasio",
        font=("Arial", 22, "bold"),
        bg=COLOR_PRINCIPAL,
        fg="white"
    )
    titulo.pack(pady=(18, 0))

    subtitulo = tk.Label(
        encabezado,
        text="Panel principal del sistema",
        font=("Arial", 11),
        bg=COLOR_PRINCIPAL,
        fg="#dbe8f3"
    )
    subtitulo.pack(pady=(4, 0))

    contenido = tk.Frame(
        ventana_principal,
        bg=COLOR_FONDO
    )
    contenido.pack(fill="both", expand=True, padx=35, pady=25)

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
        text="Seleccione una opcion para acceder a los modulos del sistema.",
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

    def crear_boton_modulo(texto, fila, columna):
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
            command=lambda: mostrar_modulo(texto)
        )
        boton.grid(row=fila, column=columna, padx=15, pady=15)
        return boton

    crear_boton_modulo("Usuarios", 0, 0)
    crear_boton_modulo("Socios", 0, 1)
    crear_boton_modulo("Pagos y Cuotas", 1, 0)
    crear_boton_modulo("Asistencia", 1, 1)

    estado = tk.Label(
        contenido,
        text="Sprint actual: Modulo Login finalizado",
        font=("Arial", 10, "bold"),
        bg=COLOR_FONDO,
        fg=COLOR_PRINCIPAL
    )
    estado.pack(anchor="w", pady=(25, 5))

    detalle = tk.Label(
        contenido,
        text="El sistema valida credenciales desde SQLite y permite el acceso a la pantalla principal.",
        font=("Arial", 10),
        bg=COLOR_FONDO,
        fg=COLOR_TEXTO_SUAVE
    )
    detalle.pack(anchor="w")

    def cerrar_sesion():
        respuesta = messagebox.askyesno("Cerrar sesion", "Desea cerrar la sesion actual?")
        if respuesta:
            ventana_principal.destroy()

    boton_cerrar = tk.Button(
        contenido,
        text="Cerrar sesion",
        font=("Arial", 11, "bold"),
        bg=COLOR_BOTON,
        fg="white",
        width=18,
        height=2,
        borderwidth=0,
        cursor="hand2",
        command=cerrar_sesion
    )
    boton_cerrar.pack(anchor="e", pady=(25, 0))

    ventana_principal.mainloop()