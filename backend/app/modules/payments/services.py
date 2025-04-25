from fastapi import HTTPException, status
from sqlmodel import select

from app.database import session
from app.modules import Orders
from .models import *


def db_add_payment(payment_data: PaymentCreate, customer_id: uuid.UUID):
    with session:
        is_order_belong_to_customer = session.exec(
            select(Orders).where(
                Orders.id == payment_data.order_id,
                Orders.customer_id == customer_id,
            )
        ).first()
        if not is_order_belong_to_customer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        db_payment = Payments.model_validate(payment_data,
                                             update={
                                                 "customer_id": customer_id
                                             })
        session.add(db_payment)
        session.commit()
        session.refresh(db_payment)
        return db_payment


def db_get_payment(customer_id: uuid.UUID):
    with session:
        db_payment = session.exec(
            select(Payments).where(
                Payments.customer_id == customer_id
            )
        ).all()
        if db_payment:
            return db_payment
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment are empty")


def db_get_payment_by_id(id: uuid.UUID, customer_id: uuid.UUID):
    with session:
        db_payment = session.exec(
            select(Payments).where(
                Payments.customer_id == customer_id,
                Payments.id == id
            )
        ).first()
        if db_payment is not None:
            return db_payment
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")


def db_update_payment_status(id: uuid.UUID, payment_status: PaymentStatus):
    with session:
        db_payment = session.get(Payments, id)
        if db_payment is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")
        db_payment.status = payment_status
        session.add(db_payment)
        session.commit()
        session.refresh(db_payment)
        return db_payment
