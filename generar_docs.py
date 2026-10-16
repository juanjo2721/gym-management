"""
Genera la documentación HTML de los módulos con pydoc.

pydoc incluye la ruta absoluta de cada archivo (por ejemplo c:\\users\\...),
que cambia según la computadora de quien la genera. Este script reemplaza
esa ruta por el nombre relativo del archivo.

Uso:
    python generar_docs.py
"""

import os
import pydoc
import re


MODULOS = ["database", "miembros", "pagos", "estilos"]


def generar_documentacion():
    for modulo in MODULOS:
        pydoc.writedoc(modulo)

        ruta_html = f"{modulo}.html"

        with open(ruta_html, encoding="utf-8") as archivo:
            contenido = archivo.read()

        contenido = re.sub(
            r'<a href="file:[^"]*">[^<]*</a>',
            f'<a href="{modulo}.py">{modulo}.py</a>',
            contenido
        )

        with open(ruta_html, "w", encoding="utf-8") as archivo:
            archivo.write(contenido)


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    generar_documentacion()
