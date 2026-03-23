from fastapi import Request
from fastapi.templating import Jinja2Templates

from .services.optimization import OptimizationService
from .services.orders import OrdersService
from .services.routes import RoutesService


def get_templates(request: Request) -> Jinja2Templates:
    return request.app.state.templates


def get_orders_service(request: Request) -> OrdersService:
    return request.app.state.orders_service


def get_routes_service(request: Request) -> RoutesService:
    return request.app.state.routes_service


def get_optimization_service(request: Request) -> OptimizationService:
    return request.app.state.optimization_service
