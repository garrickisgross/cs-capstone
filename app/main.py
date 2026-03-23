from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .db.in_memory import InMemoryStorage
from .routers.home import router as home_router
from .routers.optimization import router as optimization_router
from .routers.orders import router as orders_router
from .routers.routes import router as routes_router
from .services.optimization import OptimizationService
from .services.orders import OrdersService
from .services.routes import RoutesService

APP_DIR = Path(__file__).resolve().parent
STATIC_DIR = APP_DIR / "static"
TEMPLATES_DIR = APP_DIR / "templates"


def create_app() -> FastAPI:
    app = FastAPI()

    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
    app.state.templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

    storage = InMemoryStorage()
    app.state.storage = storage
    app.state.orders_service = OrdersService(storage)
    app.state.routes_service = RoutesService(storage)
    app.state.optimization_service = OptimizationService()

    app.include_router(home_router)
    app.include_router(orders_router)
    app.include_router(routes_router)
    app.include_router(optimization_router)

    return app


app = create_app()
