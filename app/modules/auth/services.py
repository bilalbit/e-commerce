from datetime import timedelta, datetime, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException,status
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from jwt import InvalidTokenError

from app.modules.users.services import db_get_user_by_username
from .models import *

from app.core.utils import verify_password
from app.core.config import get_settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

token_dependency = Annotated[str, Depends(oauth2_scheme)]
form_dependency = Annotated[OAuth2PasswordRequestForm, Depends()]


def authenticate_user(username: str, password: str):
    db_user  = db_get_user_by_username(username)
    if db_user is None or not verify_password(db_user.password_hash,password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="incorrect username or password")
    return {
        "username": db_user.username,
        "id": db_user.id,
        "role": db_user.role,
    }

def create_access_token(user: UserSchema, expires_delta: timedelta = get_settings().access_token_expire_minutes):
    encode = {
        "username": user["username"],
        "id": str(user["id"]),
        "role": user["role"].value,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=expires_delta),
    }
    encode_jwt = jwt.encode(encode, get_settings().secret_key, algorithm=get_settings().algorithm)
    return encode_jwt
def verify_token(token: token_dependency):
    try:
        payload = jwt.decode(token, get_settings().secret_key, algorithms=[get_settings().algorithm])
        username: str = payload.get("username")
        id: int = payload.get("id")
        role: str = str(payload.get("role"))
        if username is None or id is None or role is None:
            return False
    except InvalidTokenError:
        return False
    return {
        "username": username,
        "id": id,
        "role": role
    }