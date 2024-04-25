from typing import List
from models.response import ReservationModel, RoomModel, SearchModel
from database.queries import RoomQuery, BuildingQuery
from datetime import datetime
from datetime import timedelta
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


def is_room_booked(room_name: str) -> bool:
    reservations = show_room_reservations(room_name)

    # If no reservations return False
    if (len(reservations) <= 0):
        return False
    
    for res in reservations:
        if (compare_reservation_times(res) == True):
            return True
    return False
    
    
def compare_reservation_times(reservation):
    # The time-interval to be checked
    INTERVAL: int = 0

    # If the start date of reservation is not today return False
    reserved_date = datetime.strptime(re.sub("-", "/", re.sub(" 00:00:00.000", "",reservation.start_date)), "%Y/%m/%d").date()
    if(reserved_date != datetime.today().date()):
        return False
    
    # Get current time and start time of reservation + start time with interval
    start_time = datetime.strptime(reservation.start_time, "%H:%M").time().strftime("%H:%M")
    end_time = datetime.strptime(reservation.end_time, "%H:%M").time().strftime("%H:%M")
    current_time_interval = (datetime.now() + timedelta(hours=INTERVAL)).time().strftime("%H:%M")
    current_time = datetime.now().time().strftime("%H:%M")

    start_ahead          =  current_time > start_time           # We have passed the start time      --C---S--------E--
    end_behind           =  current_time < end_time             # The booking has not finished       --S---C--------E--
    interval_start_ahead =  current_time_interval > start_time  # Room is not booked within interval --C---I--S-----E--
    interval_end_behind  =  current_time_interval < end_time    # Room is booked within interval     --C-----S--I---E--

    # If the booked time lies within [now, now+2h] return True
    if ((start_ahead and end_behind) or (interval_start_ahead and interval_end_behind)):
        return True
    return False


def __booked_percentage(building_name: str) -> float:
    # Get all rooms of a building
    rooms = BuildingQuery(building_name).get_all_rooms_in_building()
    
    # Filter out first come first serve rooms
    filtered_rooms: int = 0
    booked_rooms: int = 0
    
    for r in rooms:
        if(not r.first_come_first_served):
            filtered_rooms += 1
            if(is_room_booked(r.room_name)):
                booked_rooms += 1
    # Loop over all rooms in a building
    percentage: float = booked_rooms / max(filtered_rooms, 1)
    return percentage

def calculate_rgb_color(building_name : str):
    inverted_percentage = 1 - __booked_percentage(building_name)
    return [int(255 * inverted_percentage), int(255 * inverted_percentage), int(255 * inverted_percentage)]