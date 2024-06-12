from jwt import encode, decode, exceptions
from datetime import datetime, timedelta
from os import getenv
from fastapi.responses import JSONResponse


def exp_time(days: int):
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