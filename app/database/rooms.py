from database.pb import client

def get_room_info(room_name):
    filter = f"room_name='{room_name}"
    room_record = client.collection('grouprooms').get_list(
        1, 1,  {'filter': filter}
    )
    return room_record

def get_room_building(room: str) -> str:
    filter = f"room_name = {room}"
    room_record = client.collection('grouprooms').get_list(
        1, 1,  {'filter': filter}
    )
    return room_record.items[0].building

def show_room_reservations(room_name: str):
    filter = f"room_name = {room_name}"
    room_record = client.collection('grouprooms').get_list(1, 1, {'filter': filter})
    room = room_record.items[0].room_id
    filter = f"room_id = {room}"
    reservations_record = client.collection('reservations').get_list(1,1, {'filter': filter})

    reserved_times = {}
    for res in reservations_record:
        if(res.room == room):
            reserved_times.append({res.starttime: res.endtime})
    return reservations_record.items[0].starttime