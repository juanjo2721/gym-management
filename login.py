import tkinter as tk
from tkinter import messagebox
from database import verificar_usuario
from pantalla_principal import abrir_pantalla_principal


COLOR_FONDO = "#f4f6f8"
COLOR_TARJETA = "#ffffff"
COLOR_PRINCIPAL = "#1f4e79"
COLOR_BOTON = "#1f4e79"
COLOR_BOTON_TEXTO = "#ffffff"
COLOR_TEXTO = "#222222"
COLOR_SECUNDARIO = "#666666"


def iniciar_sesion():
    usuario = entrada_usuario.get().strip()
    contrasena = entrada_contrasena.get().strip()

    if usuario == "" or contrasena == "":
        messagebox.showwarning("Campos vacios", "Debe ingresar usuario y contrasena.")
        return

    resultado = verificar_usuario(usuario, contrasena)

    if resultado:
        messagebox.showinfo("Acceso correcto", "Bienvenido al sistema.")
        ventana.destroy()
        abrir_pantalla_principal(usuario)
    else:
        messagebox.showerror("Error", "Usuario o contrasena incorrectos.")


ventana = tk.Tk()
ventana.title("Sistema de Gestion para Gimnasio")
ventana.geometry("500x420")
ventana.resizable(False, False)
ventana.configure(bg=COLOR_FONDO)

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
    fg=COLOR_SECUNDARIO
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
    fg=COLOR_SECUNDARIO
)
pie.pack(pady=(20, 0))

ventana.mainloop()