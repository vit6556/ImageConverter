from fastapi import FastAPI

from common import Base
from common.database.session import get_database_engine
from api.images.router import images_router


app = FastAPI()
app.include_router(images_router)

@app.on_event("startup")
def create_tables():
	Base.metadata.create_all(bind=get_database_engine())