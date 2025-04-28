from fastapi import HTTPException, status

from backend.app.database import session
from backend.app.dependencies import get_current_seller
from .models import *


def db_get_seller_info(user: dict):
    with session:
        db_user = session.get(Users, user["id"])
        if db_user.seller:
            return db_user
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="seller not Found")


def db_create_seller_info(user: dict, seller_data: SellersCreate):
    with session:
        db_user = session.get(Users, user["id"])
        if not db_user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User not Found")
        db_seller = Sellers.model_validate(seller_data)
        db_user.seller = db_seller
        session.add(db_user)
        session.commit()
        return db_get_seller_info(user)

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
