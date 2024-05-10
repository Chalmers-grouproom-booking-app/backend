from database.queries.account_querey import AccountQuery
from models.response import ReviewOutput
from database.queries.room_query import RoomQuery
from exceptions.exceptions import  InvalidInputException, RoomNotFoundException
from database.pb import client

class ReviewQuery:
    
    MAX_REVIEWS = 50
    collection = client.collection('reviews')
    def __init__(self, room_name: str=None):
        self.room_name = room_name
        self.room_filter = f'room_name="{self.room_name}"'      
    
    def _get_review_item_id(self, account: str):
        return self._get_review_record(account).id
    
    def _get_review_room_id(self, account: str):
        return self._get_review_record(account).room
    
    def _get_review_score(self, account: str):
        return self._get_review_record(account).review_score
    
    def _get_review_text(self, account: str):
        return self._get_review_record(account).review_text
    
    def _get_review_created(self, account: str):
        return self._get_review_record(account).created
    
    def _get_review_updated(self, account: str):
        return self._get_review_record(account).updated

    def _get_review_item_by_id(self, id: str):
        review_filter = f'id="{id}"'
        review = client.collection('reviews').get_list(1, 1, {'filter': review_filter})
        if review.total_items == 0:
            raise RoomNotFoundException(f"No review found with review ID '{id}'")
        return review.items[0]
    
    @classmethod
    def get_review_by_id(cls, id: str) -> ReviewOutput:
        """Get a review by review ID"""
        review = ReviewQuery()._get_review_item_by_id(id)
        return ReviewOutput(**{
            "room_name": RoomQuery._get_room_name_by_id(review.room),
            "review_score": review.review_score,
            "review_text": review.review_text,
            "id": id,
            "created": review.created,
            "updated": review.updated
        })
        
    @classmethod
    def create_review( cls, account: str, room_name: str, review_score: float | int, review_text: str) -> None:
        if len(review_text) > 500:
            raise InvalidInputException("Review text must be 500 characters or less.")
        room_id = RoomQuery(room_name).get_room_item_id()
        old_review  = cls.collection.get_list(1, cls.MAX_REVIEWS, {'filter': f"room.room_name='{room_name}' && account='{account}'"})
        if old_review.total_items > 0:
            raise RoomNotFoundException(f"Review already exists for room '{room_name}' by this account")
        review_data = {
            "room": room_id,
            "review_score": review_score,
            "review_text": review_text if review_text else None,
            "account": account,
        }
        print(review_data)
        cls.collection.create(review_data)
            
        
    def _get_review_record(self, account: str):
        review_filter = f"room.room_name='{self.room_name}' && account='{account}'"
        review =  client.collection('reviews').get_list(1, 1, {'filter': review_filter})
        if review.total_items == 0:
            raise RoomNotFoundException(f"No review found for room '{self.room_name}' by this account")
        return review.items[0]
    
    def get_account_review(self, account: str) -> ReviewOutput:
        """Get review for a room By account ID"""
        RoomQuery(self.room_name).get_room_item_id()
        review  = self.collection.get_list(1, self.MAX_REVIEWS, {'filter': f"room.room_name='{self.room_name}' && account='{account}'"})
        if review.total_items == 0:
            raise RoomNotFoundException(f"No review found for {self.room_name} by this account")
        record = review.items[0]
        return ReviewOutput(**{
            "room_name": self.room_name,
            "review_score": record.review_score,
            "review_text": record.review_text,
            "id": record.id,
            "created": record.created,
            "updated": record.updated
        })
    
    @classmethod
    def get_all_account_reviews(cls, account: str):
        """Get all account reviews"""
        review =  cls.collection.get_list(1, cls.MAX_REVIEWS, {'filter': f"account='{account}'"})
        if review.total_items == 0:
            raise RoomNotFoundException("No reviews found on this account")
        return review.items
    
    @classmethod
    def get_all_reviews(cls):
        """Get all reviews"""
        reviews = client.collection('reviews').get_full_list()
        if len(reviews) == 0:
            raise RoomNotFoundException("No reviews found")
        return reviews
    
    @classmethod
    def get_all_reviews_for_room(cls, room_name: str):
        """Get all reviews for a room"""
        RoomQuery(room_name).get_room_item_id()
        reviews = cls.collection.get_list(1, cls.MAX_REVIEWS, {'filter': f"room.room_name='{room_name}'"})
        if reviews.total_items == 0:
            raise RoomNotFoundException(f"No reviews found for room '{room_name}'")
        return reviews.items
    
    @classmethod
    def delete_one_review(cls, id: str):
        """Delete a review"""
        review = ReviewQuery()._get_review_item_by_id(id)
        client.collection('reviews').delete(review.id)
       
    @classmethod 
    def put_review(cls, id: str, review_score: float | int , review_text: str) -> ReviewOutput:
        review = ReviewQuery()._get_review_item_by_id(id)
        review_data = {
            "review_score": review_score,
            "review_text": review_text if review_text else "",
        }
        client.collection('reviews').update(review.id, review_data)
        return ReviewOutput(**{
            "room_name": RoomQuery._get_room_name_by_id(review.room),
            "review_score": review_score,
            "review_text": review_text,
            "id": id,
            "created": review.created,
            "updated": review.updated
        })
    