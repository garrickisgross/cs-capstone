from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from ..dependencies import get_templates

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def home(
    request: Request,
    templates: Jinja2Templates = Depends(get_templates),
):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
    )
