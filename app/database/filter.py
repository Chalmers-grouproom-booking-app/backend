from exceptions.exceptions import RoomsNotFoundException
from models.response import RoomModel, RoomDetails
from database.pb import client
from database.rooms import room_format
from database.reservations import get_current_reservations, update_room_statuses
UNWANTED_FIELDS = ['expand', 'collection_id', 'collection_name', 'id', 'room_id', 'created', 'updated', 'longitude', 'latitude','entrance_longitude', 'entrance_latitude', 'description', 'stair']

def get_fields(records):
    if records.items:
        item = records.items[0]
        fields = list(vars(item).keys())
    return fields

def search(search_result : str):
    results = {}
    for field in RoomModel.__fields__.keys():
        if field not in UNWANTED_FIELDS:
            result = client.collection('grouprooms').get_list(query_params={'filter': f'{field}~"{search_result}"'})
            if result.items:
                results.update({field : result.items})
    return results


def search_filter(search_result : str, filter : dict = {}):
    data = {}
    filter_result = filter_results(filter)
    empty_counter = 1
    total_fields = len(RoomDetails.__fields__.keys()) - len(UNWANTED_FIELDS)
    for field in RoomModel.__fields__.keys():
        if field not in UNWANTED_FIELDS:
            records = client.collection('grouprooms').get_list(query_params={'filter': f'{field}~"{search_result}"' + filter_result})
            if len(records.items) == 0:
                empty_counter += 1
            data.update({field : records.items})
    if empty_counter == total_fields:
        raise RoomsNotFoundException(f"No rooms found with the search term '{search_result}'")
    print(empty_counter)
    print(total_fields)
    formatted_data = room_format(data)
    return formatted_data


def search_filter_V2(search_result : str, filter : dict = {}):
    data = {}
    filter_result = filter_results(filter)
    empty_counter = 1
    total_fields = len(RoomDetails.__fields__.keys()) - len(UNWANTED_FIELDS)
    for field in RoomModel.__fields__.keys():
        if field not in UNWANTED_FIELDS:
            records = client.collection('grouprooms').get_list(query_params={'filter': f'{field}~"{search_result}"' + filter_result})
            if len(records.items) == 0:
                empty_counter += 1
            data.update({field : records.items})
    if empty_counter == total_fields:
        raise RoomsNotFoundException(f"No rooms found with the search term '{search_result}'")
    rooms_with_status = update_room_statuses(data)
    return rooms_with_status

def filter_results(filters: dict):
    filter_parts = ""
    for field, value in filters.items():
        filter_parts += " && " + f'{field}~"{value}"'
    return filter_parts