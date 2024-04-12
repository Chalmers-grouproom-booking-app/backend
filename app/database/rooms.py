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
    

def get_room_building(room: str) -> str:
    filter = f"room_name = {room}"
    room_record = client.collection('grouprooms').get_list(
        1, 1,  {'filter': filter}
    )
    return room_record.items[0].building

def show_room_reservations(room_name: str):
    filter = f"room_name = {room_name}"
    room_record = client.collection('grouprooms').get_list(1, 1, {'filter': filter})
    room = room_record.items[0].id
    new_filter = f"room.room_name={room_name}"
    #reservations_record = client.collection('reservations').get_list(1, 1, {filter: cool})
    try:
        reservation_record =  client.collection('reservations').get_list(1, 1, {'filter': new_filter})
    except:
        return "Very bad."


    reserved_times = {}
    for res in reservation_record.items:
        if(res.room == room):
            reserved_times.update({"start-time": res.starttime})
            reserved_times.update({"end-time": res.endtime})

    return reserved_times
