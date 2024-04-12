from fastapi import APIRouter
from models.test_model import TestModel
from database.rooms import get_room_building

router = APIRouter(
    prefix="/api/v1",
)
@router.get("/ping", tags=["Test the server"])
def ping() -> TestModel:
    return {"message": "pong"}

@router.get("/room/building/{room_name}", tags=["Get building"])
def get_building(room_name: str):
    return {"building": get_room_building(room_name)}