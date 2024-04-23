from database.pb import client

class RoomQuery:
    """Handles queries related to a specific room."""
    MAX_RESERVATIONS = 50

    def __init__(self, room_name: str):
        """Initialize with the name of the room to query."""
        self.room_name = room_name
        self.room_filter = f'room_name="{self.room_name}"'

    def _get_room_record(self):
        """Fetch the room record from the database."""
        fetch = client.collection('grouprooms').get_list(1, 1,  {'filter': self.room_filter})
        if fetch.total_items == 0:
            raise ValueError(f"Room '{self.room_name}' not found.")
        
        return fetch.items[0]

    def get_building(self):
        """Return the building name for the room."""
        return self._get_room_record().building

    def get_reservations(self):
        """Return the reservation records for the room."""
        reservation_filter = f"room.room_name='{self.room_name}'"
        return client.collection('reservations').get_list(1, self.MAX_RESERVATIONS, {'filter': reservation_filter}).items

    def get_room(self):
        """Return the  record."""
        return self._get_room_record()
    
    @classmethod
    def get_all_rooms(cls):
        """Return all rooms in the database."""
        return client.collection('grouprooms').get_full_list()

class BuildingQuery:
    MAX_RESERVATIONS = 50

    def __init__(self, building: str):
        self.building = building
        
    def get_all_rooms_in_building(self):
        """Return all rooms in a building"""
        reservation_filter = f"building='{self.building}'"
        rooms = client.collection('grouprooms').get_list(1, self.MAX_RESERVATIONS, {'filter': reservation_filter}).items