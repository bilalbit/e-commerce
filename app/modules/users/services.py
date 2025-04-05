from app.database import session
from app.core.utils import hash_password

from .models import *

def db_create_user_account(user_data:UsersCreate):
    hashed_password = hash_password(user_data.password)
    with session:
        extra_data = {"hashed_password": hashed_password}
        db_user = Users.model_validate(user_data,update=extra_data)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user

