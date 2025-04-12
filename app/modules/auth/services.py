from datetime import timedelta, datetime, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import InvalidTokenError

from app.core.config import get_settings
from app.core.utils import verify_password
from app.modules.users.services import db_get_user_by_username, db_create_user_account
from .models import *
from app.modules.customers.models import Customers
from app.modules.sellers.models import Sellers

from ...database import session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

token_dependency = Annotated[str, Depends(oauth2_scheme)]
form_dependency = Annotated[OAuth2PasswordRequestForm, Depends()]


def authenticate_user(username: str, password: str):
    db_user = db_get_user_by_username(username)
    if db_user is None or not verify_password(db_user.password_hash, password):
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


def db_create_customer_account(customer_data, role, user_data):
    with session:
        db_user = db_create_user_account(user_data, role)
        db_customer = Customers.model_validate(customer_data)
        db_user.customer = db_customer
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user


def db_create_seller_account(role, seller_data, user_data):
    with session:
        db_user = db_create_user_account(user_data, role)
        db_seller = Sellers.model_validate(seller_data)
        db_user.seller = db_seller
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user



