from .home import router as home_router
from .optimization import router as optimization_router
from .orders import router as orders_router
from .routes import router as routes_router

__all__ = [
    "home_router",
    "optimization_router",
    "orders_router",
    "routes_router",
]
