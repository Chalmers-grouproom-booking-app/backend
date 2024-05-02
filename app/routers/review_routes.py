from fastapi import APIRouter, Depends
from typing import List
from utils import validate_float_input, validate_input, validate_integer_input
from database.reviews import create_review, delete_one_review, get_account_review, get_all_account_reviews, get_all_reviews, get_all_reviews_for_room, get_review_by_review_id, put_review
from models.response import ReviewInput, ReviewOutput, ReviewResponse, ReviewScoreResponse
from exceptions.exceptions import ErrorResponse, RoomsNotFoundException
from routers.account import User, get_current_user

public_router = APIRouter(prefix="/review/api", tags=["Review API - Public"])
private_router = APIRouter(prefix="/review/api", tags=["Review API - Private"])

#----------- Public routes ------------
@public_router.get("/room-reviews", response_model=List[ReviewOutput])
async def get_reviews_for_room(room_name: str = Depends(validate_input)):
    reviews = get_all_reviews_for_room(room_name)
    return reviews

@public_router.get("/all-reviews", response_model=List[ReviewOutput])
async def get_all_reviews_route():
    reviews = get_all_reviews()
    return reviews

@public_router.get("/room-average-score", response_model=ReviewScoreResponse)
async def get_average_review_score(room_name: str = Depends(validate_input)):
    reviews = get_all_reviews_for_room(room_name)
    if not reviews:
        raise RoomsNotFoundException()
    score = sum([review.review_score for review in reviews]) / len(reviews)
    return {"average_score": score}

# ----------- Private routes ------------
@private_router.get("/my-room-review", response_model=ReviewOutput)
async def get_my_review_for_room(room_name: str, current_user: User = Depends(get_current_user)):
    review = get_account_review(validate_input(room_name), current_user.id)
    return review

@private_router.get("/my-reviews", response_model=List[ReviewOutput])
async def get_my_reviews(current_user: User = Depends(get_current_user)):
    reviews = get_all_reviews_for_room(current_user.id)
    return reviews

@private_router.post("/create-review", response_model=ReviewResponse)
async def leave_review(review: ReviewInput, current_user: User = Depends(get_current_user)):
    create_review( current_user.id, review.room_name, review.review_score, review.review_text )
    return {"message": "Review successfully submitted"}

@private_router.delete("/delete-review/{review_id}", response_model=ReviewResponse)
async def delete_my_review(review_id: str, current_user: User = Depends(get_current_user)):
    delete_one_review(review_id)
    return {"message": "Review successfully deleted"}

@private_router.put("/update-review/{review_id}", response_model=ReviewResponse)
async def update_my_review(review_id: str, review_score: int | float, review_text: str, current_user: User = Depends(get_current_user)):
    put_review(review_id, review_score, review_text)
    return {"message": "Review successfully updated"}