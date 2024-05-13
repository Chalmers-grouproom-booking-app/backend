from models.response import ReviewOutput
from database.queries.review_query import ReviewQuery
from database.queries.room_query import RoomQuery
from database.queries.account_querey import AccountQuery

def create_review(account: str,  room_name: str, review_score: float, review_text: str) -> None:
    return ReviewQuery.create_review(account,  room_name, review_score, review_text)
    
    
def get_account_review(room_name: str, account: str) -> ReviewOutput:
    return ReviewQuery(room_name).get_account_review(account)

def get_review_by_id(id: int) -> ReviewOutput:
    return ReviewQuery.get_review_by_id(id)

def get_all_account_reviews(account: str) -> list[ReviewOutput]:
    review_records = ReviewQuery.get_all_account_reviews(account)
    return [
        ReviewOutput(**{
            "room_name": RoomQuery._get_room_name_by_id(record.room),
            "review_score": record.review_score,
            "review_text": record.review_text,
            "id": record.id,
            "created": record.created,
            "updated": record.updated
        })
        for record in review_records
    ]

def get_all_reviews_for_room(room_name: str) -> list[ReviewOutput]:
    review_records = ReviewQuery.get_all_reviews_for_room(room_name)
    reviews = []
    for record in review_records:
        review = ReviewOutput(**{
            "room_name": RoomQuery._get_room_name_by_id(record.room),
            "review_score": record.review_score,
            "review_text": record.review_text,
            "id": record.id,
            "created": record.created,
            "updated": record.updated
        })
        reviews.append(review)
    return reviews

def get_all_reviews() -> list[ReviewOutput]:
    return [
        ReviewOutput(**{
            "room_name": RoomQuery._get_room_name_by_id(record.room),
            "review_score": record.review_score,
            "review_text": record.review_text,
            "id": record.id,
            "created": record.created,
            "updated": record.updated
        })
        for record in ReviewQuery.get_all_reviews()
    ]

def delete_one_review(id: str):
    ReviewQuery.delete_one_review(id)
    
def put_review(id: str, review_score: float | int, review_text: str) -> ReviewOutput:
    return ReviewQuery.put_review(id, review_score, review_text)


    