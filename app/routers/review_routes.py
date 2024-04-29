from fastapi import APIRouter, Depends
from typing import List
from database.reviews import create_review, delete_one_review, get_account_review, get_all_account_reviews, get_all_reviews, get_all_reviews_for_room, get_review_by_review_id, put_review
from models.response import ReviewInput, ReviewOutput, ReviewResponse, ReviewScoreResponse
from exceptions.exceptions import ErrorResponse, MissingInputException
from utils import validate_float_input, validate_input, validate_integer_input
from exceptions.exceptions import ErrorResponse, RoomsNotFoundException

router = APIRouter(prefix="/review/api", tags=["Review API"])

@router.get("/account", response_model=ReviewOutput, summary="Get review of a room from given account", responses={404: {"model": ErrorResponse, "description": "No review found"}})
async def get_review(room_name: str, account_name: str ):
    inputs  = [room_name, account_name]
    for input in inputs:
        validate_input(input)
    review = get_account_review(room_name, account_name)
    return review

@router.get("/id", response_model=ReviewOutput, summary="Get review of a room by review id", responses={404: {"model": ErrorResponse, "description": "No review found"}, 422: {"model": ErrorResponse, "description": "Input must be a single integer"}})
async def get_review_by_id(review_id: int):
    validate_integer_input(review_id)
    review = get_review_by_review_id(review_id)
    return review

@router.get("/account/all", response_model=List[ReviewOutput], summary="Get all reviews made by given account", responses={404: {"model": ErrorResponse, "description": "No reviews found"}, 422: {"model": ErrorResponse, "description": "Input must be a single integer"}})
async def get_reviews(account_name: str):
    validate_input(account_name)
    reviews = get_all_account_reviews(account_name)
    return reviews

@router.get("/room/all", response_model=List[ReviewOutput], summary="Get all reviews made for given room", responses={404: {"model": ErrorResponse, "description": "No reviews found"}})
async def get_reviews(room_name: str = Depends(validate_input)):
    reviews = get_all_reviews_for_room(room_name)
    return reviews

@router.get("/all", response_model=List[ReviewOutput], summary="Get all reviews", responses={404: {"model": ErrorResponse, "description": "No reviews found"}})
async def get_reviews():
    reviews = get_all_reviews()
    return reviews

@router.get("/room/score", response_model=ReviewScoreResponse, summary="Get average review score of a room", responses={404: {"model": ErrorResponse, "description": "No reviews found"}})
async def get_review_score(room_name: str = Depends(validate_input)):
    reviews = get_all_reviews_for_room(room_name)
    if not reviews:
        raise RoomsNotFoundException()
    score = sum([review.review_score for review in reviews]) / len(reviews)
    return {"average_score": score}

@router.post("/create", response_model=ReviewResponse, summary="Create a review of a room", responses={422: {"model": ErrorResponse, "description": "Missing input"}})
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

@router.delete("/delete", response_model=ReviewResponse, summary="Delete a review of a room", responses={404: {"model": ErrorResponse, "description": "No reviews found"}})
async def delete_review(review_id: int):
    validate_integer_input(review_id)
    delete_one_review(review_id)
    return {"message": "Review successfully deleted"}

@router.put("/update", response_model=ReviewResponse, summary="Update a review of a room", responses={404: {"model": ErrorResponse, "description": "No reviews found"}})
async def update_review(review_id: int, review_score: float, review_text: str):
    validate_integer_input(review_id)
    validate_float_input(review_score)
    put_review(review_id, review_score, review_text)
    return {"message": "Review successfully updated"}



