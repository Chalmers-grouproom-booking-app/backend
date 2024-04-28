from app.models.response import ReviewOutput
from database.pb import client
from database.queries import ReviewQuery, RoomQuery

def create_review(room_name: str, review_score: float, account_name: str, review_text: str):
    ReviewQuery(room_name).create_review(float(review_score), str(account_name), str(review_text))
    
def get_account_review(room_name: str, account_name: str) -> ReviewOutput:
    return ReviewQuery(room_name).get_account_review(account_name)

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
    