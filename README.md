﻿# Backend del Proyecto
![OIG4](https://github.com/Milanesa21/Seguridad_e_higiene/assets/127987458/0c519a02-78e7-421b-97dc-e7e0340b25f6){width=200px height=150px}


1. Se nececita crear un entrorno virtual
    ```
    python -m venv venv
    ```
2. Se abre la terminal y se ejecuta el siguente linea para ingresar al entorno virtual
- Windows
    ```
    .\venv\Scripts\activate
    ```
- Mac
    ```
    source .\venv\bin\activate
    ```
- Linux
    1. Navega al directorio donde está ubicado tu entorno virtual
        ```
        cd venv
        ```
    2. Activa el entorno virtual
        ```
        source bin/activate
        ```
- Desactivar el etorno virtual: 
    ```
    deactivate
    ```
3. Se instalan las dependecian necesarias
    ```
    pip install "fastapi[all]"
    ```
    ```
    pip install psycopg2
    ```

# Una vez inicado el entorno y las dependencias descargadas
- Se utiliza el siguiente codigo para prender el servidor
    ```
    uvicorn main:app --reload
    ```



# Una vez inicado el entorno y las dependencias descargadas
- Se utiliza el siguiente codigo para prender el servidor
    ```
    uvicorn main:app --reload
    ```

