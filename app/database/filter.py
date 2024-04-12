from database.pb import client

UNWANTED_FIELDS = ['expand', 'collection_id', 'collection_name', 'id', 'room_id', 'created', 'updated']

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
    for field in fields:
        if field not in UNWANTED_FIELDS:
            result = client.collection('grouprooms').get_list(query_params={'filter': f'{field}~"{search_result}"' + filter_result})
            if result.items:
                results.update({field : result.items})
    return results

def filter_results(filters):
    filter_parts = ""
    for field, value in filters.items():
        if (field, value):
            filter_parts += " && " + f'{field}~"{value}"'
    print(filter_parts)
    return filter_parts