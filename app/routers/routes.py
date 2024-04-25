from fastapi import APIRouter, Depends, Query, HTTPException, status, Path, Response
from typing import List, Optional
from database.filter import search_filter
from database.rooms import get_all_rooms, get_room_info, show_room_reservations, show_all_reservations
from models.response import ReservationModel, RoomModel, SearchModel
from utils import validate_input
from exceptions.exceptions import ErrorResponse, RoomsNotFoundException, RoomNotFoundException, ReservationsNotFoundException

router = APIRouter(prefix="/api/v1")

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

@router.get("/room/reservation/all", response_model=List[ReservationModel], summary="Get room reservations", responses={404: {"model": ErrorResponse, "description": "No reservations found"}})
async def get_reservation(room_name: str = Depends(validate_input)):
    reservations = show_all_reservations(room_name)
    if not reservations:
        raise ReservationsNotFoundException(f"No reservations found for room '{room_name}'")
    return reservations
