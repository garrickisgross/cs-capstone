from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .db.in_memory import InMemoryStorage
from .routers.optimization import router as optimization_router
from .routers.orders import router as orders_router
from .services.geocoding import NominatimGeocoder
from .services.optimization import OptimizationService
from .services.orders import OrdersService

APP_DIR = Path(__file__).resolve().parent
STATIC_DIR = APP_DIR / "static"
TEMPLATES_DIR = APP_DIR / "templates"


def create_app() -> FastAPI:
    app = FastAPI()

    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
    app.state.templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

    storage = InMemoryStorage()
    geocoder = NominatimGeocoder()
    app.state.storage = storage
    app.state.orders_service = OrdersService(storage, geocoder)
    app.state.optimization_service = OptimizationService(storage)

    app.include_router(orders_router)
    app.include_router(optimization_router)

    return app


app = create_app()
