import uvicorn
from fastapi import FastAPI, Request

from app.core.config import setting_dep
from app.core.routes import api_router
from app.database import create_db_and_tables

from app.modules.auth.services import current_user_context

app = FastAPI()

app.include_router(api_router)

###middleware
@app.middleware("http")
async def reset_context_middleware(request: Request, call_next):
    response = await call_next(request)
    # Reset only if it was set (optional optimization)
    if current_user_context.get() is not None:
        current_user_context.set(None)
    return response

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