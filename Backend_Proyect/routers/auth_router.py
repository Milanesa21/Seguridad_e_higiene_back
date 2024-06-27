from fastapi import APIRouter, Header, HTTPException, status
from fastapi.responses import JSONResponse
from services.jwt import validate_token



auth_router = APIRouter(prefix='/auth', tags=['Auth'])

@auth_router.post('/validate/token')
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