from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from api.images.router import images_router


app = FastAPI()
app.include_router(images_router)
templates = Jinja2Templates(directory="api/templates")

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})