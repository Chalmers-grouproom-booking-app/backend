from pydantic import BaseModel
from typing import List, Optional
import datetime

class Login(BaseModel):
    login: str

class RoomDetails(BaseModel):
    id: str
    created: datetime.datetime
    updated: datetime.datetime
    expand: dict
    collection_id: str
    collection_name: str
    address: str
    building: str
    campus: str
    description: Optional[str]
    entrance_latitude: float
    entrance_longitude: float
    equipment: Optional[str]
    first_come_first_served: bool
    floor_level: int
    latitude: float
    longitude: float
    room_id: int
    room_name: str
    room_size: int
    stair: Optional[str]

#only room id
class RoomId(BaseModel):
    room_id: int

class RoomModel(BaseModel):
    room_name: str
    room_size: Optional[int]
    building: str
    campus: str
    equipment: Optional[str] 
    longitude: float
    latitude: float
    entrance_latitude: float
    entrance_longitude: float
    description: Optional[str] 
    first_come_first_served: bool
    floor_level: Optional[int] 
    stair: Optional[str] 

class ReservationModel(BaseModel):
    start_date: str
    start_time: str
    end_time: str
    end_date: str

class BookedModel(BaseModel): ### Kanske ta bort och lägga i RoomModel!
    booked: bool

class BuildingModel(BaseModel):
    building_name: str
    color: List[int]

class SearchModel(BaseModel):
    building: Optional[ List[ RoomModel] ] 
    room_name: Optional[ List[ RoomModel ] ] 
    room_size: Optional[  List[ RoomModel ] ] 
    floor_level: Optional[  List[ RoomModel ] ] 
    first_come_first_served: Optional[  List[ RoomModel ] ] 
    