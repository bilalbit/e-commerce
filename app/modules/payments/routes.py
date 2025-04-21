from fastapi import APIRouter

from app.dependencies import current_customer_dependency, current_user_dependency
from .services import *
from app.core.security import admin_only

router = APIRouter(
    prefix="/payments",
    tags=["payments"],
)

@router.post('/')
def add_payment(payment_data: PaymentCreate,customer: current_customer_dependency):
    return db_add_payment(payment_data,customer.id)
@router.get('/{id}')
def get_payment_by_id(id: uuid.UUID,customer: current_customer_dependency):
    return db_get_payment_by_id(id,customer.id)
@router.get('/')
def get_payments(customer: current_customer_dependency):
    return db_get_payment(customer.id)
@router.patch('/{id}/status')
def update_payment_status(id: uuid.UUID,payment_status: PaymentStatus,user:current_user_dependency):
    admin_only(user)
    return db_update_payment_status(id,payment_status)