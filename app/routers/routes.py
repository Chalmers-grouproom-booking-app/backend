from fastapi import APIRouter
from models.test_model import TestModel
from database.pb import client
from database.rooms import get_room_info
from database.rooms import show_room_reservations

router = APIRouter(
    prefix="/api/v1",
)

@router.get("/test", tags=["Test the server"])
def test():
    return client.collection('grouprooms').get_full_list()

@router.get("/ping", tags=["Test the server"])
def ping() -> TestModel:
    return {"message": "pong"}

@router.get("/room/{room_name}", tags=["Get room info"])
def get_room_info_route(room_name: str):
    return get_room_info(room_name)

@router.get("/room/{room_name}/reservation", tags=["Get reservation"])
def get_reservation(room_name: str):
    return {room_name: show_room_reservations(room_name)}

