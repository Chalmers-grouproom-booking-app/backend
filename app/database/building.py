from database.pb import client


def get_building(self, building: str):
    filter = f"building = {building}"
    building_record = client.collection('grouprooms').get_list(
        1, 1,  {'filter': filter}
    )
    print(building_record)
    return building_record