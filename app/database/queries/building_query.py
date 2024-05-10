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
        data = client.collection("grouprooms").get_full_list()
        print(pd.DataFrame(data))
        buildings = []
        for entry in data:
            if (entry.building not in buildings):
                buildings.append(entry.building)
        return buildings