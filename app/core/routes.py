from fastapi import APIRouter
from app.modules.users.routes import router as users_router
from app.modules.auth.routes import router as auth_router
from app.modules.customers.routes import router as customers_router
from app.modules.sellers.routes import router as sellers_router
from app.modules.categories.routes import router as categories_router
from app.modules.products.routes import router as products_router
from app.modules.carts.routes import router as carts_router
from app.modules.wishlist.routes import router as wishlist_router
api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(customers_router)
api_router.include_router(sellers_router)
api_router.include_router(categories_router)
api_router.include_router(products_router)
api_router.include_router(carts_router)
api_router.include_router(wishlist_router)
