from fastapi import APIRouter
from app.modules.auth.routes import router as auth_router
from app.modules.customers.routes import router as customers_router
from app.modules.sellers.routes import router as sellers_router
from app.modules.users.routes import router as users_router
api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(customers_router)
api_router.include_router(sellers_router)
api_router.include_router(users_router)