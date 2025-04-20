from fastapi import APIRouter

from .services import *
from app.dependencies import current_user_dependency,admin_and_customer_only

router = APIRouter(
    prefix="/customers",
    tags=["customers"],
)


@router.patch('/')
def update_customer_account(user: current_user_dependency,customer_data: CustomersUpdate):
    admin_and_customer_only(user)
    return db_update_customer_account(user,customer_data)

@router.get('/',response_model=CustomerPublicWithUser)
def get_customer_info(user: current_user_dependency):
    admin_and_customer_only(user)
    return db_get_customer_info(user)
