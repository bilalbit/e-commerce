from fastapi import HTTPException, status

from backend.app.core.utils import verify_password, hash_password
from backend.app.database import session
from backend.app.modules.customers.models import Customers
from backend.app.modules.sellers.models import Sellers
from backend.app.modules.users.models import Users, UsersCreate
from .models import *


def db_get_user_by_username(username: str):
    with session:
        return session.query(Users).where(Users.username == username).first()


def db_create_user_account(user_data: UsersCreate, role: RoleType):
    password_hash = hash_password(user_data.password)
    with session:
        extra_data = {"password_hash": password_hash, "role": role}
        db_user = Users.model_validate(user_data, update=extra_data)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user


def db_register_user(user_data: UsersCreate):
    password_hash = hash_password(user_data.password)
    with session:
        extra_data = {"password_hash": password_hash}
        db_user = Users.model_validate(user_data, update=extra_data)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user


def authenticate_user(username: str, password: str):
    db_user = db_get_user_by_username(username)
    if db_user is None or not verify_password(db_user.password_hash, password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="incorrect username or password")
    return {
        "username": db_user.username,
        "id": db_user.id,
        "role": db_user.role,
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
