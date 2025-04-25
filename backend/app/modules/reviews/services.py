from fastapi import HTTPException
from sqlmodel import select, Session

from backend.app.database import session
from backend.app.modules.order.models import OrderStatus
from backend.app.modules.order.services import db_get_order_by_customer_id_and_order_id
from .models import *


def db_add_review(customer_id: uuid.UUID, review_data: ReviewCreate):
    with session:
        db_order = db_get_order_by_customer_id_and_order_id(review_data.order_id, customer_id, session)
        if db_order.status != OrderStatus.delivered:
            raise HTTPException(status_code=404, detail="Order does not delivered yet")
        db_order_items = db_order.order_items
        is_product_included = any(order_item.product_id == review_data.product_id for order_item in db_order_items)
        if not is_product_included:
            raise HTTPException(status_code=404, detail="Product not included")

        db_review = Reviews.model_validate(review_data, update={"customer_id": customer_id})

        session.add(db_review)
        session.commit()
        session.refresh(db_review)
        return db_review


def db_get_product_review(product_id: uuid.UUID):
    with session:
        db_review = session.exec(
            select(Reviews).where(
                Reviews.product_id == product_id,
            )
        ).all()
        return db_review


def db_get_review_of_customer(id: uuid.UUID, customer_id: uuid.UUID, db_session: Session = session):
    with db_session:
        db_review = db_session.exec(
            select(Reviews).where(
                Reviews.id == id,
                Reviews.customer_id == customer_id,
            )
        ).first()
        if db_review is None:
            raise HTTPException(status_code=404, detail="Review not found")
        return db_review


def db_update_review(id: uuid.UUID, customer_id: uuid.UUID, review_data: ReviewUpdate):
    with (session):
        db_review = db_get_review_of_customer(id, customer_id, session)
        review_update = review_data.model_dump(exclude_unset=True)
        db_review.sqlmodel_update(review_update)
        session.add(db_review)
        session.commit()
        session.refresh(db_review)
        return db_review


def db_delete_review(id: uuid.UUID, customer_id: uuid.UUID):
    with session:
        db_review = db_get_review_of_customer(id, customer_id, session)
        session.delete(db_review)
        session.commit()
        return db_review
