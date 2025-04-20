from contextvars import ContextVar
from typing import Annotated

from fastapi import HTTPException, status, Depends
from sqlmodel import Session, select

from app.core.security import current_user_dependency
from app.database import session
from app.modules import Customers, Sellers

current_user_context: ContextVar[dict | None] = ContextVar("current_user_context", default=None)


def get_current_user_data():
    return current_user_context.get()


def get_current_customer(user: current_user_dependency,db_session:Session = session):
    if user["role"] != "customer":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Customer role required")
    with db_session:
        customer = db_session.exec(
            select(Customers).where(
                Customers.user_id == user["id"]
            )
        ).first()
        if not customer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
        return customer


def get_current_seller(user: current_user_dependency,db_session:Session = session):
    if user["role"] != "seller":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Seller role required")
    with db_session:
        seller = db_session.exec(
            select(Sellers).where(
                Sellers.user_id == user["id"]
            )
        ).first()
        if not seller:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Seller not found")
        return seller


def get_current_admin(user: current_user_dependency,db_session:Session = session):
    if user["role"] != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin role required")
    with db_session:
        admin = db_session.exec(
            select(Sellers).where(
                Sellers.user_id == user["id"]
            )
        ).first()
        if not admin:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin not found")
        return admin


current_customer_dependency = Annotated[dict, Depends(get_current_customer)]
current_seller_dependency = Annotated[dict, Depends(get_current_seller)]
current_admin_dependency = Annotated[dict, Depends(get_current_admin)]


def admin_and_customer_only(user: current_user_dependency):
    user_role = user["role"]
    if user_role != "admin" and user_role != "customer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Only admin and customer authorized to do this operation"
        )


def admin_and_seller_only(user: current_user_dependency):
    user_role = user["role"]
    if user_role != "admin" and user_role != "seller":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Only seller and customer authorized to do this operation"
        )
