from fastapi import APIRouter
from models.test_model import TestModel
import database.building as building

router = APIRouter(
    prefix="/api/v1",
)
@router.get("/ping", tags=["Test the server"])
def ping() -> TestModel:
    return {"message": "pong"}

@router.get("/building", tags=["BUILDING"])
def get_building() -> TestModel:
    return {"message": building.get_building("Vasa")}