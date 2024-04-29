from app.models.response import ReviewOutput
from database.pb import client
from database.queries.review_query import ReviewQuery
from database.queries.room_query import RoomQuery

def create_review(room_name: str, review_score: float, account_name: str, review_text: str):
    ReviewQuery(room_name).create_review(review_score, account_name, review_text)
    
def get_account_review(room_name: str, account_name: str) -> ReviewOutput:
    return ReviewQuery(room_name).get_account_review(account_name)

def get_review_by_review_id(review_id: int) -> ReviewOutput:
    return ReviewQuery.get_review_by_review_id(review_id)

def get_all_account_reviews(account_name: str) -> list[ReviewOutput]:
    review_records = ReviewQuery.get_all_account_reviews(account_name)
    reviews = []
    for rev in review_records:
        review = {
            "room_name": RoomQuery._get_room_name_by_id( rev.room),
            "review_score": rev.review_score,
            "review_text": rev.review_text,
            "account_name": rev.account_name,
            "review_id": rev.review_id,
            "date": rev.date   
        }
        print(review)
        reviews.append(ReviewOutput(**review))
    return reviews

def get_all_reviews_for_room(room_name: str) -> list[ReviewOutput]:
    review_records = ReviewQuery(room_name).get_all_reviews_for_room()
    reviews = []
    for rev in review_records:
        review = {
            "room_name": RoomQuery._get_room_name_by_id( rev.room),
            "review_score": rev.review_score,
            "review_text": rev.review_text,
            "account_name": rev.account_name,
            "review_id": rev.review_id,
            "date": rev.date   
        }
        reviews.append(ReviewOutput(**review))
    return reviews

def get_all_reviews() -> list[ReviewOutput]:
    review_records = ReviewQuery.get_all_reviews()
    reviews = []
    for rev in review_records:
        review = {
            "room_name": RoomQuery._get_room_name_by_id( rev.room),
            "review_score": rev.review_score,
            "review_text": rev.review_text,
            "account_name": rev.account_name,
            "review_id": rev.review_id,
            "date": rev.date   
        }
        reviews.append(ReviewOutput(**review))
    return reviews

def delete_one_review(review_id: int):
    ReviewQuery.delete_one_review(review_id)
    
def put_review(review_id: int, review_score: float, review_text: str) -> ReviewOutput:
    
    return ReviewQuery.put_review(review_id, review_score, review_text)


    