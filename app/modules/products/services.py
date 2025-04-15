from app.database import session
from app.modules.sellers.services import db_get_seller
from .models import *
from app.core.services import get_record_by_id


def db_add_product(product_data: ProductsCreate):
    with session:
        seller_id = db_get_seller().id
        db_product = Products.model_validate(product_data,update={"seller_id": seller_id})
        session.add(db_product)
        session.commit()
        session.refresh(db_product)
        return db_product
def db_get_products():
    with session:
        sellers = session.query(Products).all()
        return sellers
def db_get_products_by_id(id: uuid.UUID):
    with session:
        return get_record_by_id(id, Products,"products")
def db_update_product(id: uuid.UUID, product_data: ProductsUpdate):
    with session:
        db_product = db_get_products_by_id(id)
        product_update = product_data.model_dump(exclude_unset=True)
        db_product.sqlmodel_update(product_update)
        session.add(db_product)
        session.commit()
        session.refresh(db_product)
        return db_product
def db_delete_product(id: uuid.UUID):
    with session:
        db_product = db_get_products_by_id(id)
        session.delete(db_product)
        session.commit()


