from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from dataBase.db import get_db
from controllers.auth_users import get_user_by_id



def get_user_info_by_name(user_id: int, db: Session = Depends(get_db)):
    user_by_id = get_user_by_id(user_id, db)
    if not user_by_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found or full_name does not match user_id")
    return {
        "id": user_by_id.id,
        "full_name": user_by_id.full_name,
        "puesto_trabajo": user_by_id.puesto_trabajo,
        "email": user_by_id.email
    }