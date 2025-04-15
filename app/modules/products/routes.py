from fastapi import APIRouter

from app.dependencies import current_user_dependency
from .services import *

router = APIRouter(
    prefix="/products",
    tags=["products"],
    # dependencies=[Depends(admin_and_customer_only)]
)
@router.post('/')
def add_product(product_data: ProductsCreate,user: current_user_dependency):
    return db_add_product(product_data)
@router.get('/')
def get_products():
    return db_get_products()
@router.get('/{id}')
def get_products_by_id(id: uuid.UUID):
    return db_get_products_by_id(id)

@router.patch('/{id}')
def update_product(id: uuid.UUID,product_data: ProductsUpdate,user: current_user_dependency):
    return db_update_product(id,product_data)
@router.delete('/{id}')
def delete_product(id: uuid.UUID,user: current_user_dependency):
    return db_delete_product(id)