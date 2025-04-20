from datetime import datetime, timezone, timedelta
from typing import Annotated

import jwt
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from starlette import status

from app.core.config import get_settings
from app.core.models import UserSchema

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
token_dependency = Annotated[str, Depends(oauth2_scheme)]

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
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, get_settings().secret_key, algorithms=[get_settings().algorithm])
        username: str = payload.get("username")
        id: str = payload.get("id")
        role: str = str(payload.get("role"))
        if username is None or id is None or role is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    return {
        "username": username,
        "id": id,
        "role": role
    }
