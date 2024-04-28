from fastapi import APIRouter, Depends, Query
from typing import Dict, List, Optional
from database.filter import search_filter
from database.reviews import create_review, delete_one_review, get_account_review, get_all_account_reviews, get_all_reviews, get_all_reviews_for_room, get_review_by_review_id, put_review
from database.rooms import get_all_rooms, get_room_info, show_room_reservations, show_all_reservations, is_room_booked, get_building_booked_percentage, get_room_id
from models.response import ReservationModel, ReviewInput, ReviewOutput, ReviewResponse, ReviewScoreResponse, RoomModel, SearchModel, BookedModel, BuildingModel, RoomId
from exceptions.exceptions import ErrorResponse, MissingInputException
from utils import validate_float_input, validate_input, validate_integer_input
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
    interval_forward_hours: float = Query(0.5, description="Hours forward interval")
):
    booked = [{"booked": is_room_booked(room_name, interval_forward_hours)}]
    if booked == None:
        raise RoomNotFoundException('No booking found')
    return booked

@router.get("/building/percentage", response_model=List[BuildingModel], summary="Get building booked percentage", responses={404: {"model": ErrorResponse, "description": "No building found"}})
async def get_building_percentage(
    building_name: str = Depends(validate_input), 
    interval_forward_hours: float = Query(0.5, description="Hours forward interval")
):
    percentage = get_building_booked_percentage(building_name, interval_forward_hours)
    if percentage == None:
        raise RoomNotFoundException('No building found')
    return [{
        "booked_percentage": percentage
    }]
    
@router.post("/review/create", response_model=ReviewResponse, summary="Leave a review of a room", responses={422: {"model": ErrorResponse, "description": "Missing input"}})
async def leave_review(review: ReviewInput):

    required_fields = [field_name for field_name, field_type in ReviewInput.__annotations__.items() if field_type.__class__.__name__ == 'Type']

    if any(field not in review.dict() for field in required_fields):
        raise MissingInputException("Missing input. Please provide room, review score, and account ID.")

    if review.review_text is None:
        review.review_text = ""
    
    filters = {k: v for k, v in review.dict().items() if v is not None and (k != "review_text" and k != "review_score")}
    for key, value in filters.items():
        validate_input(value)  # Apply validation to each filter
            
    create_review(review.room_name, review.review_score, review.account_name, review.review_text)
    return {"message": "Review successfully submitted"}

@router.get("/review/account", response_model=ReviewOutput, summary="Get review of a room from given account", responses={404: {"model": ErrorResponse, "description": "No review found"}})
async def get_review(room_name: str, account_name: str ):
    inputs  = [room_name, account_name]
    for input in inputs:
        validate_input(input)
    review = get_account_review(room_name, account_name)
    return review

@router.get("/review/id", response_model=ReviewOutput, summary="Get review of a room by review id", responses={404: {"model": ErrorResponse, "description": "No review found"}, 422: {"model": ErrorResponse, "description": "Input must be a single integer"}})
async def get_review_by_id(review_id: int):
    validate_integer_input(review_id)
    review = get_review_by_review_id(review_id)
    return review

@router.get("/review/account/all", response_model=List[ReviewOutput], summary="Get all reviews made by given account", responses={404: {"model": ErrorResponse, "description": "No reviews found"}, 422: {"model": ErrorResponse, "description": "Input must be a single integer"}})
async def get_reviews(account_name: str):
    validate_input(account_name)
    reviews = get_all_account_reviews(account_name)
    return reviews

@router.get("/review/room/all", response_model=List[ReviewOutput], summary="Get all reviewsmade for given room", responses={404: {"model": ErrorResponse, "description": "No reviews found"}})
async def get_reviews(room_name: str = Depends(validate_input)):
    reviews = get_all_reviews_for_room(room_name)
    return reviews

@router.get("/review/all", response_model=List[ReviewOutput], summary="Get all reviews", responses={404: {"model": ErrorResponse, "description": "No reviews found"}})
async def get_reviews():
    reviews = get_all_reviews()
    return reviews

@router.delete("/review/delete/one", response_model=ReviewResponse, summary="Delete a review of a room", responses={404: {"model": ErrorResponse, "description": "No reviews found"}})
async def delete_review(review_id: int):
    validate_integer_input(review_id)
    delete_one_review(review_id)
    return {"message": "Review successfully deleted"}

@router.put("/review/update", response_model=ReviewResponse, summary="Update a review of a room", responses={404: {"model": ErrorResponse, "description": "No reviews found"}})
async def update_review(review_id: int, review_score: float, review_text: str):
    validate_integer_input(review_id)
    validate_float_input(review_score)
    put_review(review_id, review_score, review_text)
    return {"message": "Review successfully updated"}

@router.get("/review/room/score", response_model=ReviewScoreResponse, summary="Get average review score of a room", responses={404: {"model": ErrorResponse, "description": "No reviews found"}})
async def get_review_score(room_name: str = Depends(validate_input)):
    reviews = get_all_reviews_for_room(room_name)
    if not reviews:
        raise RoomsNotFoundException()
    score = sum([review.review_score for review in reviews]) / len(reviews)
    return {"average_score": score}



