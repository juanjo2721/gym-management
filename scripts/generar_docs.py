"""
Genera la documentación HTML de los módulos con pydoc dentro de docs/.

pydoc incluye la ruta absoluta de cada archivo (por ejemplo c:\\users\\...),
que cambia según la computadora de quien la genera. Este script reemplaza
esa ruta por la ruta relativa del archivo.

Uso:
    python scripts/generar_docs.py
"""

import os
import pydoc
import re
import sys


RAIZ_PROYECTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CARPETA_DOCS = os.path.join(RAIZ_PROYECTO, "docs")

MODULOS = [
    "app.database",
    "app.estilos",
    "app.vistas.miembros",
    "app.vistas.pagos",
    "app.vistas.configuracion",
]


def generar_documentacion():
    for modulo in MODULOS:
        pydoc.writedoc(modulo)

        nombre_corto = modulo.split(".")[-1]
        ruta_html = f"{nombre_corto}.html"
        ruta_fuente = "../" + modulo.replace(".", "/") + ".py"

        os.replace(f"{modulo}.html", ruta_html)

        with open(ruta_html, encoding="utf-8") as archivo:
            contenido = archivo.read()

        contenido = re.sub(
            r'<a href="file:[^"]*">[^<]*</a>',
            f'<a href="{ruta_fuente}">{ruta_fuente[3:]}</a>',
            contenido
        )

        with open(ruta_html, "w", encoding="utf-8") as archivo:
            archivo.write(contenido)


if __name__ == "__main__":
    sys.path.insert(0, RAIZ_PROYECTO)
    os.chdir(CARPETA_DOCS)
    generar_documentacion()
