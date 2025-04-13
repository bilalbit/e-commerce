from fastapi import APIRouter, Depends

from .services import *
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(get_current_user)]
)


@router.get('/')
def get_user_info():
    return db_get_user_info()


@router.patch('/')
def update_user_profile(user: UsersUpdate):
    return db_update_profile(user)


@router.delete('/')
def delete_account():
    return db_delete_account()

@router.delete('/{user_id}')
def soft_delete_account(user_id: uuid.UUID):
    return db_soft_delete_account(user_id)
