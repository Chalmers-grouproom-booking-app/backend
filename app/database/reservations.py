from models.response import RoomModelV2
from database.pb import client
from enum import Enum
import datetime

class RoomStatus(Enum):
    AVAILABLE = "available"
    OCCUPIED = "occupied"
    SOON_OCCUPIED = "soon_occupied" # Room will be occupied in the next 30 minutes

def check_room_status(room_id, now, in_30_minutes, reservations):
    status = RoomStatus.AVAILABLE
    smallest_time_diff = float('inf')

    for reservation in reservations:
        if reservation.room != room_id:
            continue

        start_time_str = f"{now.strftime('%Y-%m-%d')} {reservation.starttime}"
        end_time_str = f"{now.strftime('%Y-%m-%d')} {reservation.endtime}"
        start_time = datetime.datetime.strptime(start_time_str, '%Y-%m-%d %H:%M')
        end_time = datetime.datetime.strptime(end_time_str, '%Y-%m-%d %H:%M')

        if start_time <= now <= end_time:
            status = RoomStatus.OCCUPIED
            time_diff = (end_time - now).total_seconds()
            smallest_time_diff = min(smallest_time_diff, time_diff)
            break  # No need to check further if the room is already occupied
        elif now <= start_time <= in_30_minutes:
            time_diff = (start_time - now).total_seconds()
            if time_diff < smallest_time_diff:
                smallest_time_diff = time_diff
                if status != RoomStatus.OCCUPIED:
                    status = RoomStatus.SOON_OCCUPIED

    if smallest_time_diff == float('inf'):
        smallest_time_diff = 0  # Reset if no reservations affect the status within the timeframe

    return status.value, int(smallest_time_diff)


def convert_room_to_dict( room , status, time_diff) -> RoomModelV2:
    data = {
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
        "status": status,
        "time_left": time_diff
    }
    return RoomModelV2(**data)
    
def update_room_statuses(data, status_filter: RoomStatus = None):
    reservations = get_current_reservations()

    now = datetime.datetime.now()
    in_30_minutes = (now + datetime.timedelta(minutes=30)) 
    fields = {}
    keys = data.keys()
    for key in keys:
        rooms = []
        for room in data[key]:
            room_id = room.id
            status, time_diff = check_room_status(room_id, now, in_30_minutes, reservations)
            if (status_filter != None and status != status_filter.value):
                continue
            room = convert_room_to_dict(room, status, time_diff)
            rooms.append(room)
    
        fields[key] = rooms
    return fields

def get_current_reservations():
    now = datetime.datetime.now()
    now_today = now.strftime('%Y-%m-%d')
    now_hour = now.strftime('%H:%M')
    in_30_minutes = (now + datetime.timedelta(minutes=30)).strftime('%H:%M')
    reservations = client.collection('reservations').get_full_list(
        400,
        {'filter': f'(startdate~"{now_today}" && endtime>"{now_hour}" && starttime<"{now_hour}") || (startdate~"{now_today}" && starttime>="{now_hour}" && starttime<="{in_30_minutes}")'}
    )
    return reservations