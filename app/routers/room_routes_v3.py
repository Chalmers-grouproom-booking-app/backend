from fastapi import APIRouter, Depends, Query
from typing import Optional
from database.reservations import RoomStatus
from database.filter import search_filter_V3
from models.response import SearchModelV2
from exceptions.exceptions import ErrorResponse
from utils import validate_input_V2
from exceptions.exceptions import ErrorResponse, RoomsNotFoundException

router = APIRouter(prefix="/api/v3", tags=["Room API V3"])

# RoomStatus Enum
@router.get("/search", response_model=SearchModelV2, summary="Get search filtered results from database", responses={404: {"model": ErrorResponse, "description": "No results found"}})
async def search_db(
    search_input: str = Depends(validate_input_V2),
    room_size: Optional[str] = Query("", description="Filter by room size"),
    building: Optional[str] = Query("", description="Filter by building"),
    equipment: Optional[str] = Query("", description="Filter by available equipment"),
    room_name: Optional[str] = Query("", description="Filter by room name"),
    first_come_first_served: Optional[str] = Query("", description="Filter by first come first served status"),
    status: Optional[RoomStatus] =  Query(None, description="Filter by room status", enum=['available', 'occupied', 'soon_occupied'])
):
    filters = {k: v for k, v in locals().items() if v is not None and (k != "search_input" and k != "status")}
    for key, value in filters.items():
        if value is not None:
            validate_input_V2(value)  # Apply validation to each filter
    results = search_filter_V3(search_input, filters, status)
    if not results:
        raise RoomsNotFoundException()
    return results
