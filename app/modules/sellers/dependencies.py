from typing import Annotated

from fastapi import Depends, HTTPException, status

from app.dependencies import get_current_user


def admin_and_seller_only(user: Annotated[dict, Depends(get_current_user)]):
    user_role = user["role"]
    if user_role != "admin" and user_role != "seller":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Only seller and customer authorized to do this operation"
        )