from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import starlette.status as status
from .library.helpers import *
from app.routers import org

app = FastAPI()


templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(org.router)

# Home
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return RedirectResponse(url=f'/files', status_code=status.HTTP_302_FOUND)
    # data = openfile("home.md")
    # return templates.TemplateResponse("page.html", {"request": request, "data": data})

# Files
@app.get("/files", response_class=HTMLResponse)
async def orgpath(request: Request, path: str = "\\", response: str = ""):
    # These generate the html forms for the modals.
    create_org_form('task')
    create_org_form('project')
    create_org_form('target')
    data = listorg(path)
    return templates.TemplateResponse("files.html", {"request": request, "data": data, "response": response})

# Capture templates
@app.get("/capture/new", response_class=HTMLResponse)
async def orgfile(request: Request):
    data = {}
    return templates.TemplateResponse("capture.html", {"request": request, "data": data})

# Non-org viewing
@app.get("/page/{page_name}", response_class=HTMLResponse)
async def show_page(request: Request, page_name: str):
    data = openfile(page_name+".md")
    return templates.TemplateResponse("page.html", {"request": request, "data": data})