from fastapi import APIRouter

from .dependencies import current_customer_dependency
from .services import *

router = APIRouter(
    prefix="/coupons",
    tags=["coupons"],
)
@router.post('/')
def create_coupon(coupon_data: CouponsCreate):
    return db_create_coupon(coupon_data)
@router.get('/')
def get_coupons():
    return db_get_coupons()
@router.get('/{id}')
def get_coupons_by_id(id: uuid.UUID):
    return db_get_coupons_by_id(id)
@router.patch('/{id}')
def update_coupon(id: uuid.UUID,coupon_data:CouponsUpdate):
    return db_update_coupon(id,coupon_data)
@router.post('/apply')
def apply_coupon(coupon_apply:CouponApply,customer: current_customer_dependency):
    return db_apply_coupon(coupon_apply,customer.id)
