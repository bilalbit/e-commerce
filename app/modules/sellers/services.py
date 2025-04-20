from fastapi import HTTPException, status
from sqlmodel import select

from app.database import session
from app.dependencies import get_current_user_data, get_current_seller
from .models import *


def db_get_seller():
    with session:
        user_id = get_current_user_data()["id"]
        seller = session.exec(select(Sellers).where(Sellers.user_id == user_id)).one()
        return seller


def db_get_seller_info(user: dict):
    with session:
        db_user = session.get(Users, user["id"])
        if db_user.seller:
            return db_user
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User not Found")


def db_update_seller_info(seller_data: SellersUpdate,user: dict):
    with session:
        db_seller = get_current_seller(user,session)
        seller_update = seller_data.model_dump(exclude_unset=True)
        db_seller.sqlmodel_update(seller_update)
        session.add(db_seller)
        session.commit()
        session.refresh(db_seller)
        return db_seller


def db_verify_seller(id: uuid.UUID, verify: bool):
    with session:
        db_seller = session.get(Sellers, id)
        db_seller.verified = verify
        session.add(db_seller)
        session.commit()
        session.refresh(db_seller)
        return db_seller
