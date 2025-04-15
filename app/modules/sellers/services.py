from fastapi import HTTPException, status
from sqlmodel import select

from app.database import session
from app.dependencies import get_current_user_data
from .models import *


def db_get_seller():
    with session:
        user_id = get_current_user_data()["id"]
        seller = session.exec(select(Sellers).where(Sellers.user_id == user_id)).one()
        return seller


def db_get_seller_info(id: uuid.UUID):
    with session:
        user_id = get_current_user_data()["id"]
        db_user = session.get(Users, user_id)
        if db_user.seller.id == id:
            return db_user
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User not Found")


def db_update_seller_info(id: uuid.UUID, seller_data: SellersUpdate):
    with session:
        user_id = get_current_user_data()["id"]
        db_seller = session.get(Sellers, id)
        if str(db_seller.user_id) != user_id:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User not Found")
        seller_update = seller_data.model_dump(exclude_unset=True)
        db_seller.sqlmodel_update(seller_update)
        session.add(db_seller)
        session.commit()
        session.refresh(db_seller)
        return db_seller


def db_verify_seller(id: uuid.UUID, verify: bool):
    with session:
        user_id = get_current_user_data()["id"]
        db_seller = session.get(Sellers, id)
        if str(db_seller.user_id) != user_id:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User not Found")
        db_seller.verified = verify
        session.add(db_seller)
        session.commit()
        session.refresh(db_seller)
        return db_seller
