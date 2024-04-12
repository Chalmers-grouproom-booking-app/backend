from typing import Optional
from fastapi import APIRouter, Query
from models.test_model import TestModel
from database.pb import client
from database.rooms import get_room_info
from database.filter import *

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
def search_db(search_input, room_size : str = Query(""), building : str = Query(""), campus : str = Query(""), equipment : str = Query(""), room_name : str = Query(""), first_come_first_served : str = Query(""), floor_level : str = Query("")):
    keys = ['room_size', 'building', 'campus', 'equipment', 'room_name', 'first_come_first_served', 'floor_level']
    list_of_filters = [room_size, building, campus, equipment, room_name, first_come_first_served, floor_level]
    list_of_filters = dict(zip(keys, list_of_filters))
    return search_filter(search_input, list_of_filters)
    