from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from ..dependencies import get_routes_service, get_templates
from ..services.routes import RoutesService

router = APIRouter()


@router.get("/routes", response_class=HTMLResponse)
async def routes(
    request: Request,
    templates: Jinja2Templates = Depends(get_templates),
    service: RoutesService = Depends(get_routes_service),
):
    page_data = service.build_routes_page()
    return templates.TemplateResponse(
        request=request,
        name="routes.html",
        context={"data": page_data.data},
    )
