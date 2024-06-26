from typing import List
from models.response import ReservationModel, RoomModel, SearchModel
from database.queries.room_query import RoomQuery
from database.queries.building_query import BuildingQuery
from datetime import datetime
from datetime import timedelta
import re

def get_room_info(room_name) -> RoomModel:
    return convert_room_to_dict( RoomQuery(room_name).get_room() )

def get_all_rooms():
    all_rooms = RoomQuery.get_all_rooms()
    return format_all_rooms(  all_rooms )

def format_all_rooms( room_records: list ) -> List[RoomModel]:
    return [ convert_room_to_dict(room) for room in room_records ]

def get_room_id(room_name: str) -> int:
    try:
        room_id = RoomQuery(room_name).get_room_id()
        return room_id
    except Exception as e:
        return None

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


def is_room_booked(room_name: str, interval_forward_hours: float) -> bool:
    reservations = show_room_reservations(room_name)

    # If no reservations return False
    if (len(reservations) <= 0):
        return False
    
    for res in reservations:
        if (__compare_reservation_times(res, interval_forward_hours)):
            return True
    return False
    
    
def __compare_reservation_times(reservation, interval_forward_hours):
    # If the start date of reservation is not today return False
    reserved_date = datetime.strptime(re.sub("-", "/", re.sub(" 00:00:00.000", "",reservation.start_date)), "%Y/%m/%d").date()
    if(reserved_date != datetime.today().date()):
        return False
    
    # Get current time and start time of reservation + start time with interval
    start_time = datetime.strptime(reservation.start_time, "%H:%M").time().strftime("%H:%M")
    end_time = datetime.strptime(reservation.end_time, "%H:%M").time().strftime("%H:%M")
    current_time_interval = (datetime.now() + timedelta(hours=interval_forward_hours)).time().strftime("%H:%M")
    current_time = datetime.now().time().strftime("%H:%M")

    start_ahead          =  current_time > start_time           # We have passed the start time      --C---S--------E--
    end_behind           =  current_time < end_time             # The booking has not finished       --S---C--------E--
    interval_start_ahead =  current_time_interval > start_time  # Room is not booked within interval --C---I--S-----E--
    interval_end_behind  =  current_time_interval < end_time    # Room is booked within interval     --C-----S--I---E--

    # If the booked time lies within [now, now + interval_hours] return True
    if ((start_ahead and end_behind) or (interval_start_ahead and interval_end_behind)):
        return True
    return False


def get_building_booked_percentage(building_name: str, interval_forward_hours: float) -> float:
    if(not _building_contains_rooms):
        return -1
    
    # Get all rooms of a building
    rooms = BuildingQuery(building_name).get_all_rooms_in_building()

    # reservations
    reservations = BuildingQuery(building_name).get_building_reservations(interval_forward_hours)

    # Filter out first come first serve rooms
    all_rooms: int = len(rooms)
    booked_rooms: int = len(reservations)

    percentage: float = booked_rooms / all_rooms
    return percentage

def get_all_buildings_booked_percentage(interval_forward_hours: float) -> List[SearchModel]:

    building_records = {
        "Kårhuset": -1,
        "Fysik": -1,
        "Kemi": -1, 
        "M-huset": -1, 
        "Biblioteket": -1,
        "Vasa Hus 1": -1,
        "Svea": -1,
        "Jupiter": -1,
        "Kuggen": -1
    }
    
    for key in building_records:
        building_records[key] = get_building_booked_percentage(key, interval_forward_hours)
            
    return building_records


    

def _building_contains_rooms(building_name) -> bool:
    rooms = BuildingQuery(building_name).get_all_rooms_in_building()
    if(len(rooms) != 0):
        return True
    return False
