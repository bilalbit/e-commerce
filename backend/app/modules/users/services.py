from fastapi import HTTPException, status

from app.core.utils import hash_password
from app.database import session
from .models import *


def db_get_user_by_phone(phone_number: str):
    with session:
        return session.query(Users).where(Users.phone_number == phone_number).first()


def db_get_user_info(user_id: uuid.UUID):
    with session:
        db_user = session.get(Users, user_id)
        if db_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return db_user


def db_update_profile(user_data: UsersUpdate,user_id: uuid.UUID):
    with session:
        extra_data = {}
        if user_data.password is not None:
            extra_data = {"password_hash": hash_password(user_data.password)}
        db_user = db_get_user_info(user_id)
        updated_user = user_data.model_dump(exclude_unset=True)
        db_user.sqlmodel_update(updated_user, update=extra_data)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user


def db_delete_account():
    with session:
        db_user = db_get_user_info()
        session.delete(db_user)
        session.commit()
