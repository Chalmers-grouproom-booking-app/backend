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
    room = room_record.items[0].id
    new_filter = f"room={room}"
    #reservations_record = client.collection('reservations').get_list(1, 1, {filter: cool})
    try:
       # aspdl =  client.collection('reservations').get_list(1, 1, {'filter': room})
        #resultList =  client.records.getList('reservations', 1, 50, {'filter': new_filter})
        1+1
    except:
        return "Very bad."


    #reserved_times = {}
    #for res in reservations_record.items:
    #    if(res.room == room):
    #       reserved_times.update({"start-time": res.starttime})
    #        reserved_times.update({"end-time": res.endtime})

    return room_record.items[0]
