import psycopg2 as pg2

users_db = {
    "Milanesa": {
        "username": "Milanesa",
        "full_name": "Digo Jara",
        "email": "fake@email.com",
        "disables": False,
        "password": "1234"
    },
    "Toto": {
        "username": "Toto",
        "full_name": "Juan Perez",
        "email": "fake@email.com",
        "disables": True,
        "password": "4321"
    },
    "Hide on bush": {
        "username": "Hide on bush",
        "full_name": "Lee Sang-Hyeok",
        "email": "fake@email.com",
        "disables": False,
        "password": "T1"
    }
}


def connect():
    try:
        conn = pg2.connect(
            host="localhost",
            database="prueba",
            user="postgres",
            password="papafrita",
            port="5432"
        )
        print("Conectado a la base de datos")
        return conn
    except Exception as e:
        print("Error al conectar a la base de datos")
        print(e)
        return None