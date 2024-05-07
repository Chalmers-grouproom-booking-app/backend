from fastapi.testclient import TestClient
from main import app
from models.response import BookedModel, BuildingModel, ReservationModel, ReviewOutput, RoomModel, SearchModel
from typing import Dict, Any
from utils import MAX_LENGTH


client = TestClient(app)

TEST_REV_ID = ""

def validate_review_structure(review: Dict[str, Any]) -> bool:
    try:
        ReviewOutput(**review)
        return True
    except ValueError:
        return False

# create review tests
def test_create_review():
    response = client.post("/review/api/create-review", json={"room_name": "SB-G501", "review_score": 4, "review_text": "This is for testing purposes"})
    assert response.status_code == 200
    assert response.json() == {"message": "Review created successfully."}

# Get all reviews for room tests
def test_get_all_reviews_for_room():
    response = client.get("/review/api/room-reviews?input=SB-G501")
    assert response.status_code == 200
    reviews = response.json()
    for review in reviews:
        assert validate_review_structure(review)
        
def test_get_all_reviews_for_nonexistent_room():
    response = client.get("/review/api/room-reviews?input=nonexistent")
    assert response.status_code == 404
    assert response.json() == {"detail":"No reviews found for room 'nonexistent'"}
    
def test_get_all_reviews_for_room_invalid_input():
    response = client.get("/review/api/room-reviews", params={"input": "#&!!**"})
    assert response.status_code == 422
    assert response.json() == {"detail": "Invalid input: #&!!**"}
    
def test_get_all_reviews_for_room_max_length():
    response = client.get("/review/api/room-reviews?input=" + "a" * (MAX_LENGTH + 1))
    assert response.status_code == 422
    assert response.json() == {"detail": f"Input exceeds maximum length of {MAX_LENGTH} characters."}

# Get all reviews
def test_get_all_reviews():
    response = client.get("/review/api/all-reviews")
    assert response.status_code == 200
    reviews = response.json()
    for review in reviews:
        assert validate_review_structure(review)

# Get average room review score
def test_get_average_room_review_score():
    response = client.get("/review/api/room-average-score?input=SB-G501")
    assert response.status_code == 200
    assert response.json() == {"average_score": 4}
    
def test_get_average_room_review_score_nonexistent_room():
    response = client.get("/review/api/room-average-score?input=nonexistent")
    assert response.status_code == 404
    assert response.json() == {"detail": "No reviews found for room 'nonexistent'"}
    
def test_get_average_room_review_score_invalid_input():
    response = client.get("/review/api/room-average-score", params={"input": "#&!!**"})
    assert response.status_code == 422
    assert response.json() == {"detail": "Invalid input: #&!!**"}

def test_get_average_room_review_score_max_length():
    response = client.get("/review/api/room-average-score?input=" + "a" * (MAX_LENGTH + 1))
    assert response.status_code == 422
    assert response.json() == {"detail": f"Input exceeds maximum length of {MAX_LENGTH} characters."}

# Get my review for room tests
def test_get_my_review_for_room():
    response = client.get("/review/api/my-room-review?room_name=SB-G501")
    #
    assert response.status_code == 200
    assert validate_review_structure(response.json())

# Delete review tests
def test_delete_review():
    response = client.delete("/review/api/delete-review?input=SB-G501")
    assert response.status_code == 200
    assert response.json() == {"message": "Review deleted successfully."}