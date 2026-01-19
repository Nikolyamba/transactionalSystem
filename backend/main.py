import uvicorn
from fastapi import FastAPI

from backend.api.pay import pay_router

app = FastAPI()

app.include_router(o_router)
app.include_router(pay_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000)