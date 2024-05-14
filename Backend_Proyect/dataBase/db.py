from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker,declarative_base

url = URL.create(
    drivername="postgresql",
    username="postgres",
    password="1234",
    host="localhost",
    port=5432,
    database="prueba"
)

Base = declarative_base()

engine = create_engine(url)
sessionLocal = sessionmaker(bind=engine)



def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()