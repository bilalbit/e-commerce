from fastapi import APIRouter

from .services import *
from .dependencies import current_customer_dependency

router = APIRouter(
    prefix="/wishlist",
    tags=["wishlist"],
)


@router.get('/', response_model=WishlistPublic)
def get_wishlists(customer: current_customer_dependency):
    return db_get_wishlists(customer.id)


@router.post('/items')
def add_wishlist(product_id: uuid.UUID, customer: current_customer_dependency):
    return db_add_wishlist(customer.id, product_id)


@router.delete('/items/{id}')
def delete_wishlist(id: uuid.UUID, customer: current_customer_dependency):
    return db_delete_wishlist(id, customer.id)
@router.delete('/items')
def clear_wishlist(customer: current_customer_dependency):
    return db_clear_wishlist(customer.id)