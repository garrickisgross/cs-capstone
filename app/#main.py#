from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


app = FastAPI()

# mount static directories.
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# we will be using jinja templates, teaming up with htmx.
templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
        )

@app.get("/locations", response_class=HTMLResponse)
async def locations(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="locations.html"
        )

@app.get("/orders", response_class=HTMLResponse)
async def orders(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="orders.html"
        )

@app.get("/routes", response_class=HTMLResponse)
async def routes(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="routes.html"
        )

@app.get("/optimize", response_class=HTMLResponse)
async def optimize(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="optimize.html",
        )
