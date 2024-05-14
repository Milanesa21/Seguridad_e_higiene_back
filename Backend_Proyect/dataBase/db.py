from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from config import DB_DRIVER, DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME

# Crear la URL de conexión a la base de datos usando las variables de entorno
url = URL.create(
    drivername=DB_DRIVER,
    username=DB_USERNAME,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME
)

# Crear el motor de SQLAlchemy
engine = create_engine(url)
