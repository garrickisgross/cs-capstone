from typing import Annotated

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from ..dependencies import get_orders_service, get_templates
from ..schemas.orders import CreateOrderInput
from ..services.orders import OrdersService

router = APIRouter()


@router.get("/orders", response_class=HTMLResponse)
async def orders(
    request: Request,
    templates: Jinja2Templates = Depends(get_templates),
    service: OrdersService = Depends(get_orders_service),
):
    page_data = service.build_orders_page()
    return templates.TemplateResponse(
        request=request,
        name="orders.html",
        context={"data": page_data},
    )


@router.post("/create_order", response_class=HTMLResponse)
async def create_order(
    address: Annotated[str, Form(...)],
    city: Annotated[str, Form(...)],
    st: Annotated[str, Form(...)],
    request: Request,
    description: Annotated[str | None, Form()] = None,
    templates: Jinja2Templates = Depends(get_templates),
    service: OrdersService = Depends(get_orders_service),
) -> HTMLResponse:
    result = service.create_order(
        CreateOrderInput(
            address=address,
            city=city,
            st=st,
            description=description,
        )
    )
    return templates.TemplateResponse(
        request=request,
        name="partials/order_created.html",
        context={"data": result},
    )
