# Sistema de reservas de hoteles

Este proyecto fue realizado como solución a una prueba técnica de desarrollo.

La aplicación permite consultar habitaciones disponibles teniendo en cuenta:

- Sede del hotel.
- Tipo de habitación.
- Fecha de entrada.
- Fecha de salida.
- Número de personas.
- Temporada.
- Habitaciones disponibles.
- Valor aproximado de la estadía.

## Tecnologías utilizadas

Utilicé:

- Python con FastAPI para el backend.
- React para el frontend.
- SQLite como base de datos.
- Docker para ejecutar la aplicación.

Elegí SQLite porque para el tamaño de la prueba me pareció una opción sencilla y suficiente.

## Funcionamiento

El usuario selecciona la ciudad, el tipo de habitación, las fechas y la cantidad de personas.

El sistema calcula cuántas habitaciones son necesarias y revisa cuántas están disponibles durante las fechas seleccionadas.

También muestra un valor aproximado de la estadía.

## Datos de prueba

Se utilizaron las sedes indicadas en el ejercicio:

- Barranquilla.
- Cali.
- Cartagena.
- Bogotá.

Las tarifas son valores de prueba porque el ejercicio no indicaba precios específicos.

## Organización del proyecto

Separé algunas partes del backend para no tener todo el código en un solo archivo.

Las consultas de base de datos están principalmente en:

`backend/repositories.py`

La lógica de disponibilidad está en:

`backend/services.py`

Las rutas de la API están en:

`backend/main.py`

## Docker y despliegue

Para realizar la prueba configuré un contenedor Docker independiente en un servidor que ya utilizo para otros proyectos.

El proyecto funciona internamente en:

`127.0.0.1:18160`

También configuré el subdominio:

`hotel.tecnoxpert.com`

desde mi proveedor de dominio.

Después configuré Apache para dirigir las solicitudes hacia el contenedor Docker y configuré HTTPS.

## Demo

https://hotel.tecnoxpert.com

API:

https://hotel.tecnoxpert.com/api/health

## Posibles mejoras

Por el tiempo de la prueba me enfoqué principalmente en la consulta de disponibilidad.

Posteriormente se podrían agregar:

- Registro definitivo de reservas.
- Usuarios.
- Administración de hoteles y habitaciones.
- Administración de tarifas.
- Pagos.
- Cancelaciones.
