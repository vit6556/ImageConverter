from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

from common import Base
from common.database.session import get_database_engine
from api.images.router import images_router


app = FastAPI()
app.include_router(images_router)
templates = Jinja2Templates(directory="api/templates")

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.on_event("startup")
def create_tables():
	Base.metadata.create_all(bind=get_database_engine())