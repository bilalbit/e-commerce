from fastapi import HTTPException
from sqlmodel import select, Session

from backend.app.database import session
from backend.app.modules.order.services import db_get_order_by_customer_id_and_order_id
from .models import *
from ..order.models import OrderStatus


def db_create_coupon(coupon_data: CouponsCreate):
    with session:
        db_coupon = Coupons.model_validate(coupon_data)
        session.add(db_coupon)
        session.commit()
        session.refresh(db_coupon)
        return db_coupon


def db_get_coupons():
    with session:
        current_time = datetime.now(timezone.utc)
        db_coupons = session.exec(
            select(Coupons).where(
                Coupons.is_active == True,
                Coupons.expiry_date >= current_time
            )
        ).all()
        if db_coupons:
            return db_coupons
        raise HTTPException(status_code=404, detail="Coupon not found")


def db_get_coupons_by_code(code: str, db_session: Session = session):
    with db_session:
        current_time = datetime.now(timezone.utc).replace(tzinfo=None)
        db_coupons = db_session.exec(
            select(Coupons).where(
                Coupons.code == code
            )
        ).first()
        if db_coupons is None:
            raise HTTPException(status_code=404, detail="Coupon not found")

        if db_coupons.expiry_date <= current_time:
            raise HTTPException(status_code=404, detail="Coupon is expired")
        elif not db_coupons.is_active:
            raise HTTPException(status_code=404, detail="Coupon is not active")

        return db_coupons


def db_get_coupons_by_id(id: uuid.UUID):
    with session:
        db_coupon = session.get(Coupons, id)
        if db_coupon:
            return db_coupon
        raise HTTPException(status_code=404, detail="Coupon not found")


def db_get_coupon_usage_by_customer_id_and_coupon_id(customer_id: uuid.UUID, coupon_id: uuid.UUID,
                                                     db_session: Session = session):
    with db_session:
        db_coupon = db_session.exec(
            select(Coupon_Usage).where(
                Coupon_Usage.customer_id == customer_id,
                Coupon_Usage.coupon_id == coupon_id

            )
        ).first()
        if db_coupon:
            return db_coupon


def db_update_coupon(id: uuid.UUID, coupon_data: CouponsUpdate):
    with session:
        db_coupon = db_get_coupons_by_id(id)
        coupon_update = coupon_data.model_dump(exclude_unset=True)
        db_coupon.sqlmodel_update(coupon_update)
        session.add(db_coupon)
        session.commit()
        session.refresh(db_coupon)
        return db_coupon


def db_apply_coupon(coupon_apply: CouponApply, customer_id: uuid.UUID):
    with session:
        db_order = db_get_order_by_customer_id_and_order_id(coupon_apply.order_id, customer_id, session)
        if db_order.status != OrderStatus.pending:
            raise HTTPException(status_code=404, detail=f"order is already {db_order.status}")
        db_coupon = db_get_coupons_by_code(coupon_apply.code, session)
        if db_coupon.usage_count >= db_coupon.max_users:
            raise HTTPException(status_code=404, detail=f"coupons max is hit")
        if db_get_coupon_usage_by_customer_id_and_coupon_id(customer_id, db_coupon.id, session) is not None:
            raise HTTPException(status_code=404, detail="already used this coupon")
        discount = 0
        if db_coupon.discount_type == DiscountType.percentage:
            discount = db_order.total_amount * (db_coupon.discount_value / 100)
        else:
            discount = db_coupon.discount_value
        discount = min(discount, db_order.total_amount)
        db_order.total_amount -= discount
        session.add(db_order)
        db_coupon_usage = Coupon_Usage(
            coupon_id=db_coupon.id,
            order_id=db_order.id,
            customer_id=customer_id,
        )
        db_coupon.usage_count += 1
        session.add(db_coupon)
        session.add(db_coupon_usage)
        session.commit()
        session.refresh(db_coupon_usage)
        return db_coupon_usage
