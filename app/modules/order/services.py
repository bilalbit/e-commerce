from fastapi import HTTPException
from sqlmodel import select, Session

from app.core.services import get_record_by_id
from app.database import session
from app.modules import Products
from app.modules.carts.services import db_get_cart, db_clear_cart
from app.modules.products.services import db_update_product
from .models import *
from ..products.models import ProductsUpdate


def db_get_order_by_id(order_id: uuid.UUID,customer_id: uuid.UUID,db_session: Session = session):
    with db_session:
        db_order = db_session.exec(
            select(Orders).where(
                Orders.id == order_id,
                Orders.customer_id == customer_id,
            )
        ).one()
        if db_order is not None and db_order.order_items:
            return db_order
        raise HTTPException(status_code=404,detail="not found")

def db_get_orders(customer_id: uuid.UUID):
    with session:
        db_orders = session.exec(
            select(Orders).where(
                Orders.customer_id == customer_id,
            )
        ).all()
        return db_orders

def db_create_order(shipping_address: str, customer_id: uuid.UUID):
    with session:
        db_cart = db_get_cart(customer_id)
        db_cart_items = db_cart.cart_items
        total_amount = Decimal("0.00")
        order_items_data:list["OrderItem"] = []
        for item in db_cart_items:
            db_product = get_record_by_id(item.product_id, Products,"products")
            price_at_purchase = Decimal(str(db_product.price))
            total_amount += price_at_purchase * item.quantity
            db_update_product(db_product.id,ProductsUpdate(stock_quantity = db_product.stock_quantity - item.quantity))
            order_items_data.append(
                OrderItem(
                    product_id= db_product.id,
                    quantity = item.quantity,
                    price_at_purchase= price_at_purchase
                )
            )


        db_order = Orders(
            customer_id=customer_id,
            shipping_address=shipping_address,
            total_amount=total_amount
        )
        db_order.order_items = order_items_data
        db_order_id = db_order.id
        session.add(db_order)
        session.commit()
        session.refresh(db_order)
        db_clear_cart(customer_id)

        return get_record_by_id(db_order_id,Orders,"Order")
def db_update_order_status(id: uuid.UUID,customer_id: uuid.UUID,status: OrderStatus):
    with session:
        db_order = db_get_order_by_id(id,customer_id,session)
        db_order.status = status
        session.add(db_order)
        session.commit()
        session.refresh(db_order)
        return db_order
