from fastapi import FastAPI
from app.routers import router
from app.database import init_db

app = FastAPI()

# create tables when app starts
@app.on_event('startup')
def on_startup():
    init_db()

app.include_router(router)