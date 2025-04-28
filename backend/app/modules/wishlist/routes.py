from fastapi import APIRouter

from backend.app.dependencies import current_customer_dependency
from .services import *

router = APIRouter(
    prefix="/wishlist",
    tags=["wishlist"],
)


@router.get('/', response_model=WishlistPublic)
def get_wishlists(customer: current_customer_dependency):
    return db_get_wishlists(customer.id)


@router.post('/items', status_code=status.HTTP_201_CREATED)
def add_wishlist(product_id: uuid.UUID, customer: current_customer_dependency):
    return db_add_wishlist(customer.id, product_id)


@router.delete('/items/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_wishlist(id: uuid.UUID, customer: current_customer_dependency):
    return db_delete_wishlist(id, customer.id)


@router.delete('/items', status_code=status.HTTP_204_NO_CONTENT)
def clear_wishlist(customer: current_customer_dependency):
    return db_clear_wishlist(customer.id)