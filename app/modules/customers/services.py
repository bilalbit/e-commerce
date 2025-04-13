from fastapi import HTTPException,status

from app.core.services import get_record_by_id
from app.database import session
from .models import *
from app.dependencies import get_current_user_data


def db_update_customer_account(id: uuid.UUID,customer_data: CustomersUpdate):
    with session:
        user_id = get_current_user_data()["id"]
        db_customer = get_record_by_id(id, Customers,"customer")
        if user_id != str(db_customer.user_id):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User not Found")
        customer_update = customer_data.model_dump(exclude_unset=True)
        db_customer.sqlmodel_update(customer_update)
        session.add(db_customer)
        session.commit()
        session.refresh(db_customer)
        return db_customer

def db_get_customer_info(id: uuid.UUID):
    with session:
        user_id = get_current_user_data()["id"]
        db_user = session.get(Users,user_id)
        if db_user.customer.id == id:
            return db_user
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User not Found")
