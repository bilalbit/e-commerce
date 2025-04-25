from fastapi import HTTPException, status
from sqlmodel import select, Session

from backend.app.core.services import get_record_by_id
from backend.app.database import session
from backend.app.modules import Products
from backend.app.modules.carts.services import db_get_cart, db_clear_cart
from backend.app.modules.products.services import db_update_product_stock_quantity, db_get_products_by_id
from .models import *


def db_get_order_by_customer_id_and_order_id(order_id: uuid.UUID, customer_id: uuid.UUID, db_session: Session = session):
    with db_session:
        db_order = db_session.exec(
            select(Orders).where(
                Orders.id == order_id,
                Orders.customer_id == customer_id,
            )
        ).first()
        if db_order is not None and db_order.order_items:
            return db_order
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="order not found")


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
        db_cart = db_get_cart(customer_id, session)
        db_cart_items = db_cart.cart_items
        total_amount = Decimal("0.00")
        order_items_data: list["OrderItem"] = []
        for item in db_cart_items:
            db_product = get_record_by_id(item.product_id, Products, "products")
            price_at_purchase = Decimal(str(db_product.price))
            total_amount += price_at_purchase * item.quantity
            db_update_product_stock_quantity(db_product.id, db_product.stock_quantity - item.quantity)
            order_items_data.append(
                OrderItem(
                    product_id=db_product.id,
                    quantity=item.quantity,
                    price_at_purchase=price_at_purchase
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

        return db_get_order_by_customer_id_and_order_id(db_order_id, customer_id)


def db_add_product_to_order(product_id: uuid.UUID, order_create: OrderCreate, customer_id: uuid.UUID):
    with session:
        db_product = db_get_products_by_id(product_id)
        db_update_product_stock_quantity(db_product.id, order_create.quantity)
        price_at_purchase = Decimal(db_product.price)
        total_amount = price_at_purchase * order_create.quantity
        db_order_item = OrderItem(
            product_id=db_product.id,
            quantity=order_create.quantity,
            price_at_purchase=price_at_purchase
        )
        db_order = Orders(
            customer_id=customer_id,
            shipping_address=order_create.shipping_address,
            total_amount=total_amount
        )
        db_order.order_items.append(db_order_item)
        session.add(db_order)
        session.commit()
        session.refresh(db_order)
        return db_get_order_by_customer_id_and_order_id(db_order.id, customer_id)


def db_update_order_status(id: uuid.UUID, order_status: OrderStatus):
    with session:
        db_order = session.get(Orders, id)
        if db_order is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        db_order.status = order_status
        session.add(db_order)
        session.commit()
        session.refresh(db_order)
        return db_order
