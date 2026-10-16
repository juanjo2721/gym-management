"""
Colores y utilidades visuales compartidas por todas las pantallas del sistema.
"""


COLOR_FONDO = "#f4f6f8"
COLOR_TARJETA = "#ffffff"
COLOR_PRINCIPAL = "#1f4e79"
COLOR_SECUNDARIO = "#eef3f8"
COLOR_BOTON = "#1f4e79"
COLOR_BOTON_TEXTO = "#ffffff"
COLOR_BOTON_LIMPIAR = "#dfe6ed"
COLOR_BOTON_CERRAR = "#eeeeee"
COLOR_TEXTO = "#222222"
COLOR_TEXTO_SUAVE = "#666666"
COLOR_TITULO_ENCABEZADO = "#ffffff"
COLOR_SUBTITULO_ENCABEZADO = "#dbe8f3"


def limpiar_ventana(ventana):
    """
    Elimina todos los widgets de la ventana para poder mostrar otra pantalla
    sin crear una nueva ventana raíz.
    """
    for widget in ventana.winfo_children():
        widget.destroy()


def centrar_ventana(ventana, ancho, alto):
    """
    Establece el tamaño de la ventana y la ubica en el centro de la pantalla.
    """
    x = (ventana.winfo_screenwidth() - ancho) // 2
    y = (ventana.winfo_screenheight() - alto) // 2
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")
