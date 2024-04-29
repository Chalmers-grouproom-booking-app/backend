from fastapi.testclient import TestClient
from main import app
from models.response import BookedModel, BuildingModel, ReservationModel, ReviewOutput, RoomModel, SearchModel
from typing import Dict, Any
from utils import MAX_LENGTH


client = TestClient(app)

def validate_review_structure(review: Dict[str, Any]) -> bool:
    try:
        ReviewOutput(**review)
        return True
    except ValueError:
        return False

# Get all reviews tests
def test_get_all_reviews():
    response = client.get("/review/api/all")
    assert response.status_code == 200
    for review in response.json():
        assert validate_review_structure(review)

# Get all reviews for room tests
def test_get_all_reviews_for_room():
    response = client.get("/review/api/room/all?input=Jupiter123")
    if response.status_code == 404:
        assert response.json() == {"detail": "No reviews found for room 'Jupiter123'"}
    elif response.status_code == 200:
        for review in response.json():
            assert validate_review_structure(review)
    else:
        assert False

def test_get_all_reviews_for_room_no_results():
    response = client.get("/review/api/room/all?input=nonexistent")
    assert response.status_code == 404
    assert response.json() == {"detail": "Room 'nonexistent' not found."}

def test_get_all_reviews_for_room_invalid_input():
    response = client.get("/review/api/room/all", params={"input": "#&!!**"})
    assert response.status_code == 422
    assert response.json() == {"detail": "Invalid input: #&!!**"}
    
def test_get_all_reviews_for_room_max_length_input():
    response = client.get("/review/api/room/all?input=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    assert response.status_code == 422
    assert response.json() == {"detail": f"Input exceeds maximum length of {MAX_LENGTH} characters."}
    
# Get review by review id tests
def test_get_review_by_review_id_no_results():
    response = client.get("/review/api/id?review_id=1000")
    assert response.status_code == 404
    assert response.json() == {"detail": "No review found with review ID '1000'"}
    
def test_get_review_by_review_id_invalid_input():
    response = client.get("/review/api/id", params={"review_id": "#&!!**"})
    assert response.status_code == 422
    #FIX ERROR MESSAGE
        
def test_get_review_by_review_id_max_length_input():
    response = client.get("/review/api/id?review_id=1111111111111111111111111111111111111111111111111111111111111111111111111111111")
    assert response.status_code == 422
    assert response.json() == {"detail": f"Input exceeds maximum length of {MAX_LENGTH} characters."}
