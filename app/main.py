import uvicorn
from fastapi import FastAPI

from app.core.config import setting_dep

app = FastAPI()



@app.get("/healthy")
def healthy():
    return {"status": "OK"}

@app.get("/info")
def info(settings: setting_dep):
    return settings

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=7000, reload=True)