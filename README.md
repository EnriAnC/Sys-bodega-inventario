# Sys-bodega-inventario

Este es un proyecto de inventario de bodegas desarrollado con FastAPI.

## Instalación

Sigue estos pasos para configurar el proyecto en tu entorno local.

### Prerrequisitos

Asegúrate de tener instalado lo siguiente:

- Python (versión 3.8 o superior)
- pip
- virtualenv

### Pasos de Instalación

1. Clona el repositorio en tu máquina local:
~~~
git clone https://github.com/EnriAnC/Sys-bodega-inventario.git
~~~
2. Ve al directorio del proyecto:
~~~
cd Sys-bodega-inventario
~~~
3. Crea un entorno virtual para el proyecto:
~~~
(si no tienes instalado virtualenv) pip install virtualenv
virtualenv venv
~~~
4. Activa el entorno virtual:
~~~
source venv/bin/activate
~~~
5. Instala las dependencias del proyecto:
~~~
pip install -r requirements.txt
~~~
6. Define las variables de entorno necesarias. Crea un archivo `.env` en la raíz del proyecto y añade las siguientes líneas:
~~~
DATABASE_HOST= silly.db.exxxx
DATABASE_PORT= 54xxx
DATABASE_NAME= iuxxxxxx
DATABASE_USER= iuxxxxxxxxxx
DATABASE_PASSWORD= CXxxxxxxxx

DATABASE_HOST_DEV= xxxxxxxx
DATABASE_PORT_DEV= xxxx
DATABASE_NAME_DEV= xxxx
DATABASE_USER_DEV= xxxxx
DATABASE_PASSWORD_DEV= xxxxx
~~~
Asegúrate de reemplazar los valores `DATABASE_HOST`, `DATABASE_PORT`, `DATABASE_NAME`, `DATABASE_USER` y `DATABASE_PASSWORD` con las configuraciones correctas para tu entorno.

7. Inicia el servidor de desarrollo:
~~~
uvicorn main:app --reload
~~~
El servidor de desarrollo se iniciará en `http://localhost:8000`.
