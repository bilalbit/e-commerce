from fastapi import APIRouter

from app.dependencies import current_customer_dependency, admin_and_seller_only, current_user_dependency
from .services import *

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)


@router.post('/', response_model=OrdersWithOrder_ItemsPublic)
def add_order_from_cart(shipping_address: str, customer: current_customer_dependency):
    return db_create_order(shipping_address, customer.id)


@router.post('/{product_id}', response_model=OrdersWithOrder_ItemsPublic)
def add_order_on_one_product(product_id: uuid.UUID, order_create: OrderCreate, customer: current_customer_dependency):
    return db_add_product_to_order(product_id, order_create, customer.id)


@router.get('/', response_model=list[Orders])
def get_orders(customer: current_customer_dependency):
    return db_get_orders(customer.id)


@router.get('/{id}', response_model=OrdersWithOrder_ItemsPublic)
def get_order_by_id(id: uuid.UUID, customer: current_customer_dependency):
    return db_get_order_of_customer_by_id(id, customer.id)


@router.patch('/{id}', response_model=OrdersPublic)
def update_order_status(id: uuid.UUID, order_status: OrderStatus, user: current_user_dependency):
    admin_and_seller_only(user)
    return db_update_order_status(id, order_status)
