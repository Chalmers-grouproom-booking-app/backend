from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from database.filter import search_filter
from database.rooms import get_all_rooms, get_room_info, show_room_reservations, show_all_reservations, is_room_booked, get_building_booked_percentage, get_room_id, get_all_buildings_booked_percentage
from models.response import ReservationModel, RoomModel, SearchModel, BookedModel, BuildingModel, RoomId
from exceptions.exceptions import ErrorResponse
from utils import validate_input
from exceptions.exceptions import ErrorResponse, RoomsNotFoundException, RoomNotFoundException, ReservationsNotFoundException

router = APIRouter(prefix="/api/v1", tags=["Room API"])

@router.get("/all_rooms", response_model=List[RoomModel], summary="Get all rooms from database", responses={404: {"model": ErrorResponse, "description": "Rooms not found"}})
async def get_all_rooms_info():
    rooms = get_all_rooms()
    if not rooms:
        raise RoomsNotFoundException()
    return rooms

@router.get("/room", response_model=RoomModel, summary="Get room info", responses={404: {"model": ErrorResponse, "description": "Room not found"}})
async def get_room_info_route(room_name: str = Depends(validate_input)):
    room = get_room_info(room_name)
    if room is None:
        raise RoomNotFoundException()
    return room

@router.get("/search", response_model=SearchModel, summary="Get search filtered results from database", responses={404: {"model": ErrorResponse, "description": "No results found"}})
async def search_db(
    search_input: str = Depends(validate_input),
    room_size: Optional[str] = Query("", description="Filter by room size"),
    building: Optional[str] = Query("", description="Filter by building"),
    campus: Optional[str] = Query("", description="Filter by campus"),
    equipment: Optional[str] = Query("", description="Filter by available equipment"),
    room_name: Optional[str] = Query("", description="Filter by room name"),
    first_come_first_served: Optional[str] = Query("", description="Filter by first come first served status"),
    floor_level: Optional[str] = Query("", description="Filter by floor level")
):
    filters = {k: v for k, v in locals().items() if v is not None and k != "search_input"}
    for key, value in filters.items():
        if value is not None:
            validate_input(value)  # Apply validation to each filter
    results = search_filter(search_input, filters)
    if not results:
        raise RoomsNotFoundException()
    return results

@router.get("/room/reservation", response_model=List[ReservationModel], summary="Get room reservations", responses={404: {"model": ErrorResponse, "description": "No reservations found"}})
async def get_reservation(room_name: str = Depends(validate_input)):
    reservations = show_room_reservations(room_name)
    if not reservations:
        raise ReservationsNotFoundException(f"No reservations found for room '{room_name}'")
    return reservations

# get room id by room name
@router.get("/room/id", response_model=RoomId, summary="Get room info by room id", responses={404: {"model": ErrorResponse, "description": "Room not found"}})
async def get_room_info_by_id( room_name: str = Depends(validate_input)):
    room_id = get_room_id(room_name)
    if room_id is None:
        raise RoomNotFoundException()
    return {"room_id": room_id}

@router.get("/room/reservation/all", response_model=List[ReservationModel], summary="Get room reservations", responses={404: {"model": ErrorResponse, "description": "No reservations found"}})
async def get_reservation(room_name: str = Depends(validate_input)):
    reservations = show_all_reservations(room_name)
    if not reservations:
        raise ReservationsNotFoundException(f"No reservations found for room '{room_name}'")
    return reservations

@router.get("/room/booked", response_model=List[BookedModel], summary="Get room booked status", responses={404: {"model": ErrorResponse, "description": "No room found"}})
async def get_room_booked(
    room_name: str = Depends(validate_input), 
    interval_forward_minutes: float = Query(30, description="Minutes forward interval")
):
    booked = [{"booked": is_room_booked(room_name, interval_forward_minutes)}]
    if booked == None:
        raise RoomNotFoundException('No booking found')
    return booked

@router.get("/building/percentage", response_model=float, summary="Get building booked percentage", responses={404: {"model": ErrorResponse, "description": "No building found"}})
async def get_building_percentage(
    building_name: str = Depends(validate_input), 
    interval_forward_minutes: float = Query(30, description="Minutes forward interval")
):
    percentage = get_building_booked_percentage(building_name, interval_forward_minutes)

    if percentage == None:
        raise RoomNotFoundException('No building found')
    return percentage

@router.get("/building/percentage/all", response_model=dict, summary="Get all building booked percentages", responses={404: {"model": ErrorResponse, "description": "No buildings found"}})
async def get_all_building_percentages(
    interval_forward_minutes: float = Query(30, description="Minutes forward interval")
):
    building_percentages = get_all_buildings_booked_percentage(interval_forward_minutes)

    if building_percentages == None:
        raise RoomNotFoundException('No buildings found')
    return building_percentages