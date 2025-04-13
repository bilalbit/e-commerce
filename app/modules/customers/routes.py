from fastapi import APIRouter, Depends

from .dependencies import admin_and_customer_only
from .services import *

router = APIRouter(
    prefix="/customers",
    tags=["customers"],
    dependencies=[Depends(admin_and_customer_only)]
)


@router.patch('/{id}')
def update_customer_account(id: uuid.UUID,customer_data: CustomersUpdate):
    return db_update_customer_account(id,customer_data)

@router.get('/',response_model=CustomerPublicWithUser)
def get_customer_info(id: uuid.UUID):
    return db_get_customer_info(id)
