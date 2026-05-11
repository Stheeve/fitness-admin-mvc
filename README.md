# Fitness Admin MVC

## Descripción del proyecto

Fitness Admin MVC es una aplicación web desarrollada bajo el patrón MVC que permite administrar información relacionada con rutinas de ejercicio y ejercicios físicos. Este módulo administrativo alimenta el core del sistema, el cual se basa en el análisis de usuarios con características similares para apoyar la selección de rutinas y ejercicios según los objetivos del usuario.

## Core del proyecto

El core del sistema consiste en comparar datos de usuarios con características similares, como peso, edad, nivel de actividad y objetivo personal. A partir de esta comparación, el sistema puede identificar patrones de rutinas y ejercicios que han resultado efectivos para usuarios con perfiles parecidos.

La administración permite registrar rutinas, ejercicios y asignar ejercicios a rutinas, generando la información necesaria para que el core pueda analizar y comparar datos posteriormente.

## Funcionalidades

- Inicio de sesión
- Registro de usuarios
- Protección de rutas mediante sesiones
- CRUD de rutinas
- CRUD de ejercicios
- Asignación de ejercicios a rutinas
- Uso de dropdowns para manejar relaciones entre tablas
- Validaciones Back-End para datos sensibles del core

## Validaciones Back-End

El sistema valida datos importantes antes de guardarlos en la base de datos:

- El nombre de una rutina debe tener al menos 3 caracteres.
- El nombre de un ejercicio debe tener al menos 3 caracteres.
- Las calorías quemadas deben ser mayores a 0.
- Las series deben ser mayores a 0.
- Las repeticiones deben ser mayores a 0.
- Para asignar ejercicios a rutinas, se debe seleccionar una rutina y un ejercicio desde listas desplegables.

Estas validaciones se realizan en el Back-End, no únicamente en el navegador.

## Relaciones entre tablas

La tabla `rutina_ejercicio` relaciona rutinas y ejercicios. Para registrar una asignación, el usuario no escribe manualmente los IDs de las claves foráneas, sino que selecciona la rutina y el ejercicio mediante dropdowns.

## Tecnologías utilizadas

- Python
- Flask
- MySQL
- MySQL Workbench
- HTML
- Jinja2
- Git y GitHub

## Estructura del proyecto


FitnessAdminMVC/
│── app.py
│── requirements.txt
│── README.md
│
├── config/
│   ├── __init__.py
│   └── db.py
│
├── controllers/
│   ├── __init__.py
│   ├── auth_controller.py
│   ├── rutina_controller.py
│   ├── ejercicio_controller.py
│   └── rutina_ejercicio_controller.py
│
├── models/
│   ├── __init__.py
│   ├── user_model.py
│   ├── rutina_model.py
│   ├── ejercicio_model.py
│   └── rutina_ejercicio_model.py
│
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── rutinas.html
│   ├── crear_rutina.html
│   ├── editar_rutina.html
│   ├── ejercicios.html
│   ├── crear_ejercicio.html
│   ├── editar_ejercicio.html
│   ├── asignaciones.html
│   └── crear_asignacion.html
│
└── static/

## Base de datos
Nombre de la base de datos: fitness_admin
Tablas principales:

usuarios
rutinas
ejercicios
rutina_ejercicio

## Instalación
Clonar el repositorio:
git clone URL_DEL_REPOSITORIO
cd FitnessAdminMVC

Crear entorno virtual:
python -m venv venv

Activar entorno virtual:
venv\Scripts\activate

Instalar dependencias:
pip install -r requirements.txt

Crear la base de datos en MySQL Workbench:
CREATE DATABASE fitness_admin;
USE fitness_admin;

Ejecutar el proyecto:
python app.py

Abrir en el navegador:
http://127.0.0.1:5000/

Rutas principales

/                       Login
/register               Registro
/dashboard              Panel administrativo
/rutinas                Listado de rutinas
/rutinas/crear          Crear rutina
/ejercicios             Listado de ejercicios
/ejercicios/crear       Crear ejercicio
/asignaciones           Listado de asignaciones
/asignaciones/crear     Asignar ejercicio a rutina
/logout                 Cerrar sesión

## Autor

Stheeven Quishpe

## Deploy

La aplicación se encuentra disponible en:

fitness-admin-mvc-production.up.railway.app