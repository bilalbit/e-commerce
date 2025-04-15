import uuid

from fastapi import HTTPException
from sqlmodel import Session, select

from app.database import session
from app.modules import Products
from .models import *
from ...core.services import get_record_by_id


def db_get_or_create_cart(customer_id: uuid.UUID, db_session: Session):
    db_cart = db_session.exec(select(Carts).filter(Carts.customer_id == customer_id)).first()
    if not db_cart:
        db_cart = Carts(customer_id=customer_id)
        db_session.add(db_cart)
        db_session.commit()
        db_session.refresh(db_cart)
    return db_cart

def db_get_cart(id:uuid.UUID):
    with session:
        db_cart = db_get_or_create_cart(id,session)
        if db_cart.cart_items is not None:
            return db_cart
        raise HTTPException(status_code=404, detail="Items list is Empty")
def db_add_cart_item(customer_id: uuid.UUID, cart_item_data: CartsCreate):
    with session:
        db_product = session.query(Products).filter(Products.id == cart_item_data.product_id).first()
        if not db_product:
            raise HTTPException(status_code=404, detail="Product not found")
        if not db_product.is_available:
            raise HTTPException(status_code=400, detail="Product is not available")
        if db_product.stock_quantity < cart_item_data.quantity:
            raise HTTPException(status_code=400, detail="Insufficient stock")

        db_cart = db_get_or_create_cart(customer_id,session)
        cart_item = session.query(CartItems).where(
            CartItems.cart_id == db_cart.id,
            CartItems.product_id == cart_item_data.product_id
        ).first()
        if cart_item:
            # Update quantity
            cart_item.quantity += cart_item_data.quantity
            if db_product.stock_quantity < cart_item.quantity:
                raise HTTPException(status_code=400, detail="Total quantity exceeds stock")
        else:
            cart_item = CartItems(cart_id=db_cart.id, product_id=cart_item_data.product_id,
                                  quantity=cart_item_data.quantity)
        session.add(cart_item)
        session.commit()
        session.refresh(db_cart)
        return db_cart
def db_update_cart_item(cart_item_id:uuid.UUID,customer_id: uuid.UUID,cart_data: CartsUpdate):
    with session:
        db_cart = session.exec(
            select(Carts).where(
                Carts.customer_id == customer_id,
            )
        ).one()
        if not db_cart.cart_items:
            raise HTTPException(status_code=404, detail="Cart is not found")
        db_cart_item = session.exec(
            select(CartItems).where(
                CartItems.cart_id == db_cart.id,
                CartItems.id == cart_item_id
            )
        ).one()
        if not db_cart_item:
            raise HTTPException(status_code=404, detail="Cart item not found")
        db_product = session.get(Products,db_cart_item.product_id)
        if not db_product or not db_product.is_available:
            raise HTTPException(status_code=400, detail="Product is not available")
        if db_product.stock_quantity < cart_data.quantity:
            raise HTTPException(status_code=400, detail="Insufficient stock")

        db_cart_item.quantity = cart_data.quantity
        session.add(db_cart_item)
        session.commit()
        session.refresh(db_cart_item)
        return db_cart
def db_delete_items(id:uuid.UUID,customer_id: uuid.UUID):
    with session:
        db_cart_item = session.get(CartItems,id)
        print("db_cart_item: ",db_cart_item)
        if db_cart_item is None or db_cart_item.cart.customer_id != customer_id:
            raise HTTPException(status_code=404, detail="Cart item not found")
        session.delete(db_cart_item)
        session.commit()
def db_clear_cart(customer_id: uuid.UUID):
    with session:
        db_cart = session.exec(
            select(Carts).where(
                Carts.customer_id == customer_id,
                )
        ).one()
        if not db_cart.cart_items:
            raise HTTPException(status_code=404, detail="Cart is not found")
        session.delete(db_cart)
        session.commit()

