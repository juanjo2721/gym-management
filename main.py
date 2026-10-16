import tkinter as tk

from app.database import crear_tablas
from app.vistas.login import mostrar_login


def main():
    """
    Punto de entrada de la aplicación.

    Prepara la base de datos (crea tablas y columnas faltantes), crea la
    única ventana raíz del sistema y muestra la pantalla de login.
    """
    crear_tablas()

    ventana = tk.Tk()
    mostrar_login(ventana)
    ventana.mainloop()


if __name__ == "__main__":
    main()
