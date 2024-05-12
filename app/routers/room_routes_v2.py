from fastapi import APIRouter, Depends, Query
from typing import Optional
from database.filter import search_filter, search_filter_V2
from models.response import SearchModel, SearchModelV2
from exceptions.exceptions import ErrorResponse
from utils import validate_input
from exceptions.exceptions import ErrorResponse, RoomsNotFoundException

router = APIRouter(prefix="/api/v2", tags=["Room API V2"])

@router.get("/search", response_model=SearchModelV2, summary="Get search filtered results from database", responses={404: {"model": ErrorResponse, "description": "No results found"}})
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
    results = search_filter_V2(search_input, filters)
    if not results:
        raise RoomsNotFoundException()
    return results
