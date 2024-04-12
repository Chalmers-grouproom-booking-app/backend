from database.pb import client
import json

def get_room_info(room_name):
    # try:
    thisfilter = f"room_name='{room_name}'"
    room_record = client.collection('grouprooms').get_list(1, 1,  {'filter': thisfilter})
    return room_format(room_record)
    
def room_format(room_record):
    rooms = []
    for item in room_record.items:
        
        room = {
            "Room Name": item.room_name,
            "Room Size": item.room_size,
            "Building": item.building,
            "Campus": item.campus,
            "Equipment": item.equipment,
            "Longitude": item.longitude,
            "Latitude": item.latitude,
            "Entrance latitude": item.entrance_latitude,
            "Entrance longitude": item.entrance_longitude,
            "Description": item.description,
            "First come first served": item.first_come_first_served,
            "Floor Level": item.floor_level,
            "stair": item.stair
        }
        
        equipment = room.get("Equipment", "")
        room_size = room.get("Room Size", "")
        floor_level = room.get("Floor Level", "")
        stair = room.get("stair", "")
            
        rooms.append({
            "Room Name": item.room_name,
            "Room Size": room_size ,
            "Building": item.building,
            "Campus": item.campus,
            "Equipment": equipment,
            "Longitude": item.longitude,
            "Latitude": item.latitude,
            "Entrance Latitude": item.entrance_latitude,
            "Entrance Longitude": item.entrance_longitude,
            "Description": item.description,
            "First Come First Served": item.first_come_first_served,
            "Floor Level": floor_level,
            "Stairs": stair
        })

    return rooms
    
