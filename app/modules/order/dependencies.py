from typing import Annotated

from fastapi import HTTPException, status, Depends

from app.database import session
from app.dependencies import current_user_dependency
from app.modules import Customers


def get_current_customer(user: current_user_dependency):
    if user["role"] != "customer":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized as customer")
    with session:
        customer = session.query(Customers).filter(Customers.user_id == user["id"]).first()
        if not customer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer profile not found")
        return customer


current_customer_dependency = Annotated[dict, Depends(get_current_customer)]
