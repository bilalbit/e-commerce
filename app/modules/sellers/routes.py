from fastapi import APIRouter, Depends

from .dependencies import admin_and_seller_only
from .services import *

router = APIRouter(
    prefix="/sellers",
    tags=["sellers"],
    dependencies=[Depends(admin_and_seller_only)]
)



@router.get('/', response_model=SellersPublicWithUsers)
def get_seller_info(id: uuid.UUID):
    return db_get_seller_info(id)

@router.put('/{id}')
def update_seller_info(id: uuid.UUID,seller_data: SellersUpdate):
    return db_update_seller_info(id,seller_data)

@router.patch('/{id}')
def verify_seller(id: uuid.UUID,verify: bool):
    return db_verify_seller(id,verify)
