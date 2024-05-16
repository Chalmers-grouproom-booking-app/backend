from exceptions.exceptions import RoomNotFoundException
from database.pb import client
import pandas as pd
import datetime

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
        data = client.collection('grouprooms').get_list(1, 310)
        df.columns = ["record"]

        df = df['record'].apply(_get_building_name_from_record_item)
        return df.unique()

    def get_building_reservations(self, minutes_interval: int):
        now = datetime.datetime.now()
        now_today = now.strftime('%Y-%m-%d')
        now_hour = now.strftime('%H:%M')
        in_30_minutes = (now + datetime.timedelta(minutes=minutes_interval)).strftime('%H:%M')
        reservations_in_building = client.collection('reservations').get_full_list(
            400,
            {'filter': f'((startdate~"{now_today}" && endtime>"{now_hour}" && starttime<"{now_hour}") && room.building="{self.building}") || ((startdate~"{now_today}" && starttime>="{now_hour}" && starttime<="{in_30_minutes}") && room.building="{self.building}")'}
        )
    
        return reservations_in_building


def _get_building_name_from_record_item(record_item):
    return record_item.building
    