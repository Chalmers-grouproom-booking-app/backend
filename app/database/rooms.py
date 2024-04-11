from database.pb import client

def get_room_info(room_name):
    filter = f"room_name='{room_name}'"
    room_record = client.collection('grouprooms').get_list(
        1, 1,  {'filter': filter}
    )
    return room_record
