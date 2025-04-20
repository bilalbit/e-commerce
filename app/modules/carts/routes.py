from fastapi import APIRouter

from .services import *
from app.dependencies import current_customer_dependency

router = APIRouter(
    prefix="/carts",
    tags=["carts"],
)

@router.get("/",response_model=CartsPublic)
def get_cart(customer: current_customer_dependency):
    return db_get_cart(customer.id)

@router.post("/items")
def add_cart_item(cart_item_data: CartsCreate,customer: current_customer_dependency):
    return db_add_cart_item(customer.id,cart_item_data)
@router.patch("/items/{id}")
def update_cart_item(id:uuid.UUID,customer: current_customer_dependency,cart_item_data: CartsUpdate):
    return db_update_cart_item(id,customer.id,cart_item_data)
@router.delete("/items/{id}")
def delete_items(id:uuid.UUID,customer: current_customer_dependency):
    return db_delete_items(id,customer.id)

@router.delete("/items")
def clear_cart(customer: current_customer_dependency):
    return db_clear_cart(customer.id)
