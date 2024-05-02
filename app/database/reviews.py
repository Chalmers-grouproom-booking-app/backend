from models.response import ReviewOutput
from database.queries.review_query import ReviewQuery
from database.queries.room_query import RoomQuery
from database.queries.account_querey import AccountQuery

def create_review(account_id: str,  room_name: str, review_score: float, review_text: str) -> None:
    return ReviewQuery.create_review(account_id,  room_name, review_score, review_text)
    
    
def get_account_review(room_name: str, account_id: str) -> ReviewOutput:
    return ReviewQuery(room_name).get_account_review(account_id)

def get_review_by_review_id(review_id: int) -> ReviewOutput:
    return ReviewQuery.get_review_by_review_id(review_id)

def get_all_account_reviews(account_id: str) -> list[ReviewOutput]:
    review_records = ReviewQuery.get_all_account_reviews(account_id)
    return [
        ReviewOutput(
            account_display_name=AccountQuery(record.account).get_display_name(),
            created=record.created,
            updated=record.updated,
            room_name=RoomQuery._get_room_name_by_id(record.room),
            review_score=record.review_score,
            review_text=record.review_text,
        )
        for record in review_records
    ]

def get_all_reviews_for_room(room_name: str) -> list[ReviewOutput]:
    review_records = ReviewQuery.get_all_reviews_for_room(room_name)
    reviews = []
    for record in review_records:
        print(record.account)
        review = ReviewOutput(
            account_display_name=  AccountQuery(record.account).get_display_name(),
            created=record.created,
            updated=record.updated,
            room_name= RoomQuery._get_room_name_by_id( record.room ),
            review_score=record.review_score,
            review_text=record.review_text,
        )
        reviews.append(review)
        
    return reviews

def get_all_reviews() -> list[ReviewOutput]:
    return [
        ReviewOutput(
            account_display_name=AccountQuery(record.account).get_display_name(),
            created=record.created,
            updated=record.updated,
            room_name=RoomQuery._get_room_name_by_id(record.room),
            review_score=record.review_score,
            review_text=record.review_text,
        )
        for record in ReviewQuery.get_all_reviews()
    ]

def delete_one_review(review_id: int):
    ReviewQuery.delete_one_review(review_id)
    
def put_review(review_id: str, review_score: float | int, review_text: str) -> ReviewOutput:
    return ReviewQuery.put_review(review_id, review_score, review_text)


    