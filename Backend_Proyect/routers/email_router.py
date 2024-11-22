from fastapi import APIRouter, Depends, HTTPException, exceptions, status
from sqlalchemy.orm import Session
from dataBase.db import get_db
from controllers.auth_users import get_user_email
from services.service_jwt import generate_reset_token, validate_token
from services.email_service import send_email, send_create_company
from controllers.auth_users import change_password
from model.schemas.email_schemas import CreateNewCompany
from controllers.token_controllers import temooral_token

email_routes = APIRouter(prefix='/email', tags=['Email'])

@email_routes.post('/reperacion/')
async def email_recuperacion(email: str, db: Session = Depends(get_db)):
    user = get_user_email(email, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    token = temooral_token(email, db)
    if not token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to generate token")
    # Intenta enviar el correo y maneja cualquier error
    try:
        send_email(email=email,id=user.id, full_name=user.full_name, temporal_token=token.Token)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Failed to send recovery email: {e}")

    return {"message": "Correo de recuperación enviado exitosamente"}

@email_routes.post('/')
async def create_new_company(request: CreateNewCompany):
    data = {
        'nombre_empresa': request.empresa,
        'nombre_dueno': request.dueno,
        'email': request.email,
        'telefono': request.telefono
    }
    try:
        send_create_company(data)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Failed to send company registration email: {e}")
    return {"message": "Correo de registro de empresa enviado exitosamente"}


# Ruta para restablecer la contraseña
@email_routes.post('/resetPassword/{token}')
async def reset_password(token: str, new_password: str, db: Session = Depends(get_db)):
    try:
        data = validate_token(token, output=True)
        email = data['sub']

        user = get_user_email(email, db)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        if not change_password(user.id, new_password, db):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to change password")

        return {'message': 'Contraseña cambiada exitosamente'}

    except exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expirado")
    except exceptions.DecodeError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
