from fastapi import HTTPException, status


def admin_and_seller_only(user: dict):
    user_role = user["role"]
    if user_role != "admin" and user_role != "seller":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Only admin and seller authorized to do this operation"
        )
