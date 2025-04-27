from fastapi import APIRouter

from backend.app.core.exceptions import exception_dependencies
from backend.app.modules.auth.routes import router as auth_router
from backend.app.modules.carts.routes import router as carts_router
from backend.app.modules.categories.routes import router as categories_router
from backend.app.modules.coupons.routes import router as coupons_router
from backend.app.modules.customers.routes import router as customers_router
from backend.app.modules.order.routes import router as order_router
from backend.app.modules.payments.routes import router as payment_router
from backend.app.modules.products.routes import router as products_router
from backend.app.modules.reviews.routes import router as reviews_router
from backend.app.modules.sellers.routes import router as sellers_router
from backend.app.modules.users.routes import router as users_router
from backend.app.modules.wishlist.routes import router as wishlist_router

api_routes = APIRouter(
    dependencies=exception_dependencies
)

api_routes.include_router(auth_router)
api_routes.include_router(users_router)
api_routes.include_router(customers_router)
api_routes.include_router(sellers_router)
api_routes.include_router(categories_router)
api_routes.include_router(products_router)
api_routes.include_router(carts_router)
api_routes.include_router(wishlist_router)
api_routes.include_router(order_router)
api_routes.include_router(payment_router)
api_routes.include_router(coupons_router)
api_routes.include_router(reviews_router)
