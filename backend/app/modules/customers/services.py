from fastapi import HTTPException, status

from app.database import session
from app.dependencies import get_current_customer
from .models import *


def db_update_customer_account(user: dict, customer_data: CustomersUpdate):
    with session:
        db_customer = get_current_customer(user, session)
        customer_update = customer_data.model_dump(exclude_unset=True)
        db_customer.sqlmodel_update(customer_update)
        session.add(db_customer)
        session.commit()
        session.refresh(db_customer)
        return db_customer


def db_get_customer_info(user: dict):
    with session:
        db_user = session.get(Users, user["id"])
        if db_user.customer:
            return db_user
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User not Found")


def db_create_customer_account(user: dict, customer_data: CustomersCreate):
    with session:
        db_user = session.get(Users, user["id"])
        if not db_user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User not Found")
        db_customer = Customers.model_validate(customer_data)
        db_user.customer = db_customer
        session.add(db_customer)
        session.commit()
        return db_get_customer_info(user)
