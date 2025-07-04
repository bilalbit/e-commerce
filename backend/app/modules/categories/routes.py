from fastapi import APIRouter, status

from backend.app.core.security import admin_and_seller_only
from backend.app.dependencies import current_user_dependency
from .services import *

router = APIRouter(
    prefix="/categories",
    tags=["categories"],
)


@router.get('/')
def get_categories():
    return db_get_categories()


@router.get('/{id}')
def get_categories_by_id(id: uuid.UUID):
    return db_get_categories_by_id(id)


@router.post('/', status_code=status.HTTP_201_CREATED)
def add_categories(categories: CategoriesCreate, user: current_user_dependency):
    admin_and_seller_only(user)
    return db_add_categories(categories)


@router.patch('/{id}')
def update_categories(id: uuid.UUID, categories_data: CategoriesUpdate, user: current_user_dependency):
    admin_and_seller_only(user)
    return db_update_categories(id, categories_data)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_categories(id: uuid.UUID,  user: current_user_dependency):
    admin_and_seller_only(user)
    return db_delete_categories(id)
