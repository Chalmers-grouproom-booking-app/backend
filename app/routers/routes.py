from fastapi import APIRouter, Query, HTTPException, status, Path, Response
from typing import List, Optional
from app.database.filter import search_filter
from app.database.rooms import get_all_rooms, get_room_info, show_room_reservations
from app.models.response import ReservationModel, RoomModel, SearchModel
from app.exceptions.exceptions import ErrorResponse
import re

router = APIRouter(prefix="/api/v1")

@router.get("/all_rooms", response_model=List[RoomModel], summary="Get all rooms from database", responses={404: {"model": ErrorResponse, "description": "Rooms not found"}})
async def get_all_rooms_info():
    rooms = get_all_rooms()
    if not rooms:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rooms not found")
    return rooms

@router.get("/room/{room_name}", response_model=RoomModel, summary="Get room info", responses={404: {"model": ErrorResponse, "description": "Room not found"}})
async def get_room_info_route(room_name: str = Path(..., description="The name of the room to fetch")):
    room = get_room_info(room_name)
    if room is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
    return room

@router.get("/search/{search_input}", response_model=SearchModel, summary="Get search filtered results from database", responses={404: {"model": ErrorResponse, "description": "No results found"}})
async def search_db(
    search_input: str = Path(..., description="The search input to filter rooms", min_length=1, max_length=50),
    room_size: Optional[str] = Query("", description="Filter by room size"),
    building: Optional[str] = Query("", description="Filter by building"),
    campus: Optional[str] = Query("", description="Filter by campus"),
    equipment: Optional[str] = Query("", description="Filter by available equipment"),
    room_name: Optional[str] = Query("", description="Filter by room name"),
    first_come_first_served: Optional[str] = Query("", description="Filter by first come first served status"),
    floor_level: Optional[str] = Query("", description="Filter by floor level")
):
    if not re.match(r"^[a-zA-Z0-9\s]*$", search_input):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid search input")
    filters = {k: v for k, v in locals().items() if v is not None and k != "search_input"}
    for k, v in filters.items():
        if not re.match(r"^[a-zA-Z0-9\s]*$", v):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid filter input")
    results = search_filter(search_input, filters)
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No results found")
    return results

@router.get("/room/reservation/{room_name}", response_model=List[ReservationModel], summary="Get room reservations", responses={404: {"model": ErrorResponse, "description": "No reservations found"}})
async def get_reservation(room_name: str = Path(..., description="The name of the room to check reservations for")):
    reservations = show_room_reservations(room_name)
    if not reservations:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No reservations found")
    return reservations
