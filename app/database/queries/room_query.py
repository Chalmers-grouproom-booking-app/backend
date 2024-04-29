from exceptions.exceptions import RoomNotFoundException
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
        fetch = client.collection('grouprooms').get_list(1, 1, {'filter': self.room_filter})
        if fetch.total_items == 0:
            raise RoomNotFoundException(f"Room '{self.room_name}' not found.")
        return fetch.items[0]
    
    @classmethod
    def _get_room_record_by_id(cls, id: str):
        """Fetch the room record from the database."""
        fetch = client.collection('grouprooms').get_list(1, 1, {'filter': f'id="{id}"'})
        if fetch.total_items == 0:
            raise RoomNotFoundException(f"The id '{id}' does not correspond to a room.")
        return fetch.items[0]
    
    @classmethod
    def _get_room_name_by_id(cls, id: str):
        return cls._get_room_record_by_id(id).room_name

    def get_building(self):
        """Return the building name for the room."""
        return self._get_room_record().building

    def get_reservations(self):
        """Return the reservation records for the room."""
        fetch = client.collection('grouprooms').get_list(1, 1, {'filter': self.room_filter})
        if fetch.total_items == 0:
            raise RoomNotFoundException(f"Room '{self.room_name}' not found.")
        reservation_filter = f"room.room_name='{self.room_name}'"
        return client.collection('reservations').get_list(1, self.MAX_RESERVATIONS, {'filter': reservation_filter}).items

    def get_room(self):
        """Return the  record."""
        return self._get_room_record()
    
    def get_room_id(self):
        """Return the room ID."""
        return self._get_room_record().room_id
    
    def get_room_item_id(self):
        """Return the room item ID."""
        return self._get_room_record().id
    
    @classmethod
    def get_all_rooms(cls):
        """Return all rooms in the database."""
        return client.collection('grouprooms').get_full_list()
    