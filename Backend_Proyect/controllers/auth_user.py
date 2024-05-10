from model.user import User, UserDB
from dataBase.db import users_db
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def search_user(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    return None

async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = search_user(token)
    if user is None:
        raise HTTPException( status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Invalid credentials",
                            headers={"WWW-Authenticate": "Bearer"})
    
    if user.disables:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return user


def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")
    
    user = search_user(form.username)
    if not form.password == user.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")
    return {"access_token": user.username, "token_type": "bearer"}

def read_users(user: User = Depends(get_current_user)):
    return user