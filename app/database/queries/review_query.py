from app.automatisation.auto_get_reservations import fetch_group_room_id
from app.models.response import ReviewOutput
from app.database.queries.room_query import RoomQuery
from exceptions.exceptions import FastAPIParseError, InvalidInputException, RoomNotFoundException
from database.pb import client
from datetime import datetime
import random
import re

class ReviewQuery:
    
    MAX_REVIEWS = 50
    
    def __init__(self, room_name: str=None):
        self.room_name = room_name
        self.room_filter = f'room_name="{self.room_name}"'
        
    def _get_review_id(self, account_name: str):
        return self._get_review_record(account_name).review_id
    
    def _get_review_item_id(self, account_name: str):
        return self._get_review_record(account_name).id
    
    def _get_review_score(self, account_name: str):
        return self._get_review_record(account_name).review_score
    
    def _get_review_text(self, account_name: str):
        return self._get_review_record(account_name).review_text
    
    def _get_review_date(self, account_name: str):
        return self._get_review_record(account_name).date
    
    def _get_review_review_id(self, account_name: str):
        return self._get_review_record(account_name).review_id
    
    def _get_review_item_by_id(self, review_id: int):
        review_filter = f"review_id={review_id}"
        review = client.collection('reviews').get_list(1, 1, {'filter': review_filter})
        if review.total_items == 0:
            raise RoomNotFoundException(f"No review found with review ID '{review_id}'")
        return review.items[0]
    
    @classmethod
    def get_review_by_review_id(cls, review_id: int) -> ReviewOutput:
        """Get a review by review ID"""
        review = ReviewQuery()._get_review_item_by_id(review_id)
        return ReviewOutput(**{
            "room_name": RoomQuery._get_room_name_by_id(review.room),
            "review_score": review.review_score,
            "review_text": review.review_text,
            "account_name": review.account_name,
            "review_id": review_id,
            "date": review.date
        })
        
    def create_review(self, review_score: float, account_name: str, review_text: str):
        """Put a review for a room"""
        fetch = client.collection('grouprooms').get_list(1, 1, {'filter': self.room_filter})
        if fetch.total_items == 0:
            raise RoomNotFoundException(f"Room '{self.room_name}' not found.")
        if review_score < 0.1 or review_score > 5:
            raise InvalidInputException("Review score must be between 0.1 and 5.")
        if len(review_text) > 500:
            raise InvalidInputException("Review text must be 500 characters or less.")
        review_filter = f"room.room_name='{self.room_name}' && account_name='{account_name}'"
        review =  client.collection('reviews').get_list(1, 1, {'filter': review_filter}).items
        if len(review) != 0:
            raise RoomNotFoundException(f"You already left a review for room '{self.room_name}' with this account")
        review_data = {
            "room": RoomQuery(self.room_name).get_room_item_id(),
            "review_score": review_score,
            "account_name": account_name,
            "review_text": review_text,
            "review_id": re.sub(r'\D', '', str(datetime.now()))[-8:] + str(random.randint(100, 999)),
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        print(review_data)
        try:
            client.collection('reviews').create(review_data)
        except:
            raise FastAPIParseError("FastAPI can not parse a 0 or 0.0.... as a float through JSON")
            
        
    def _get_review_record(self, account_name: str):
        review_filter = f"room.room_name='{self.room_name}' && account_name='{account_name}'"
        review =  client.collection('reviews').get_list(1, 1, {'filter': review_filter})
        if review.total_items == 0:
            raise RoomNotFoundException(f"No review found for room '{self.room_name}' by this account")
        return review.items[0]
    
    
    def get_account_review(self, account_name: str) -> ReviewOutput:
        """Get all reviews for a room"""
        # Check if room exists
        RoomQuery(self.room_name)._get_room_record()
        # review_data of type ReviewOutput
        review_data = {
            "room_name": self.room_name,
            "review_score": float(self._get_review_score(account_name)),
            "review_text": self._get_review_text(account_name),
            "account_name": account_name,
            "review_id": self._get_review_review_id(account_name),
            "date": self._get_review_date(account_name)
        }
        return ReviewOutput(**review_data)
    
    @classmethod
    def get_all_account_reviews(cls, account_name: str):
        """Get all reviews for a room"""
        review_filter = f"account_name='{account_name}'"
        review = client.collection('reviews').get_list(1, cls.MAX_REVIEWS, {'filter': review_filter})
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
    
    def get_all_reviews_for_room(self):
        """Get all reviews for a room"""
        # Check if room exists
        RoomQuery(self.room_name)._get_room_record()
        review_filter = f"room.room_name='{self.room_name}'"
        reviews = client.collection('reviews').get_list(1, self.MAX_REVIEWS, {'filter': review_filter})
        if reviews.total_items == 0:
            raise RoomNotFoundException(f"No reviews found for room '{self.room_name}'")
        return reviews.items
    
    @classmethod
    def delete_one_review(cls, review_id: int):
        """Delete a review"""
        review = ReviewQuery()._get_review_item_by_id(review_id)
        client.collection('reviews').delete(review.id)
       
    @classmethod 
    def put_review(cls, review_id: int, review_score: float, review_text: str) -> ReviewOutput:
        """Update a review"""
        review = ReviewQuery()._get_review_item_by_id(review_id)    
        if review_score < 0.1 or review_score > 5:
            raise InvalidInputException("Review score must be between 0.1 and 5.")
        if len(review_text) > 500:
            raise InvalidInputException("Review text must be 500 characters or less.")
        review_data = {
            "review_score": review_score,
            "review_text": review_text,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        client.collection('reviews').update(review.id, review_data)
        return ReviewOutput(**{
            "room_name": RoomQuery._get_room_name_by_id(review.room),
            "review_score": review_score,
            "review_text": review_text,
            "account_name": review.account_name,
            "review_id": review_id,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        