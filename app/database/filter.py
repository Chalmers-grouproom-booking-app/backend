from database.pb import client
from database.rooms import room_format

UNWANTED_FIELDS = ['expand', 'collection_id', 'collection_name', 'id', 'room_id', 'created', 'updated', 'longitude', 'latitude','entrance_longitude', 'entrance_latitude', 'description', 'stair']

def get_fields(records):
    if records.items:
        item = records.items[0]
        fields = list(vars(item).keys())
    return fields

def search(search_result):
    result = client.collection('grouprooms').get_list()
    fields = get_fields(result)
    results = {}
    for field in fields:
        if field not in UNWANTED_FIELDS:
            result = client.collection('grouprooms').get_list(query_params={'filter': f'{field}~"{search_result}"'})
            if result.items:
                results.update({field : result.items})
    return results

def search_filter(search_result, filter):
    result = client.collection('grouprooms').get_list()
    fields = get_fields(result)
    results = {}
    filter_result = filter_results(filter)
    real_results = []
    for field in fields:
        if field not in UNWANTED_FIELDS:
            result = client.collection('grouprooms').get_list(query_params={'filter': f'{field}~"{search_result}"' + filter_result})
            if result.items:
                results.update({field : result.items})
            formatted_data = room_format(result)
            if len(formatted_data) != 0:
                real_results.append(formatted_data)
    if len(real_results) == 0:
        return ["No results found"]
    return real_results

def filter_results(filters):
    filter_parts = ""
    for field, value in filters.items():
        filter_parts += " && " + f'{field}~"{value}"'
    return filter_parts