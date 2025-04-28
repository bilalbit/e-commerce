from fastapi import APIRouter

from backend.app.core.security import admin_and_customer_only, customer_only
from backend.app.dependencies import current_user_dependency
from .services import *

router = APIRouter(
    prefix="/customers",
    tags=["customers"],
)


@router.post('/', response_model=CustomerPublicWithUser, status_code=status.HTTP_201_CREATED)
def create_customer_account(user: current_user_dependency, customer_data: CustomersUpdate):
    customer_only(user)
    return db_create_customer_account(user, customer_data)


@router.patch('/', response_model=CustomerPublicWithUser)
def update_customer_account(user: current_user_dependency,customer_data: CustomersUpdate):
    admin_and_customer_only(user)
    return db_update_customer_account(user,customer_data)

@router.get('/',response_model=CustomerPublicWithUser)
def get_customer_info(user: current_user_dependency):
    admin_and_customer_only(user)
    return db_get_customer_info(user)
