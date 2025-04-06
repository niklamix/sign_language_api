from fastapi import APIRouter

router = APIRouter(prefix="/predict", tags=["predictions"])

@router.get("/")
async def read_root():
    return {"message": "Predict sign result"}