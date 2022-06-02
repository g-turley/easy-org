from fastapi import FastAPI, Request, Form, APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import starlette.status as status
from ..library.helpers import *
import subprocess

router = APIRouter()
templates = Jinja2Templates(directory="templates/")

# Org Templating
@router.post("/org/new", response_class=HTMLResponse)
async def orgfile(request: Request, form_type: str = "task"):
    form = await request.form()
    response = org_protocol(form_type, *create_org_template(form_type, form))
    return RedirectResponse(url=f'/files?response={response}', status_code=status.HTTP_302_FOUND)

# Read org file.
@router.get("/org/{file}", response_class=HTMLResponse)
async def orgfile(request: Request, file: str, path: str, export: str = ""):
    if export == "html":
        evaluate = subprocess.check_output(f'echo "$PWD"')#emacsclient -e "(progn (find-file \"{os.path.join(path, file)}\") (org-html-export-to-html) (kill-buffer))"', shell=True).decode('utf-8')
    data = readorg(os.path.join(path, file))
    return templates.TemplateResponse("org.html", {"request": request, "data": data})