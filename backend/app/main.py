from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.endpoints import predict_sign
import uvicorn

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(predict_sign.router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
