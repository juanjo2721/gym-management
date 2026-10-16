# Sistema de Gestión para Gimnasio

Sistema de gestión administrativa para gimnasios, desarrollado como proyecto académico.

El sistema busca centralizar la información de usuarios y miembros, facilitar el registro de datos personales y permitir futuras funcionalidades relacionadas con pagos, cuotas y asistencia.

## Tecnologías utilizadas

- Python 3
- Tkinter
- SQLite3
- datetime
- tkcalendar
- unittest
- Git y GitHub
- Visual Studio Code

## Módulos del sistema

### Módulo de Login

Permite:

- Ingresar mediante usuario y contraseña.
- Validar las credenciales en SQLite.
- Permitir el acceso únicamente a usuarios activos.
- Mostrar la pantalla principal luego de iniciar sesión.
- Informar cuando las credenciales son incorrectas.
- Cerrar sesión y volver a la pantalla de login.

### Módulo de Miembros

Permite:

- Registrar un nuevo miembro.
- Cargar datos personales.
- Registrar datos de contacto.
- Guardar la información en la tabla `miembros`.
- Validar que la cédula no esté duplicada.
- Establecer automáticamente la fecha de registro.
- Definir el estado inicial del miembro como activo.

### Módulo de Pagos y Cuotas

Permite:

- Buscar al miembro por su número de cédula (solo miembros activos).
- Seleccionar el tipo de membresía; el monto se completa con el precio configurado y puede modificarse.
- Elegir la fecha de inicio con un calendario (`tkcalendar`).
- Calcular automáticamente la fecha de vencimiento según la duración del tipo de membresía.
- Registrar el pago con estado `pagado` o `pendiente`.
- Marcar automáticamente como `vencido` los pagos pendientes cuya fecha de vencimiento ya pasó.
- Ver los últimos pagos registrados, o los del miembro seleccionado, con colores por estado.

Los tipos de membresía se configuran en la tabla `tipos_membresia`:

| Campo | Descripción |
|---|---|
| `nombre` | Nombre del tipo (Diaria, Mensual, etc.) |
| `duracion_cantidad` | Cantidad de días o meses que dura |
| `duracion_unidad` | `dias` o `meses` |
| `precio` | Precio sugerido en guaraníes |
| `estado` | `activo` o `inactivo` (los inactivos no se muestran) |

## Próximos módulos

- Usuarios
- Renovación de membresías
- Asistencia

## Estructura del proyecto

```text
gym-management/
│
├── main.py                 # Punto de entrada: crea la ventana y muestra el login
├── login.py                # Pantalla de inicio de sesión
├── pantalla_principal.py   # Panel principal con acceso a los módulos
├── miembros.py             # Registro de miembros
├── pagos.py                # Registro de pagos y cuotas
├── database.py             # Conexión y consultas a SQLite
├── estilos.py              # Colores y utilidades visuales compartidas
├── generar_docs.py         # Genera la documentación HTML con pydoc
├── test_login.py           # Pruebas de login y miembros
├── test_pagos.py           # Pruebas de pagos
├── requirements.txt        # Dependencias externas
├── gym_management.db       # Base de datos SQLite
├── database.html           # Documentación generada
├── miembros.html           # Documentación generada
├── pagos.html              # Documentación generada
├── estilos.html            # Documentación generada
├── README.md
└── .gitignore
```

## Instalación y ejecución

```bash
pip install -r requirements.txt
python main.py
```

Usuario de prueba: `admin` / `admin123`.

## Pruebas

```bash
python -m unittest -v
```

Las pruebas crean una base de datos temporal en cada ejecución, por lo que no modifican `gym_management.db`.

## Documentación

```bash
python generar_docs.py
```

Genera los archivos `.html` con pydoc usando rutas relativas.
