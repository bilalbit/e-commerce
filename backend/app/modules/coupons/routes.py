from fastapi import APIRouter, status

from backend.app.core.security import admin_and_seller_only
from backend.app.dependencies import current_customer_dependency
from .services import *

router = APIRouter(
    prefix="/coupons",
    tags=["coupons"],
)


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_coupon(coupon_data: CouponsCreate,user:current_customer_dependency):
    admin_and_seller_only(user)
    return db_create_coupon(coupon_data)
@router.get('/')
def get_coupons():
    return db_get_coupons()
@router.get('/{id}')
def get_coupons_by_id(id: uuid.UUID):
    return db_get_coupons_by_id(id)
@router.patch('/{id}')
def update_coupon(id: uuid.UUID,coupon_data:CouponsUpdate,user:current_customer_dependency):
    admin_and_seller_only(user)
    return db_update_coupon(id,coupon_data)


@router.post('/apply', status_code=status.HTTP_204_NO_CONTENT)
def apply_coupon(coupon_apply:CouponApply,customer: current_customer_dependency):
    return db_apply_coupon(coupon_apply,customer.id)
