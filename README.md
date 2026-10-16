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

### Módulo de Miembros

Permite:

- Registrar un nuevo miembro.
- Cargar datos personales.
- Registrar datos de contacto.
- Guardar la información en la tabla `miembros`.
- Validar que la cédula no esté duplicada.
- Establecer automáticamente la fecha de registro.
- Definir el estado inicial del miembro como activo.

## Próximos módulos

- Usuarios
- Pagos y cuotas
- Renovación y cálculo de vencimiento
- Asistencia

## Estructura del proyecto

```text
gym-management/
│
├── database.py
├── database.html
├── gym_management.db
├── login.py
├── main.py
├── miembros.py
├── pantalla_principal.py
├── test_login.py
├── README.md
└── .gitignore