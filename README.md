# Gym Management System

Sistema de gestión para gimnasios desarrollado en Python como proyecto académico.

El objetivo del sistema es centralizar la administración del gimnasio mediante diferentes módulos que serán desarrollados de forma incremental durante los distintos Sprints del proyecto.

## Sprint 1 - Módulo de Login

En el Sprint 1 se desarrolló el sistema de autenticación y acceso inicial a la aplicación.

### Funcionalidades implementadas

- Inicio de sesión mediante usuario y contraseña.
- Validación de credenciales.
- Base de datos local utilizando SQLite.
- Control de acceso al sistema.
- Pantalla principal posterior al inicio de sesión.
- Pruebas del módulo de autenticación.

## Tecnologías utilizadas

- Python 3
- Tkinter
- SQLite
- Git
- GitHub

## Estructura del proyecto

```text
gym-management/
│
├── database.py
├── login.py
├── main.py
├── pantalla_principal.py
├── test_login.py
├── gym_management.db
├── .gitignore
└── README.md
```

### Descripción de los archivos principales

- `main.py`: punto de entrada de la aplicación.
- `login.py`: interfaz y lógica del módulo de inicio de sesión.
- `database.py`: gestión de la conexión y operaciones con la base de datos.
- `pantalla_principal.py`: interfaz principal mostrada después de un inicio de sesión exitoso.
- `test_login.py`: pruebas relacionadas con el módulo de autenticación.
- `gym_management.db`: base de datos SQLite utilizada por el sistema.

## Requisitos

Para ejecutar el proyecto es necesario tener instalado:

- Python 3.x
- Git (opcional, para clonar el repositorio)

Las demás tecnologías utilizadas forman parte de la biblioteca estándar de Python.

## Instalación

Clonar el repositorio:

```bash
git clone https://github.com/juanjo2721/gym-management.git
```

Ingresar a la carpeta del proyecto:

```bash
cd gym-management
```

## Ejecución

Ejecutar el archivo principal:

```bash
python main.py
```

En Windows también puede utilizarse:

```bash
py main.py
```

## Estado del proyecto

Actualmente se encuentra completado el **Sprint 1**, correspondiente al módulo de autenticación y acceso inicial al sistema.

Los siguientes módulos serán incorporados progresivamente en futuros Sprints.