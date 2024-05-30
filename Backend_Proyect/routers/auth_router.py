from fastapi import APIRouter, Header, HTTPException, status
from services.jwt import validate_token



auth_router = APIRouter(prefix='/auth', tags=['Auth'])

@auth_router.post('/validate/token')
async def validate_token_route(Authorization: str = Header(None)):
    token = Authorization.split(" ")[1]
    if not token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token not found")
    Authorization_response = validate_token(token, output=True)
    if Authorization_response == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")
    return {"message": "Token valido", "Usuario": Authorization_response}