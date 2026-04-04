from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from ..dependencies import get_optimization_service, get_templates
from ..services.optimization import OptimizationService

router = APIRouter()


@router.get("/optimize", response_class=HTMLResponse)
async def optimize(
    request: Request,
    templates: Jinja2Templates = Depends(get_templates),
    service: OptimizationService = Depends(get_optimization_service),
):
    page_data = service.build_optimize_page()
    return templates.TemplateResponse(
        request=request,
        name="optimize.html",
        context={"data": page_data},
    )


@router.post("/optimize/orders", response_class=HTMLResponse)
async def optimize_orders(
    request: Request,
    templates: Jinja2Templates = Depends(get_templates),
    service: OptimizationService = Depends(get_optimization_service),
):
    orders_list = service.build_optimized_orders_list()
    return templates.TemplateResponse(
        request=request,
        name="partials/optimization_orders.html",
        context={"data": orders_list},
    )
