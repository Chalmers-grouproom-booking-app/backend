from exceptions.exceptions import RoomNotFoundException
from database.pb import client
import pandas as pd

class BuildingQuery:
    MAX_RESERVATIONS = 50

    def __init__(self, building: str):
        self.building = building
        
    def get_all_rooms_in_building(self):
        """Return all rooms in a building"""
        building_filter = f"building='{self.building}'"
        rooms = client.collection('grouprooms').get_list(1, self.MAX_RESERVATIONS, {'filter': building_filter}).items
        if not rooms:
            raise RoomNotFoundException(f"No building found called '{self.building}'")
        return rooms
    

    def get_all_buildings(self):
        """Return all buildings"""
        df = pd.DataFrame(client.collection('grouprooms').get_list(1, 310).items)
        df.columns = ["record"]

        df = df['record'].apply(_get_building_name_from_record_item)
        #buildings = []
        #for entry in record:
        #    if (entry.building not in buildings):
        #        buildings.append(entry.building)
        return df.unique()

def _get_building_name_from_record_item(record_item):
    return record_item.building