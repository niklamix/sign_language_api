from fastapi import FastAPI
from api.endpoints import predict_sign
import uvicorn

app = FastAPI()

app.include_router(predict_sign.router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
