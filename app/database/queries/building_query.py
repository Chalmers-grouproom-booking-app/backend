from exceptions.exceptions import RoomNotFoundException
from database.pb import client

class BuildingQuery:
    MAX_RESERVATIONS = 50

    def __init__(self, building: str):
        self.building = building
        
    def get_all_rooms_in_building(self):
        """Return all rooms in a building"""
        reservation_filter = f"building='{self.building}'"
        rooms = client.collection('grouprooms').get_list(1, self.MAX_RESERVATIONS, {'filter': reservation_filter}).items
        if not rooms:
            raise RoomNotFoundException(f"No building found called '{self.building}'")
        return rooms