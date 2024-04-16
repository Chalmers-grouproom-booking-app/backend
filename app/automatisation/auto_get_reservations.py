from automatisation.timeedit_api import TimeEditAPI
from database.pb import client
import json
from datetime import datetime, timedelta
import requests

# Initialize TimeEdit API & and room cache
room_cache = {}


def parse_rooms(data):
    # Extract the string of rooms (assuming it's always in the first index)
    room_string = data['columns'][0]
    # Split the string by commas to get individual room names
    room_list = room_string.split(', ')
    return room_list

def fetch_group_room_id(room_name):
    """
    Fetch the group room ID by room name. Cache the results to minimize API calls.
    """
    # Assume we have cached room IDs in a dictionary
    if room_name not in room_cache:
        rooms = client.collection("grouprooms").get_list(1, 1, { "filter": f'room_name="{room_name}"' })
        if rooms.items:
            room_cache[room_name] = rooms.items[0].id
        else:
            room_cache[room_name] = None
    return room_cache[room_name]

def fetch_reservations():
    timeedit = TimeEditAPI()
    
    reservations = timeedit.get_reservations( from_date= datetime.now(), to_date= datetime.now() + timedelta(days=14))
    for reservation in reservations["reservations"]:
        all_room_names = parse_rooms(reservation)
        if not all_room_names:
            print(f"No room names found for reservation {reservation['id']}")
            continue
        
        for room_name in all_room_names:
            group_room_id = fetch_group_room_id(room_name)
            print(group_room_id)
            
            if not group_room_id:
                print(f"Room {room_name} not found.")
                continue
            
            # Prepare data for update or create
            reservation_data = {
                "room": group_room_id,
                "reservation_id": reservation["id"],
                "startdate": reservation["startdate"],
                "starttime": reservation["starttime"],
                "endtime": reservation["endtime"],
                "enddate": reservation["enddate"]
            }            
            # Check if the reservation already exists
            existing_reservation = client.collection("reservations").get_list(1, 1, { "filter": f'reservation_id={reservation["id"]}' })
            if existing_reservation.total_items > 0:
                # check if the reservation is different
                if existing_reservation.items[0].starttime == reservation_data["starttime"] and existing_reservation.items[0].endtime == reservation_data["endtime"]:
                    continue
                url = f"https://pb.sacic.dev/api/collections/reservations/records/{existing_reservation.items[0].id}"
                headers = {
                    "Content-Type": "application/json"
                }
                response = requests.patch(url, json=json.dumps(reservation_data), headers=headers)
                print(response.status_code)
                print(f"Updated reservation {reservation['id']} linked to room {room_name}")
            else:
                new_reservation = client.collection("reservations").create(reservation_data)
                print(f"Created new reservation {reservation['id']} linked to room {room_name} with ID {new_reservation.id}")