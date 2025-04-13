from typing import Annotated

from fastapi import Depends, HTTPException, status

from app.dependencies import get_current_user


def admin_and_customer_only(user: Annotated[dict, Depends(get_current_user)]):
    user_role = user["role"]
    if user_role != "admin" and user_role != "customer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Only admin and customer authorized to do this operation"
        )