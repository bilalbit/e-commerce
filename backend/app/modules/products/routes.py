from fastapi import APIRouter

from backend.app.dependencies import current_seller_dependency
from .services import *

router = APIRouter(
    prefix="/products",
    tags=["products"],
)
@router.post('/')
def add_product(product_data: ProductsCreate,seller: current_seller_dependency):
    return db_add_product(product_data,seller.id)
@router.get('/')
def get_products(filter_q: filter_query):
    return db_get_products(filter_q)
@router.get('/{id}')
def get_products_by_id(id: uuid.UUID):
    return db_get_products_by_id(id)

@router.patch('/{id}')
def update_product(id: uuid.UUID,product_data: ProductsUpdate,seller: current_seller_dependency):
    return db_update_product(id,product_data,seller.id)
@router.delete('/{id}')
def delete_product(id: uuid.UUID,seller: current_seller_dependency):
    return db_delete_product(id,seller.id)