from app.automatisation.auto_get_reservations import fetch_group_room_id
from app.models.response import ReviewInput, ReviewOutput
from exceptions.exceptions import FastAPIParseError, InvalidInputException, RoomNotFoundException
from database.pb import client
from datetime import datetime
from datetime import timedelta
import random
import re

class RoomQuery:
    """Handles queries related to a specific room."""
    MAX_RESERVATIONS = 50

    def __init__(self, room_name: str):
        """Initialize with the name of the room to query."""
        self.room_name = room_name
        self.room_filter = f'room_name="{self.room_name}"'

    def _get_room_record(self):
        """Fetch the room record from the database."""
        fetch = client.collection('grouprooms').get_list(1, 1, {'filter': self.room_filter})
        if fetch.total_items == 0:
            raise RoomNotFoundException(f"Room '{self.room_name}' not found.")
        return fetch.items[0]
    
    @classmethod
    def _get_room_record_by_id(cls, id: str):
        """Fetch the room record from the database."""
        fetch = client.collection('grouprooms').get_list(1, 1, {'filter': f'id="{id}"'})
        if fetch.total_items == 0:
            raise RoomNotFoundException(f"The id '{id}' does not correspond to a room.")
        return fetch.items[0]
    
    @classmethod
    def _get_room_name_by_id(cls, id: str):
        return cls._get_room_record_by_id(id).room_name

    def get_building(self):
        """Return the building name for the room."""
        return self._get_room_record().building

    def get_reservations(self):
        """Return the reservation records for the room."""
        fetch = client.collection('grouprooms').get_list(1, 1, {'filter': self.room_filter})
        if fetch.total_items == 0:
            raise RoomNotFoundException(f"Room '{self.room_name}' not found.")
        reservation_filter = f"room.room_name='{self.room_name}'"
        return client.collection('reservations').get_list(1, self.MAX_RESERVATIONS, {'filter': reservation_filter}).items

    def get_room(self):
        """Return the  record."""
        return self._get_room_record()
    
    def get_room_id(self):
        """Return the room ID."""
        return self._get_room_record().room_id
    
    def get_room_item_id(self):
        """Return the room item ID."""
        return self._get_room_record().id
    
    @classmethod
    def get_all_rooms(cls):
        """Return all rooms in the database."""
        return client.collection('grouprooms').get_full_list()
    
    

class BuildingQuery:
    MAX_RESERVATIONS = 50

    def __init__(self, building: str):
        self.building = building
        
    def get_all_rooms_in_building(self):
        """Return all rooms in a building"""
        reservation_filter = f"building='{self.building}'"
        rooms = client.collection('grouprooms').get_list(1, self.MAX_RESERVATIONS, {'filter': reservation_filter}).items
        if not rooms:
            raise RoomNotFoundException(f"No building found called '{self.building}'")
        return rooms
    
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
        
        
        