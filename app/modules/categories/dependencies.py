from typing import Annotated

from fastapi import Depends, HTTPException, status

from app.dependencies import get_current_user

current_user_dependency = Annotated[dict, Depends(get_current_user)]
def admin_and_seller_only(user: dict):
    user_role = user["role"]
    if user_role != "admin" and user_role != "seller":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Only admin and seller authorized to do this operation"
        )
