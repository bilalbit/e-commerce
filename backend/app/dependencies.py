from typing import Annotated

from fastapi import HTTPException, status, Depends
from sqlmodel import Session, select

from backend.app.core.security import current_user
from backend.app.database import session
from backend.app.modules import Customers, Sellers, Users

current_user_dependency = Annotated[dict, current_user]


def get_current_customer(user: current_user_dependency, db_session: Session = Depends(lambda: session)):
    if user["role"] != "customer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Customer role required")
    with db_session:
        customer = db_session.exec(
            select(Customers).where(
                Customers.user_id == user["id"]
            )
        ).first()
        if not customer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
        return customer


def get_current_seller(user: current_user_dependency, db_session: Session = Depends(lambda: session)):
    if user["role"] != "seller":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Seller role required")
    with db_session:
        seller = db_session.exec(
            select(Sellers).where(Sellers.user_id == user["id"])
        ).first()
        if not seller:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Seller not found")
        return seller


def get_current_admin(user: current_user_dependency,db_session: Session = Depends(lambda: session)):
    if user["role"] != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Admin role required")
    with db_session:
        admin = db_session.exec(
            select(Sellers).where(
                Sellers.user_id == user["id"]
            )
        ).first()
        if not admin:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin not found")
        return admin


current_customer_dependency = Annotated[Customers, Depends(get_current_customer)]
current_seller_dependency = Annotated[Sellers, Depends(get_current_seller)]
current_admin_dependency = Annotated[Users, Depends(get_current_admin)]


