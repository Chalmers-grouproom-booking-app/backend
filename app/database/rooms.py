from typing import List
from models.response import ReservationModel, RoomModel, SearchModel
from database.queries import RoomQuery
from datetime import datetime
import re

def get_room_info(room_name) -> RoomModel:
    return convert_room_to_dict( RoomQuery(room_name).get_room() )

def get_all_rooms():
    all_rooms = RoomQuery.get_all_rooms()
    return format_all_rooms(  all_rooms )

def format_all_rooms( room_records: list ) -> list[RoomModel]:
    return [ convert_room_to_dict(room) for room in room_records ]

def convert_room_to_dict( room ) -> RoomModel:
    return {
        "room_name": room.room_name,
        "room_size": room.room_size if (room.room_size != None) else "",
        "building": room.building,
        "campus": room.campus,
        "equipment": room.equipment if (room.equipment != None) else "",
        "longitude": room.longitude,
        "latitude": room.latitude,
        "entrance_latitude": room.entrance_latitude,
        "entrance_longitude": room.entrance_longitude,
        "description": room.description,
        "first_come_first_served": room.first_come_first_served,
        "floor_level": room.floor_level if (room.floor_level != None) else "",
        "stair": room.stair if (room.stair != None) else "",
    }

def room_format(room_record: dict) -> SearchModel:
    fields = {}
    rooms = []
    keys = room_record.keys()
    for key in keys:
        fields[key] = room_record[key]
        for item in room_record[key]:  
            room = convert_room_to_dict(item)
            rooms.append(room) 
        fields[key] = rooms
        rooms = []
    return fields
    

def show_room_reservations(room_name: str) -> List[ReservationModel]:
    reservations = RoomQuery(room_name).get_reservations()
    reserved_times = []

    current_date = datetime.today().date()
    for res in reservations:
        reserved_date = datetime.strptime(re.sub("-", "/", re.sub(" 00:00:00.000", "",res.startdate)), "%Y/%m/%d").date()
        if reserved_date < current_date:
            continue
        reservation = {
            "start_date": re.sub("-", "/", re.sub(" 00:00:00.000", "",res.startdate)),
            "start_time": res.starttime,
            "end_time": res.endtime,
            "end_date": re.sub("-", "/", re.sub(" 00:00:00.000", "",res.enddate))
        }
        reserved_times.append(ReservationModel(**reservation))        
    return reserved_times

def show_all_reservations(room_name: str) -> List[ReservationModel]:
    reservations = RoomQuery(room_name).get_reservations()
    reserved_times = []
    for res in reservations:
        reservation = {
            "start_date": re.sub("-", "/", re.sub(" 00:00:00.000", "",res.startdate)),
            "start_time": res.starttime,
            "end_time": res.endtime,
            "end_date": re.sub("-", "/", re.sub(" 00:00:00.000", "",res.enddate))
        }
        reserved_times.append(ReservationModel(**reservation))
    return reserved_times