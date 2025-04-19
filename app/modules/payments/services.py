import uuid

from fastapi import HTTPException
from sqlmodel import select

from .models import *
from app.database import session


def db_add_payment(payment_data: PaymentCreate, customer_id: uuid.UUID):
    with session:
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
        if not db_payment:
            return db_payment
        raise HTTPException(status_code=404, detail="Payment are empty")


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
        raise HTTPException(status_code=404, detail="Payment not found")


def db_update_payment_status(id: uuid.UUID, status: PaymentStatus):
    with session:
        db_payment = session.get(Payments, id)
        if db_payment is None:
            raise HTTPException(status_code=404, detail="Payment not found")
        db_payment.status = status
        session.add(db_payment)
        session.commit()
        session.refresh(db_payment)
        return db_payment
