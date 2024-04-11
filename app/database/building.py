from database.pb import client

class Building:

    def get_building(building: str):
        filter = f"building = {building}"
        building_record = client.collection('grouprooms').get_list(
            1, 1,  {'filter': filter}
        )
        return building_record