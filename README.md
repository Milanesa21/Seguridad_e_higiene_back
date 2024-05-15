# Backend del proyecto de seguridad e higiene
![OIG4 (1) (1)](https://github.com/Milanesa21/Seguridad_e_higiene/assets/127987458/049d4215-f74a-4ec3-a096-abd80d8308ef)

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
    pip install "fastapi[all]" bcrypt SQLAlchemy psycopg2 python-dotenv passlib
    ```
    o tambien se puede hacer de la siguiente manera
    ´´´
    pip install -r requirements.txt
    ```
4. Se necesita crear un archivo .env con los siguientes datos:
     ```
   DB_DRIVER=
    DB_USERNAME=
    DB_PASSWORD=
    DB_HOST=
    DB_PORT=
    DB_NAME=
    ```
## Una vez inicado el entorno y las dependencias descargadas
- Se utiliza el siguiente codigo para prender el servidor
    ```
    uvicorn main:app --reload
    ```
 
## Integrantes del grupo
- Tomas Valdez
- Ivan Pietkiewicz
- Diego Jara

Para actualizar el requirements:

pip freeze > requirements.txt