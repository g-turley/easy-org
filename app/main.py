<<<<<<< Updated upstream
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .library.helpers import *
from app.routers import twoforms, unsplash, accordion

app = FastAPI()


templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(unsplash.router)
app.include_router(twoforms.router)
app.include_router(accordion.router)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    data = openfile("home.md")
    return templates.TemplateResponse("page.html", {"request": request, "data": data})

@app.get("/files", response_class=HTMLResponse)
async def orgpath(request: Request, path: str = "\\", response: str = ""):
    data = listorg(path)
    return templates.TemplateResponse("files.html", {"request": request, "data": data, "response": response})
# Capture templates
@app.get("/capture/new", response_class=HTMLResponse)
async def orgfile(request: Request):
    data = {}
    return templates.TemplateResponse("capture.html", {"request": request, "data": data})

# Org Editing
@app.get("/org/new", response_class=HTMLResponse)
async def orgfile(request: Request, content: str):
    response = org_protocol(request, content)
    response = RedirectResponse(url=f'/files?response={response}')
    return response
    # return templates.TemplateResponse("files.html", {"request": request, "data": data})

@app.get("/org", response_class=HTMLResponse)
async def orgfile(request: Request, file: str, path: str):
    data = listorg(os.path.join(path, file))
    return templates.TemplateResponse("files.html", {"request": request, "data": data})

@app.get("/org/{file}", response_class=HTMLResponse)
async def orgfile(request: Request, file: str, path: str):
    data = readorg(os.path.join(path, file))
    return templates.TemplateResponse("org.html", {"request": request, "data": data})

# Non-org viewing
@app.get("/page/{page_name}", response_class=HTMLResponse)
async def show_page(request: Request, page_name: str):
    data = openfile(page_name+".md")
    return templates.TemplateResponse("page.html", {"request": request, "data": data})
=======
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .library.helpers import *
from app.routers import twoforms, unsplash, accordion

app = FastAPI()


templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(unsplash.router)
app.include_router(twoforms.router)
app.include_router(accordion.router)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    data = openfile("home.md")
    return templates.TemplateResponse("page.html", {"request": request, "data": data})

@app.get("/files", response_class=HTMLResponse)
async def orgpath(request: Request, path: str = "\\", response: str = ""):
    data = listorg(path)
    return templates.TemplateResponse("files.html", {"request": request, "data": data, "response": response})
# Capture templates
@app.get("/capture/new", response_class=HTMLResponse)
async def orgfile(request: Request):
    data = {}
    return templates.TemplateResponse("capture.html", {"request": request, "data": data})

# Org Editing
@app.get("/org/new", response_class=HTMLResponse)
async def orgfile(request: Request, content: str):
    response = org_protocol(request, content)
    response = RedirectResponse(url='/org/tasks.org?response={response}&path=\\')
    # response = RedirectResponse(url=f'/files?response={response}')
    return response
    # return templates.TemplateResponse("files.html", {"request": request, "data": data})

@app.get("/org", response_class=HTMLResponse)
async def orgfile(request: Request, file: str, path: str):
    data = listorg(os.path.join(path, file))
    return templates.TemplateResponse("files.html", {"request": request, "data": data})

@app.get("/org/{file}", response_class=HTMLResponse)
async def orgfile(request: Request, file: str, path: str):
    data = readorg(os.path.join(path, file))
    return templates.TemplateResponse("org.html", {"request": request, "data": data})

# Non-org viewing
@app.get("/page/{page_name}", response_class=HTMLResponse)
async def show_page(request: Request, page_name: str):
    data = openfile(page_name+".md")
    return templates.TemplateResponse("page.html", {"request": request, "data": data})
>>>>>>> Stashed changes
