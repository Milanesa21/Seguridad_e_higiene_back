# Backend del Proyecto
![OIG4 (1) (1)](https://github.com/Milanesa21/Seguridad_e_higiene/assets/127987458/a99e1845-1792-4b23-9283-1c1de395981b)



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

