from fastapi import FastAPI
import models
from database import engine
from routers import reports, timeline

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(reports.router)
app.include_router(timeline.router)

@app.get('/')
def root():
    return {"Hello": "World"}