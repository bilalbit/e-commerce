from app.core.utils import hash_password
from app.database import session
from .models import *


def db_create_user_account(user_data: UsersCreate,role:RoleType):
    password_hash = hash_password(user_data.password)
    with session:
        extra_data = {"password_hash": password_hash,"role": role}
        db_user = Users.model_validate(user_data, update=extra_data)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user


def db_get_user_by_email(email: str):
    with session:
        return session.query(Users).where(Users.email == email).one()


def db_get_user_by_phone(phone_number: str):
    with session:
        return session.query(Users).where(Users.phone_number == phone_number).one()
