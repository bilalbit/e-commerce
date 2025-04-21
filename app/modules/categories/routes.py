from fastapi import APIRouter

from app.dependencies import admin_and_seller_only, current_user_dependency
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


@router.post('/')
def add_categories(categories: CategoriesCreate, user: current_user_dependency):
    admin_and_seller_only(user)
    return db_add_categories(categories)


@router.patch('/{id}')
def update_categories(id: uuid.UUID, categories_data: CategoriesUpdate, user: current_user_dependency):
    admin_and_seller_only(user)
    return db_update_categories(id, categories_data)


@router.delete('/{id}')
def delete_categories(id: uuid.UUID,  user: current_user_dependency):
    admin_and_seller_only(user)
    return db_delete_categories(id)
