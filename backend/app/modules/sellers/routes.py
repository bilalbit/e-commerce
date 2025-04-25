from fastapi import APIRouter

from backend.app.core.security import admin_only, seller_only
from backend.app.dependencies import current_user_dependency
from .services import *

router = APIRouter(
    prefix="/sellers",
    tags=["sellers"],
)



@router.get('/', response_model=SellersPublicWithUsers)
def get_seller_info(user:current_user_dependency):
    return db_get_seller_info(user)


@router.post('/')
def create_seller_info(seller_data: SellersUpdate, user: current_user_dependency):
    seller_only(user)
    return db_create_seller_info(user, seller_data)
@router.put('/')
def update_seller_info(seller_data: SellersUpdate,user:current_user_dependency):
    return db_update_seller_info(seller_data,user)

@router.patch('/{id}')
def verify_seller(id:uuid.UUID,verify: bool,user:current_user_dependency):
    admin_only(user)
    return db_verify_seller(id,verify)
