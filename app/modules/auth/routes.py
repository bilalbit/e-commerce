
from fastapi import APIRouter

from app.database import session
from app.modules.users.models import *
from app.modules.customers.models import *
from app.modules.users.services import db_create_user_account

router = APIRouter(
    tags=["auth"]
)


@router.post('/register/{role}')
def register(role: RoleType,user_data:UsersCreate,customer_data:CustomersCreate | None = None):
    with session:
        if role is RoleType.customer:
            db_user = db_create_user_account(user_data)
            db_customer = Customers.model_validate(customer_data)
            db_user.customer = db_customer
            session.add(db_user)
            session.commit()
            session.refresh(db_user)
            return db_user
        elif role is RoleType.seller:
            return RoleType.seller
        else:
            return RoleType.admin
