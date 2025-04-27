import uvicorn
from fastapi import FastAPI

from backend.app.core.config import setting_dep
from backend.app.database import create_db_and_tables
from backend.app.modules.api_routes import api_routes

app = FastAPI()

app.include_router(api_routes)



@app.get("/healthy")
def healthy():
    return {"status": "OK"}

@app.get("/info")
def info(settings: setting_dep):
    return settings
@app.get("/db-init")
def db_init():
    create_db_and_tables()
    return "success"

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=7000, reload=True)