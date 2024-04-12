from database.pb import client
import json

def get_room_info(room_name):
    try:
        thisfilter = f"room_name='{room_name}'"
        room_record = client.collection('grouprooms').get_list(1, 1,  {'filter': thisfilter})
        room_info = {
                "Room Name": room_name,
                "Room Size": f"{get_room_size(room_record)} square meters",
                "Building": get_building(room_record),
                "Campus": get_campus(room_record),
                "Equipment": get_equipment(room_record)
            }
        if not room_info["Equipment"]:
            equipment = "There is no Equipments"
        else:
            equipment = room_info["Equipment"]
            
        return {"Room Name": room_name,"Room Size":f"{get_room_size(room_record)} square meters","Building": get_building(room_record),"Campus": get_campus(room_record),"Equipment": equipment}
    except:
        return "This Room Does not exist"
def get_room_size(room_record):
    return room_record.items[0].room_size

def get_building(room_record):
    return room_record.items[0].building

def get_campus(room_record):
    return room_record.items[0].campus

def get_equipment(room_record):
    return room_record.items[0].equipment
