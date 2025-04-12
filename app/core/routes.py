from fastapi import APIRouter
from app.modules.auth.routes import router as auth_router
from app.modules.customers.routes import router as customer_router
from app.modules.users.routes import router as users_router
api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(customer_router)
api_router.include_router(users_router)