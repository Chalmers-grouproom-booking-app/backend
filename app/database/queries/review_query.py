from typing import Optional
from app.automatisation.auto_get_reservations import fetch_group_room_id
from app.database.queries.account_querey import AccountQuery
from app.models.response import ReviewOutput
from app.database.queries.room_query import RoomQuery
from exceptions.exceptions import FastAPIParseError, InvalidInputException, RoomNotFoundException
from database.pb import client
from datetime import datetime
import random
import re

class ReviewQuery:
    
    MAX_REVIEWS = 50
    collection = client.collection('reviews')
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
        review_filter = f'id="{review_id}"'
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
        
    @classmethod
    def create_review( cls, account_id: str, room_name: str, review_score: float | int, review_text: str) -> None:
        if len(review_text) > 500:
            raise InvalidInputException("Review text must be 500 characters or less.")
        review_data = {
            "room": RoomQuery(room_name).get_room_item_id(),
            "review_score": review_score,
            "review_text": review_text if review_text else None,
            "account": AccountQuery(account_id).get_id(),
        }
        print(review_data)
        cls.collection.create(review_data)
            
        
    def _get_review_record(self, account_name: str):
        review_filter = f"room.room_name='{self.room_name}' && account_name='{account_name}'"
        review =  client.collection('reviews').get_list(1, 1, {'filter': review_filter})
        if review.total_items == 0:
            raise RoomNotFoundException(f"No review found for room '{self.room_name}' by this account")
        return review.items[0]
    
    @classmethod
    def get_account_review( cls, account_id: str) -> ReviewOutput:
        """Get all reviews for a room By account ID"""
        review  = cls.collection.get_list(1, cls.MAX_REVIEWS, {'filter': f"account.id='{account_id}'"})
        if review.total_items == 0:
            raise RoomNotFoundException(f"No review found for account '{account_id}'")
        record = review.items[0]
        return ReviewOutput(
            account_display_name=  AccountQuery(record.account).get_display_name(),
            created=record.created,
            updated=record.updated,
            room_name= RoomQuery._get_room_name_by_id( record.room ),
            review_score=record.review_score,
            review_text=record.review_text,
        )
    
    @classmethod
    def get_all_account_reviews(cls, account_id: str):
        """Get all reviews for a room"""
        review =  cls.collection.get_list(1, cls.MAX_REVIEWS, {'filter': f"account.id='{account_id}'"})
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
        reviews = cls.collection.get_list(1, cls.MAX_REVIEWS, {'filter': f"room.room_name='{room_name}'"})
        if reviews.total_items == 0:
            raise RoomNotFoundException(f"No reviews found for room '{room_name}'")
        return reviews.items
    
    @classmethod
    def delete_one_review(cls, review_id: int):
        """Delete a review"""
        review = ReviewQuery()._get_review_item_by_id(review_id)
        client.collection('reviews').delete(review.id)
       
    @classmethod 
    def put_review(cls, review_id: str, review_score: float | int , review_text: str) -> ReviewOutput:
        review = ReviewQuery()._get_review_item_by_id(review_id)
        review_data = {
            "review_score": review_score,
            "review_text": review_text if review_text else None,
        }
        client.collection('reviews').update(review.id, review_data)
        return ReviewOutput(**{
            "room_name": RoomQuery._get_room_name_by_id(review.room),
            "review_score": review_score,
            "review_text": review_text,
            "account_name": review.account_name,
            "review_id": review_id,
            "date": review.date
        })
        