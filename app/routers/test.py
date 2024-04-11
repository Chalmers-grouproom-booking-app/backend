from fastapi import APIRouter
from models.test_model import TestModel

router = APIRouter(
    prefix="/api/v1",
)
@router.get("/ping", tags=["Test the server"])
async def ping() -> TestModel:
    return {"message": "pong"}