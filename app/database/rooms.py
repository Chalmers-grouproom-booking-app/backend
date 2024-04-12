from database.pb import client

def get_room_info(room_name):
    thisfilter = f"room_name='{room_name}"
    room_record = client.collection('grouprooms').get_list(
        1, 1,  {'filter': thisfilter}
    )
    return room_record
