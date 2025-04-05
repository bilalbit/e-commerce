import uvicorn
from fastapi import FastAPI

app = FastAPI()



@app.get("/healthy")
def healthy():
    return {"status": "OK"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=7000, reload=True)