import uuid

from fastapi import APIRouter

from .services import *
from .dependencies import current_customer_dependency

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)
@router.post('/',response_model=OrdersPublic)
def create_order(shipping_address: str,customer:current_customer_dependency):
    return db_create_order(shipping_address,customer.id)
@router.get('/',response_model=list[Orders])
def get_orders(customer:current_customer_dependency):
    return db_get_orders(customer.id)
@router.get('/{id}',response_model=OrdersPublic)
def get_order_by_id(id: uuid.UUID,customer:current_customer_dependency):
    return db_get_order_by_id(id,customer.id)
@router.patch('/{id}',response_model=OrdersPublic)
def update_order_status(id: uuid.UUID,status: OrderStatus,customer:current_customer_dependency):
    return db_update_order_status(id,customer.id,status)