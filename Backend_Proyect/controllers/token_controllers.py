from datetime import datetime, timedelta
import random
import string
from model.email_recuperacion_model import Token
from sqlalchemy.orm import Session


def generate_random_token(length=20):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def temooral_token(email: str, db: Session):
    """ Genera un token temporal para el restablecimiento de contraseña """
    existe_token = db.query(Token).filter(Token.email == email).first()
    if existe_token:
        if existe_token.expiration_time > datetime.utcnow():
            return existe_token
        else:
            db.delete(existe_token)
            db.commit()
    token = generate_random_token()
    expiration_time = datetime.utcnow() + timedelta(hours=2)
    db_token = Token(Token=token, email=email, expiration_time=expiration_time)
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token
