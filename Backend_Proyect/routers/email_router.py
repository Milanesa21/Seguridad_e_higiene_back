from fastapi import APIRouter, Depends, HTTPException, exceptions, status
from sqlalchemy.orm import Session
from dataBase.db import get_db
from controllers.auth_users import get_user_email
from services.jwt import generate_reset_token,validate_token
from services.email_service import send_email
from controllers.auth_users import change_password


email_routes = APIRouter(prefix='/email', tags=['Email'])


@email_routes.post('/reperacion/')
async def email_recuperacio(email: str, db:Session = Depends(get_db)):

    user = get_user_email(email,db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
    temporal_token = generate_reset_token(email)

    send_email(
        email=email,
        full_name=user.full_name,
        temporal_token=temporal_token
        )
    return {"message": "Correo de recuperación enviado exitosamente"}


@email_routes.post('/resetPassword/{token}')
async def reset_password(token:str, new_password:str,db:Session=Depends(get_db)):
    try:
        data = validate_token(token, output=True)
        email = data['sub']
        
        user = get_user_email(email, db)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        if not change_password(user.id, new_password,db):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to change password")
        
        return {'messege': 'Contraseña cambiada exitosamente'}
    except exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expirado")
    except exceptions.DecodeError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")



