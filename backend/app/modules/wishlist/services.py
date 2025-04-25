from fastapi import HTTPException, status
from sqlmodel import select, Session

from app.database import session
from .models import *


def db_get_or_create_wishlist(db: Session, customer_id: uuid.UUID):
    db_wishlist = db.exec(select(Wishlists).where(Wishlists.customer_id == customer_id)).first()
    if db_wishlist is None:
        db_wishlist = Wishlists(customer_id=customer_id)
        db.add(db_wishlist)
        db.commit()
        db.refresh(db_wishlist)
    return db_wishlist


def db_get_wishlists(customer_id: uuid.UUID):
    with session:
        db_wishlist = db_get_or_create_wishlist(session, customer_id)
        if db_wishlist.wishlist_items:
            return db_wishlist
        raise HTTPException(status_code=404, detail="wishlist items is Not found")


def db_add_wishlist(customer_id: uuid.UUID, product_id: uuid.UUID):
    with session:
        db_wishlist = db_get_or_create_wishlist(session, customer_id)
        is_product_added = session.exec(
            select(Wishlist_Items).where(
                Wishlist_Items.product_id == product_id,
                Wishlist_Items.wishlist_id == db_wishlist.id
            )
        ).first()
        if is_product_added:
            raise HTTPException(status_code=status.HTTP_412_PRECONDITION_FAILED, detail="product already added")

        db_wishlist_item = Wishlist_Items(product_id=product_id,
                                          wishlist_id=db_wishlist.id)
        db_wishlist.wishlist_items.append(db_wishlist_item)
        session.add(db_wishlist)
        session.commit()
        session.refresh(db_wishlist)
        return db_wishlist


def db_delete_wishlist(wishlist_item_id: uuid.UUID, customer_id: uuid.UUID):
    with session:
        db_wishlist = db_get_or_create_wishlist(session, customer_id)
        db_wishlist_item = session.exec(
            select(Wishlist_Items).where(
                Wishlist_Items.id == wishlist_item_id,
                Wishlist_Items.wishlist_id == db_wishlist.id
            )
        ).first()
        if db_wishlist_item is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="wishlist item  not found")
        session.delete(db_wishlist_item)
        session.commit()


def db_clear_wishlist(customer_id: uuid.UUID):
    with session:
        db_wishlist = session.exec(select(Wishlists).where(Wishlists.customer_id == customer_id)).first()
        if db_wishlist:
            session.delete(db_wishlist)
            session.commit()
