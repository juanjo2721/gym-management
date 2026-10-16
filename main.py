import tkinter as tk

from login import mostrar_login


def main():
    """
    Punto de entrada de la aplicación.

    Crea la única ventana raíz del sistema y muestra la pantalla de login.
    """
    ventana = tk.Tk()
    mostrar_login(ventana)
    ventana.mainloop()


if __name__ == "__main__":
    main()
