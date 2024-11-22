from jwt import encode, decode, exceptions
from datetime import datetime, timedelta
from os import getenv

from sqlalchemy.orm import Session
from model.email_recuperacion_model import Token


def exp_time(days: int=0, minutes: int = 0):
    date = datetime.now()
    new_date = date + timedelta(days)
    return new_date

def write_token(data: dict):
    token = encode(payload={**data, 'exp': exp_time(1)}, key=getenv('SECRET_KEY'), algorithm='HS256')
    return token


def validate_token(token: str, output: bool = False):
    try:
        if output:
            token_response = decode(token, getenv('SECRET_KEY'), algorithms=['HS256'])
            print('la variable',token_response)
            return token_response
    except exceptions.DecodeError:
        return {'message': 'Invalid token', 'status_code': 401}
    except exceptions.ExpiredSignatureError:
        return {'message': 'Expired token', 'status_code': 401}
    

def generate_reset_token(email: str):
    token = encode(
        payload={
            'sub': email, 
            'exp': exp_time(minutes=15)  # Token válido por 15 minutos
        },
        key=getenv('SECRET_KEY'), 
        algorithm='HS256'
    )
    return token

def validate_token_temporal(token: str, db: Session):
    try:
        exist_token = db.query(Token).filter(Token.Token == token).first()
        if not exist_token:
            return {'message': 'Invalid token', 'status_code': 401}
        if exist_token.expiration_time < datetime.utcnow():
            return {'message': 'Expired token', 'status_code': 401}
        return {'message': 'Token valido', 'status_code': 200}
    except exceptions.DecodeError:
        return {'message': 'Invalid token', 'status_code': 401}