
from fastapi import APIRouter, HTTPException,status

from app.database import session
from app.modules.sellers.models import SellersCreate
from app.modules.users.models import *
from app.modules.customers.models import *
from app.modules.users.services import db_create_user_account

router = APIRouter(
    tags=["auth"]
)


@router.post('/register/{role}')
def register(role: RoleType,user_data:UsersCreate,customer_data:CustomersCreate | None = None,seller_data: SellersCreate | None = None):
    if customer_data is not None and seller_data is not None:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail="only one account can be created at a time😑.either as a seller or customer.")
    with session:
        if role is RoleType.customer:
            if customer_data is None:
                raise HTTPException(status_code=status.HTTP_424_FAILED_DEPENDENCY,detail="customer data is required.")
            db_user = db_create_user_account(user_data,role)
            db_customer = Customers.model_validate(customer_data)
            db_user.customer = db_customer
            session.add(db_user)
            session.commit()
            session.refresh(db_user)
            return db_user
        elif role is RoleType.seller:
            if seller_data is None:
                raise HTTPException(status_code=status.HTTP_424_FAILED_DEPENDENCY,detail="seller data is required.")
            db_user = db_create_user_account(user_data,role)
            db_seller = Sellers.model_validate(seller_data)
            db_user.seller = db_seller
            session.add(db_user)
            session.commit()
            session.refresh(db_user)
            return db_user
        else:
            return db_create_user_account(user_data,role)
