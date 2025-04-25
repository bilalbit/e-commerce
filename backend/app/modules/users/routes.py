from fastapi import APIRouter

from backend.app.dependencies import current_user_dependency
from .services import *

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get('/')
def get_user_info(user:current_user_dependency):
    return db_get_user_info(user["id"])


@router.patch('/')
def update_user_profile(user_data: UsersUpdate,user:current_user_dependency):
    return db_update_profile(user_data,user["id"])


@router.delete('/')
def delete_account(user:current_user_dependency):
    return db_delete_account(user["id"])


