from fastapi import FastAPI, Request, Form, APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import starlette.status as status
from ..library.helpers import *

router = APIRouter()
templates = Jinja2Templates(directory="templates/")

# Org Editing
@router.post("/org/new", response_class=HTMLResponse)
async def orgfile(request: Request, form_type: str = "task"):
    form = await request.form()
    response = org_protocol(form_type, *create_org_template(form_type, form))
    return RedirectResponse(url=f'/files?response={response}', status_code=status.HTTP_302_FOUND)

@router.get("/org", response_class=HTMLResponse)
async def orgfile(request: Request, file: str, path: str):
    data = listorg(os.path.join(path, file))
    return templates.TemplateResponse("files.html", {"request": request, "data": data})

@router.get("/org/{file}", response_class=HTMLResponse)
async def orgfile(request: Request, file: str, path: str):
    data = readorg(os.path.join(path, file))
    return templates.TemplateResponse("org.html", {"request": request, "data": data})