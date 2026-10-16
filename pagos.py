import tkinter as tk
from datetime import date
from tkinter import messagebox, ttk

from tkcalendar import DateEntry

from database import (
    actualizar_pagos_vencidos,
    buscar_miembro_por_cedula,
    calcular_fecha_vencimiento,
    listar_pagos,
    obtener_tipos_membresia,
    registrar_pago,
)
from estilos import (
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


COLOR_ESTADO = {
    "pagado": "#e3f4e6",
    "pendiente": "#fff4d6",
    "vencido": "#fbe1e1",
}

ESTADOS_REGISTRO = ("pagado", "pendiente")


def formatear_monto(monto):
    """
    Formatea un monto en guaraníes con separador de miles (150000 -> 150.000).
    """
    return f"{monto:,}".replace(",", ".")


def formatear_fecha(fecha_iso):
    """
    Convierte una fecha ISO (2026-10-16) al formato 16/10/2026.
    """
    return date.fromisoformat(fecha_iso).strftime("%d/%m/%Y")


def abrir_ventana_pagos(ventana_principal):
    actualizar_pagos_vencidos()

    ventana = tk.Toplevel(ventana_principal)
    ventana.title("Pagos y cuotas")
    ventana.geometry("860x760")
    ventana.resizable(False, False)
    ventana.configure(bg=COLOR_FONDO)

    tipos = obtener_tipos_membresia()
    tipos_por_nombre = {tipo[1]: tipo for tipo in tipos}

    miembro_seleccionado = {"datos": None}

    encabezado = tk.Frame(
        ventana,
        bg=COLOR_PRINCIPAL,
        height=90
    )
    encabezado.pack(fill="x")

    titulo = tk.Label(
        encabezado,
        text="Pagos y cuotas",
        font=("Arial", 21, "bold"),
        bg=COLOR_PRINCIPAL,
        fg=COLOR_TITULO_ENCABEZADO
    )
    titulo.pack(pady=(18, 4))

    subtitulo = tk.Label(
        encabezado,
        text="Registre el pago de la membresía de un miembro",
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

    # Cédula y búsqueda del miembro
    crear_etiqueta("Cédula del miembro", 0)

    entrada_cedula = tk.Entry(
        formulario,
        font=("Arial", 11),
        width=22
    )
    entrada_cedula.grid(row=0, column=1, sticky="w", pady=6, ipady=4)

    label_miembro = tk.Label(
        formulario,
        text="Ingrese la cédula y presione Buscar",
        font=("Arial", 10),
        bg=COLOR_TARJETA,
        fg=COLOR_TEXTO_SUAVE,
        anchor="w"
    )
    label_miembro.grid(row=1, column=1, columnspan=2, sticky="w", pady=(0, 6))

    # Tipo de membresía
    crear_etiqueta("Tipo de membresía", 2)

    combo_tipo = ttk.Combobox(
        formulario,
        values=[tipo[1] for tipo in tipos],
        state="readonly",
        font=("Arial", 11),
        width=20
    )
    combo_tipo.grid(row=2, column=1, sticky="w", pady=6)

    # Monto
    crear_etiqueta("Monto (Gs.)", 3)

    entrada_monto = tk.Entry(
        formulario,
        font=("Arial", 11),
        width=22
    )
    entrada_monto.grid(row=3, column=1, sticky="w", pady=6, ipady=4)

    # Fecha de inicio
    crear_etiqueta("Fecha de inicio", 4)

    selector_fecha = DateEntry(
        formulario,
        font=("Arial", 11),
        width=19,
        locale="es_ES",
        date_pattern="dd/MM/yyyy",
        background=COLOR_PRINCIPAL,
        foreground=COLOR_BOTON_TEXTO,
        borderwidth=1
    )
    selector_fecha.grid(row=4, column=1, sticky="w", pady=6)

    # Vencimiento calculado
    crear_etiqueta("Vencimiento", 5)

    label_vencimiento = tk.Label(
        formulario,
        text="-",
        font=("Arial", 11),
        bg=COLOR_TARJETA,
        fg=COLOR_PRINCIPAL,
        anchor="w"
    )
    label_vencimiento.grid(row=5, column=1, sticky="w", pady=6)

    # Estado del pago
    crear_etiqueta("Estado del pago", 6)

    combo_estado = ttk.Combobox(
        formulario,
        values=ESTADOS_REGISTRO,
        state="readonly",
        font=("Arial", 11),
        width=20
    )
    combo_estado.grid(row=6, column=1, sticky="w", pady=6)

    formulario.columnconfigure(2, weight=1)

    # Listado de pagos
    listado = tk.Frame(
        ventana,
        bg=COLOR_TARJETA,
        padx=20,
        pady=15
    )
    listado.pack(fill="both", expand=True, padx=30, pady=(10, 25))

    titulo_listado = tk.Label(
        listado,
        text="Últimos pagos registrados",
        font=("Arial", 12, "bold"),
        bg=COLOR_TARJETA,
        fg=COLOR_PRINCIPAL,
        anchor="w"
    )
    titulo_listado.pack(fill="x", pady=(0, 8))

    columnas = (
        ("miembro", "Miembro", 170),
        ("cedula", "Cédula", 85),
        ("tipo", "Tipo", 90),
        ("monto", "Monto (Gs.)", 95),
        ("inicio", "Inicio", 85),
        ("vencimiento", "Vencimiento", 90),
        ("estado", "Estado", 85),
    )

    contenedor_tabla = tk.Frame(listado, bg=COLOR_TARJETA)
    contenedor_tabla.pack(fill="both", expand=True)

    tabla = ttk.Treeview(
        contenedor_tabla,
        columns=[columna[0] for columna in columnas],
        show="headings",
        height=8
    )

    for clave, texto, ancho in columnas:
        tabla.heading(clave, text=texto)
        tabla.column(clave, width=ancho, anchor="center")

    tabla.column("miembro", anchor="w")

    for estado, color in COLOR_ESTADO.items():
        tabla.tag_configure(estado, background=color)

    barra = ttk.Scrollbar(contenedor_tabla, orient="vertical", command=tabla.yview)
    tabla.configure(yscrollcommand=barra.set)

    tabla.pack(side="left", fill="both", expand=True)
    barra.pack(side="right", fill="y")

    def cargar_pagos():
        tabla.delete(*tabla.get_children())

        datos = miembro_seleccionado["datos"]

        if datos:
            titulo_listado.config(text=f"Pagos de {datos[1]} {datos[2]}")
            pagos = listar_pagos(id_miembro=datos[0])
        else:
            titulo_listado.config(text="Últimos pagos registrados")
            pagos = listar_pagos()

        for pago in pagos:
            (_, miembro, cedula, tipo, monto, _,
             fecha_inicio, fecha_vencimiento, estado) = pago

            tabla.insert(
                "",
                tk.END,
                values=(
                    miembro,
                    cedula,
                    tipo,
                    formatear_monto(monto),
                    formatear_fecha(fecha_inicio),
                    formatear_fecha(fecha_vencimiento),
                    estado.capitalize()
                ),
                tags=(estado,)
            )

    def actualizar_vencimiento(event=None):
        tipo = tipos_por_nombre.get(combo_tipo.get())

        if tipo is None:
            label_vencimiento.config(text="-")
            return

        _, _, cantidad, unidad, _ = tipo
        vencimiento = calcular_fecha_vencimiento(selector_fecha.get_date(), cantidad, unidad)
        label_vencimiento.config(text=vencimiento.strftime("%d/%m/%Y"))

    def seleccionar_tipo(event=None):
        tipo = tipos_por_nombre.get(combo_tipo.get())

        if tipo is not None:
            entrada_monto.delete(0, tk.END)
            entrada_monto.insert(0, formatear_monto(tipo[4]))

        actualizar_vencimiento()

    def buscar_miembro(event=None):
        cedula = entrada_cedula.get().strip()

        if not cedula:
            messagebox.showwarning(
                "Cédula requerida",
                "Ingrese la cédula del miembro.",
                parent=ventana
            )
            return

        miembro = buscar_miembro_por_cedula(cedula)

        if miembro is None:
            miembro_seleccionado["datos"] = None
            label_miembro.config(
                text="No se encontró un miembro con esa cédula.",
                fg="#b3261e"
            )
        elif miembro[4] != "activo":
            miembro_seleccionado["datos"] = None
            label_miembro.config(
                text=f"{miembro[1]} {miembro[2]} está {miembro[4]}.",
                fg="#b3261e"
            )
        else:
            miembro_seleccionado["datos"] = miembro
            label_miembro.config(
                text=f"Miembro: {miembro[1]} {miembro[2]}",
                fg=COLOR_PRINCIPAL
            )

        cargar_pagos()

    def cedula_modificada(event=None):
        if miembro_seleccionado["datos"] and entrada_cedula.get().strip() != miembro_seleccionado["datos"][3]:
            miembro_seleccionado["datos"] = None
            label_miembro.config(
                text="Ingrese la cédula y presione Buscar",
                fg=COLOR_TEXTO_SUAVE
            )
            cargar_pagos()

    def limpiar_formulario():
        entrada_cedula.delete(0, tk.END)
        entrada_monto.delete(0, tk.END)
        combo_tipo.set("")
        combo_estado.set(ESTADOS_REGISTRO[0])
        selector_fecha.set_date(date.today())
        label_vencimiento.config(text="-")
        miembro_seleccionado["datos"] = None
        label_miembro.config(
            text="Ingrese la cédula y presione Buscar",
            fg=COLOR_TEXTO_SUAVE
        )
        cargar_pagos()
        entrada_cedula.focus()

    def guardar_pago():
        datos = miembro_seleccionado["datos"]

        if datos is None:
            messagebox.showwarning(
                "Miembro requerido",
                "Busque y seleccione un miembro activo por su cédula.",
                parent=ventana
            )
            return

        tipo = tipos_por_nombre.get(combo_tipo.get())

        if tipo is None:
            messagebox.showwarning(
                "Tipo de membresía",
                "Seleccione un tipo de membresía.",
                parent=ventana
            )
            return

        monto_texto = entrada_monto.get().strip().replace(".", "")

        if not monto_texto.isdigit() or int(monto_texto) <= 0:
            messagebox.showwarning(
                "Monto inválido",
                "Ingrese un monto mayor a cero, solo con números.",
                parent=ventana
            )
            return

        registrado, mensaje = registrar_pago(
            datos[0],
            tipo[0],
            int(monto_texto),
            selector_fecha.get_date(),
            combo_estado.get()
        )

        if registrado:
            messagebox.showinfo("Registro exitoso", mensaje, parent=ventana)
            combo_tipo.set("")
            entrada_monto.delete(0, tk.END)
            label_vencimiento.config(text="-")
            cargar_pagos()
        else:
            messagebox.showerror("Error", mensaje, parent=ventana)

    boton_buscar = tk.Button(
        formulario,
        text="Buscar",
        font=("Arial", 10, "bold"),
        bg=COLOR_BOTON,
        fg=COLOR_BOTON_TEXTO,
        width=10,
        borderwidth=0,
        cursor="hand2",
        command=buscar_miembro
    )
    boton_buscar.grid(row=0, column=2, sticky="w", padx=10)

    entrada_cedula.bind("<Return>", buscar_miembro)
    entrada_cedula.bind("<KeyRelease>", cedula_modificada)
    combo_tipo.bind("<<ComboboxSelected>>", seleccionar_tipo)
    selector_fecha.bind("<<DateEntrySelected>>", actualizar_vencimiento)
    selector_fecha.bind("<FocusOut>", actualizar_vencimiento)

    botones = tk.Frame(
        formulario,
        bg=COLOR_TARJETA
    )
    botones.grid(row=7, column=0, columnspan=3, pady=(15, 0))

    boton_guardar = tk.Button(
        botones,
        text="Guardar pago",
        font=("Arial", 11, "bold"),
        bg=COLOR_BOTON,
        fg=COLOR_BOTON_TEXTO,
        width=18,
        height=2,
        borderwidth=0,
        cursor="hand2",
        command=guardar_pago
    )
    boton_guardar.grid(row=0, column=0, padx=8)

    boton_limpiar = tk.Button(
        botones,
        text="Limpiar",
        font=("Arial", 11, "bold"),
        bg=COLOR_BOTON_LIMPIAR,
        fg=COLOR_PRINCIPAL,
        width=14,
        height=2,
        borderwidth=0,
        cursor="hand2",
        command=limpiar_formulario
    )
    boton_limpiar.grid(row=0, column=1, padx=8)

    boton_cerrar = tk.Button(
        botones,
        text="Cerrar",
        font=("Arial", 11, "bold"),
        bg=COLOR_BOTON_CERRAR,
        fg=COLOR_TEXTO_SUAVE,
        width=14,
        height=2,
        borderwidth=0,
        cursor="hand2",
        command=ventana.destroy
    )
    boton_cerrar.grid(row=0, column=2, padx=8)

    combo_estado.set(ESTADOS_REGISTRO[0])
    cargar_pagos()
    entrada_cedula.focus()
