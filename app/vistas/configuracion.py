import tkinter as tk
from tkinter import messagebox, ttk

from app.database import (
    actualizar_tipo_membresia,
    cambiar_estado_tipo_membresia,
    crear_tipo_membresia,
    listar_tipos_membresia,
    UNIDADES_DURACION,
)
from app.estilos import (
    centrar_ventana,
    COLOR_BOTON,
    COLOR_BOTON_CERRAR,
    COLOR_BOTON_LIMPIAR,
    COLOR_BOTON_TEXTO,
    COLOR_FONDO,
    COLOR_PRINCIPAL,
    COLOR_SUBTITULO_ENCABEZADO,
    COLOR_TARJETA,
    COLOR_TEXTO,
    COLOR_TEXTO_SUAVE,
    COLOR_TITULO_ENCABEZADO,
)
from app.vistas.pagos import formatear_monto


COLOR_INACTIVO = "#eeeeee"


def formatear_duracion(cantidad, unidad):
    """
    Describe la duración de una membresía (1, 'meses' -> '1 mes').
    """
    if unidad == "meses":
        return f"{cantidad} {'mes' if cantidad == 1 else 'meses'}"

    return f"{cantidad} {'día' if cantidad == 1 else 'días'}"


def abrir_ventana_configuracion(ventana_principal):
    ventana = tk.Toplevel(ventana_principal)
    ventana.title("Configuración")
    centrar_ventana(ventana, 760, 700)
    ventana.resizable(False, False)
    ventana.configure(bg=COLOR_FONDO)

    tipos_por_id = {}
    tipo_seleccionado = {"id": None}

    encabezado = tk.Frame(
        ventana,
        bg=COLOR_PRINCIPAL,
        height=90
    )
    encabezado.pack(fill="x")

    titulo = tk.Label(
        encabezado,
        text="Configuración",
        font=("Arial", 21, "bold"),
        bg=COLOR_PRINCIPAL,
        fg=COLOR_TITULO_ENCABEZADO
    )
    titulo.pack(pady=(18, 4))

    subtitulo = tk.Label(
        encabezado,
        text="Tipos de membresía, duraciones y precios",
        font=("Arial", 10),
        bg=COLOR_PRINCIPAL,
        fg=COLOR_SUBTITULO_ENCABEZADO
    )
    subtitulo.pack(pady=(0, 14))

    formulario = tk.Frame(
        ventana,
        bg=COLOR_TARJETA,
        padx=30,
        pady=18
    )
    formulario.pack(fill="x", padx=30, pady=(20, 10))

    label_modo = tk.Label(
        formulario,
        text="Nuevo tipo de membresía",
        font=("Arial", 12, "bold"),
        bg=COLOR_TARJETA,
        fg=COLOR_PRINCIPAL,
        anchor="w"
    )
    label_modo.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 8))

    def crear_etiqueta(texto, fila):
        etiqueta = tk.Label(
            formulario,
            text=texto,
            font=("Arial", 11, "bold"),
            bg=COLOR_TARJETA,
            fg=COLOR_TEXTO,
            anchor="w"
        )
        etiqueta.grid(row=fila, column=0, sticky="w", padx=(0, 15), pady=6)

    # Nombre
    crear_etiqueta("Nombre", 1)

    entrada_nombre = tk.Entry(
        formulario,
        font=("Arial", 11),
        width=22
    )
    entrada_nombre.grid(row=1, column=1, columnspan=2, sticky="w", pady=6, ipady=4)

    # Duración
    crear_etiqueta("Duración", 2)

    entrada_cantidad = tk.Entry(
        formulario,
        font=("Arial", 11),
        width=8
    )
    entrada_cantidad.grid(row=2, column=1, sticky="w", pady=6, ipady=4)

    combo_unidad = ttk.Combobox(
        formulario,
        values=UNIDADES_DURACION,
        state="readonly",
        font=("Arial", 11),
        width=10
    )
    combo_unidad.grid(row=2, column=2, sticky="w", padx=(10, 0), pady=6)

    # Precio
    crear_etiqueta("Precio (Gs.)", 3)

    entrada_precio = tk.Entry(
        formulario,
        font=("Arial", 11),
        width=22
    )
    entrada_precio.grid(row=3, column=1, columnspan=2, sticky="w", pady=6, ipady=4)

    ayuda = tk.Label(
        formulario,
        text=(
            "Ejemplo: semanal = 7 días. Cambiar el precio no modifica "
            "los pagos ya registrados."
        ),
        font=("Arial", 9),
        bg=COLOR_TARJETA,
        fg=COLOR_TEXTO_SUAVE,
        anchor="w"
    )
    ayuda.grid(row=4, column=0, columnspan=4, sticky="w", pady=(4, 0))

    formulario.columnconfigure(3, weight=1)

    # Listado de tipos
    listado = tk.Frame(
        ventana,
        bg=COLOR_TARJETA,
        padx=20,
        pady=15
    )
    listado.pack(fill="both", expand=True, padx=30, pady=(10, 25))

    titulo_listado = tk.Label(
        listado,
        text="Tipos de membresía (seleccione uno para editarlo)",
        font=("Arial", 12, "bold"),
        bg=COLOR_TARJETA,
        fg=COLOR_PRINCIPAL,
        anchor="w"
    )
    titulo_listado.pack(fill="x", pady=(0, 8))

    columnas = (
        ("nombre", "Nombre", 200),
        ("duracion", "Duración", 140),
        ("precio", "Precio (Gs.)", 140),
        ("estado", "Estado", 120),
    )

    contenedor_tabla = tk.Frame(listado, bg=COLOR_TARJETA)
    contenedor_tabla.pack(fill="both", expand=True)

    tabla = ttk.Treeview(
        contenedor_tabla,
        columns=[columna[0] for columna in columnas],
        show="headings",
        selectmode="browse",
        height=8
    )

    for clave, texto, ancho in columnas:
        tabla.heading(clave, text=texto)
        tabla.column(clave, width=ancho, anchor="center")

    tabla.column("nombre", anchor="w")
    tabla.tag_configure("inactivo", background=COLOR_INACTIVO, foreground=COLOR_TEXTO_SUAVE)

    barra = ttk.Scrollbar(contenedor_tabla, orient="vertical", command=tabla.yview)
    tabla.configure(yscrollcommand=barra.set)

    tabla.pack(side="left", fill="both", expand=True)
    barra.pack(side="right", fill="y")

    def cargar_tipos():
        tabla.delete(*tabla.get_children())
        tipos_por_id.clear()

        for tipo in listar_tipos_membresia():
            id_tipo, nombre, cantidad, unidad, precio, estado = tipo
            tipos_por_id[id_tipo] = tipo

            tabla.insert(
                "",
                tk.END,
                iid=str(id_tipo),
                values=(
                    nombre,
                    formatear_duracion(cantidad, unidad),
                    formatear_monto(precio),
                    estado.capitalize()
                ),
                tags=(estado,)
            )

    def limpiar_formulario():
        tipo_seleccionado["id"] = None
        tabla.selection_remove(*tabla.selection())

        entrada_nombre.delete(0, tk.END)
        entrada_cantidad.delete(0, tk.END)
        entrada_precio.delete(0, tk.END)
        combo_unidad.set(UNIDADES_DURACION[0])

        label_modo.config(text="Nuevo tipo de membresía")
        boton_guardar.config(text="Crear tipo")
        boton_estado.config(text="Desactivar", state="disabled")
        entrada_nombre.focus()

    def seleccionar_tipo(event=None):
        seleccion = tabla.selection()

        if not seleccion:
            return

        id_tipo, nombre, cantidad, unidad, precio, estado = tipos_por_id[int(seleccion[0])]
        tipo_seleccionado["id"] = id_tipo

        entrada_nombre.delete(0, tk.END)
        entrada_nombre.insert(0, nombre)
        entrada_cantidad.delete(0, tk.END)
        entrada_cantidad.insert(0, str(cantidad))
        entrada_precio.delete(0, tk.END)
        entrada_precio.insert(0, formatear_monto(precio))
        combo_unidad.set(unidad)

        label_modo.config(text=f"Editando: {nombre}")
        boton_guardar.config(text="Guardar cambios")
        boton_estado.config(
            text="Desactivar" if estado == "activo" else "Activar",
            state="normal"
        )

    def guardar_tipo():
        nombre = entrada_nombre.get().strip()
        cantidad_texto = entrada_cantidad.get().strip()
        precio_texto = entrada_precio.get().strip().replace(".", "")

        if not nombre:
            messagebox.showwarning(
                "Nombre requerido",
                "Ingrese el nombre del tipo de membresía.",
                parent=ventana
            )
            return

        if not cantidad_texto.isdigit() or int(cantidad_texto) <= 0:
            messagebox.showwarning(
                "Duración inválida",
                "Ingrese una duración mayor a cero, solo con números.",
                parent=ventana
            )
            return

        if not precio_texto.isdigit() or int(precio_texto) <= 0:
            messagebox.showwarning(
                "Precio inválido",
                "Ingrese un precio mayor a cero, solo con números.",
                parent=ventana
            )
            return

        datos = (nombre, int(cantidad_texto), combo_unidad.get(), int(precio_texto))

        if tipo_seleccionado["id"] is None:
            guardado, mensaje = crear_tipo_membresia(*datos)
        else:
            guardado, mensaje = actualizar_tipo_membresia(tipo_seleccionado["id"], *datos)

        if guardado:
            messagebox.showinfo("Configuración", mensaje, parent=ventana)
            cargar_tipos()
            limpiar_formulario()
        else:
            messagebox.showerror("Error", mensaje, parent=ventana)

    def alternar_estado():
        id_tipo = tipo_seleccionado["id"]

        if id_tipo is None:
            return

        nombre, estado = tipos_por_id[id_tipo][1], tipos_por_id[id_tipo][5]
        nuevo_estado = "inactivo" if estado == "activo" else "activo"

        if nuevo_estado == "inactivo":
            confirmado = messagebox.askyesno(
                "Desactivar tipo",
                f"¿Desactivar '{nombre}'? Dejará de ofrecerse al registrar pagos.",
                parent=ventana
            )

            if not confirmado:
                return

        cambiado, mensaje = cambiar_estado_tipo_membresia(id_tipo, nuevo_estado)

        if cambiado:
            cargar_tipos()
            limpiar_formulario()
        else:
            messagebox.showerror("Error", mensaje, parent=ventana)

    botones = tk.Frame(
        formulario,
        bg=COLOR_TARJETA
    )
    botones.grid(row=5, column=0, columnspan=4, pady=(15, 0))

    boton_guardar = tk.Button(
        botones,
        text="Crear tipo",
        font=("Arial", 11, "bold"),
        bg=COLOR_BOTON,
        fg=COLOR_BOTON_TEXTO,
        width=16,
        height=2,
        borderwidth=0,
        cursor="hand2",
        command=guardar_tipo
    )
    boton_guardar.grid(row=0, column=0, padx=6)

    boton_estado = tk.Button(
        botones,
        text="Desactivar",
        font=("Arial", 11, "bold"),
        bg=COLOR_BOTON_LIMPIAR,
        fg=COLOR_PRINCIPAL,
        width=12,
        height=2,
        borderwidth=0,
        cursor="hand2",
        state="disabled",
        command=alternar_estado
    )
    boton_estado.grid(row=0, column=1, padx=6)

    boton_nuevo = tk.Button(
        botones,
        text="Nuevo",
        font=("Arial", 11, "bold"),
        bg=COLOR_BOTON_LIMPIAR,
        fg=COLOR_PRINCIPAL,
        width=12,
        height=2,
        borderwidth=0,
        cursor="hand2",
        command=limpiar_formulario
    )
    boton_nuevo.grid(row=0, column=2, padx=6)

    boton_cerrar = tk.Button(
        botones,
        text="Cerrar",
        font=("Arial", 11, "bold"),
        bg=COLOR_BOTON_CERRAR,
        fg=COLOR_TEXTO_SUAVE,
        width=12,
        height=2,
        borderwidth=0,
        cursor="hand2",
        command=ventana.destroy
    )
    boton_cerrar.grid(row=0, column=3, padx=6)

    tabla.bind("<<TreeviewSelect>>", seleccionar_tipo)

    cargar_tipos()
    limpiar_formulario()
