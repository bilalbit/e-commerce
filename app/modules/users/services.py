from app.database import session
from .models import *


def db_create_user_account(user_data:UsersCreate):
    with session:
        db_user = Users.model_validate(user_data)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user

