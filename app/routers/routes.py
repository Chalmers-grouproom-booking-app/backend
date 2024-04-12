from typing import Optional
from fastapi import APIRouter, Query
from models.test_model import TestModel
from database.pb import client
from database.rooms import get_room_info
from database.filter import *
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

@router.get("/search/{search_input}", tags=["Get room info"])
def search_db(search_input, room_size : str = Query(""), building : str = Query(""), campus : str = Query(""), equipment : str = Query(""), room_name : str = Query("")):
    keys = ['room_size', 'building', 'campus', 'equipment', 'room_name']
    list_of_filters = [room_size, building, campus, equipment, room_name]
    list_of_filters = dict(zip(keys, list_of_filters))
    return search_filter(search_input, list_of_filters)
    

@router.get("/room/reservation/{room_name}", tags=["Get reservation"])
def get_reservation(room_name: str):
    return show_room_reservations(room_name)

