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
            "Equipment": item.equipment
        }
        if not room["Equipment"]:
            equipment = "There is no Equipments"
        else:
            equipment = room["Equipment"]
            
        rooms.append({"Room Name": item.room_name,"Room Size":f"{item.room_size} square meters","Building": item.building,"Campus": item.campus,"Equipment": equipment})
    return rooms
    
