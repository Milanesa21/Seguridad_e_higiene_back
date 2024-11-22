from fastapi import APIRouter, Depends, Header, HTTPException, status
from requests import Session
from services.service_jwt import validate_token_temporal,validate_token
from dataBase.db import get_db



auth_router = APIRouter(prefix='/auth', tags=['Auth'])

@auth_router.post('/validate/token/usuario')
async def validate_token_route(Authorization: str = Header(None)):
    if not Authorization:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Authorization header not found")
    token = Authorization.split(" ")[1]
    if token is None or not token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token not found")
    Authorization_response = validate_token(token, output=True)
    if Authorization_response == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")
    if isinstance(Authorization_response, dict) and 'status_code' in Authorization_response:
        raise HTTPException(status_code=Authorization_response['status_code'], detail=Authorization_response['message'])
    return {"message": "Token valido", "Usuario": Authorization_response}

@auth_router.post('/validate/token/empresa')
async def validate_token_route_empresa(Authorization: str = Header(None)):
    if not Authorization:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Authorization header not found")
    token = Authorization.split(" ")[1]
    if token is None or not token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token not found")
    Authorization_response = validate_token(token, output=True)
    if Authorization_response == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")
    if isinstance(Authorization_response, dict) and 'status_code' in Authorization_response:
        raise HTTPException(status_code=Authorization_response['status_code'], detail=Authorization_response['message'])
    return {"message": "Token valido", "Empresa": Authorization_response}



@auth_router.post('/validate/')
async def token_temporal(token: str, db: Session = Depends(get_db)):
    print('aaaaaa',token)
    try:
        data = validate_token_temporal(token, db)
        return data
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error: {e}")

