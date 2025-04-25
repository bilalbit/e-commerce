from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from backend.app.core.security import verify_token, create_access_token
from backend.app.modules.customers.models import *
from backend.app.modules.sellers.models import SellersCreate
from .services import *

form_dependency = Annotated[OAuth2PasswordRequestForm, Depends()]
router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post('/register')
def register(user_data: UsersCreate):
    return db_register_user(user_data)

@router.post('/register/{role}')
def register_with_role(role: RoleType,
             user_data: UsersCreate,
             customer_data: CustomersCreate | None = None,
             seller_data: SellersCreate | None = None):
    if customer_data is not None and seller_data is not None:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail="only one account can be created at a time😑.either as a seller or customer.")
    if role is RoleType.customer:
        if customer_data is None:
            raise HTTPException(status_code=status.HTTP_424_FAILED_DEPENDENCY, detail="customer data is required.")
        return db_create_customer_account(customer_data, role, user_data)
    elif role is RoleType.seller:
        if seller_data is None:
            raise HTTPException(status_code=status.HTTP_424_FAILED_DEPENDENCY, detail="seller data is required.")
        return db_create_seller_account(role, seller_data, user_data)
    else:
        return db_create_user_account(user_data, role)


@router.get("/verify-token")
async def verify_user_token(token: str):
    return verify_token(token)




@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: form_dependency):
    user = authenticate_user(form_data.username, form_data.password)
    token = create_access_token(user)
    print(token)
    return {
        "access_token": token,
        "token_type": "bearer"
    }
