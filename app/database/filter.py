from models.response import RoomModel
from database.pb import client
from database.rooms import room_format

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
    for field in RoomModel.__fields__.keys():
        if field not in UNWANTED_FIELDS:
            records = client.collection('grouprooms').get_list(query_params={'filter': f'{field}~"{search_result}"' + filter_result})
            data.update({field : records.items})
        
    formatted_data = room_format(data)
    return formatted_data

def filter_results(filters: dict):
    filter_parts = ""
    for field, value in filters.items():
        filter_parts += " && " + f'{field}~"{value}"'
    return filter_parts