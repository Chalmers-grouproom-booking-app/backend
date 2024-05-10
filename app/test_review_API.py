from fastapi.testclient import TestClient
import pytest
from main import app
from models.response import ReviewOutput
from typing import Dict, Any
from utils import MAX_LENGTH
import os
from dotenv import load_dotenv, dotenv_values 
load_dotenv() 

TEST_REVIEW_ID = ""

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
      yield c

def test_user():
    return {"username": f"{os.getenv("CID_USERNAME")}", "password": f"{os.getenv("CID_PASSWORD")}"}

def test_login(client):
    response = client.post("/account/token", data=test_user())
    assert response.status_code == 200
    token = response.json()["access_token"]
    return token  # Return only the token

def get_test_review_id(client):
    token = test_login(client)
    response = client.get("/review/api/my-room-review?room_name=SB-G501", headers={"Authorization": f"Bearer {token}"})
    return response.json()["id"]

def validate_review_structure(review: Dict[str, Any]) -> bool:
    try:
        ReviewOutput(**review)
        return True
    except ValueError:
        return False

# create review tests
def test_create_review(client):  # Modified here
    token = test_login(client)
    response = client.post("/review/api/create-review", json={"room_name": "SB-G501", "review_score": 4, "review_text": "This is for testing purposes"}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == {'message': 'Review successfully submitted'}

# Get all reviews for room tests
def test_get_all_reviews_for_room(client):  # Modified here
    response = client.get("/review/api/room-reviews?input=SB-G501")
    assert response.status_code == 200
    reviews = response.json()
    for review in reviews:
        assert validate_review_structure(review)
        
def test_get_all_reviews_for_nonexistent_room(client):  # Modified here
    response = client.get("/review/api/room-reviews?input=nonexistent")
    assert response.status_code == 404
    assert response.json() == {"detail": "Room 'nonexistent' not found."}
    
def test_get_all_reviews_for_room_invalid_input(client):  # Modified here
    response = client.get("/review/api/room-reviews", params={"input": "#&!!**"})
    assert response.status_code == 422
    assert response.json() == {"detail": "Invalid input: #&!!**"}
    
def test_get_all_reviews_for_room_max_length(client):  # Modified here
    response = client.get("/review/api/room-reviews?input=" + "a" * (MAX_LENGTH + 1))
    assert response.status_code == 422
    assert response.json() == {"detail": f"Input exceeds maximum length of {MAX_LENGTH} characters."}

# Get all reviews
def test_get_all_reviews(client):  # Modified here
    response = client.get("/review/api/all-reviews")
    assert response.status_code == 200
    reviews = response.json()
    for review in reviews:
        assert validate_review_structure(review)

# Get average room review score
def test_get_average_room_review_score(client):  # Modified here
    response = client.get("/review/api/room-average-score?input=SB-G501")
    assert response.status_code == 200
    assert response.json() == {"average_score": 4}
    
def test_get_average_room_review_score_nonexistent_room(client):  # Modified here
    response = client.get("/review/api/room-average-score?input=nonexistent")
    assert response.status_code == 404
    assert response.json() == {"detail": "Room 'nonexistent' not found."}
    
def test_get_average_room_review_score_invalid_input(client):  # Modified here
    response = client.get("/review/api/room-average-score", params={"input": "#&!!**"})
    assert response.status_code == 422
    assert response.json() == {"detail": "Invalid input: #&!!**"}

def test_get_average_room_review_score_max_length(client):  # Modified here
    response = client.get("/review/api/room-average-score?input=" + "a" * (MAX_LENGTH + 1))
    assert response.status_code == 422
    assert response.json() == {"detail": f"Input exceeds maximum length of {MAX_LENGTH} characters."}

# Get my review for room tests
def test_get_my_review_for_room(client):
    token = test_login(client)
    response = client.get("/review/api/my-room-review?room_name=SB-G501", headers={"Authorization": f"Bearer {token}"})
    TEST_REVIEW_ID = response.json()["id"]
    assert response.status_code == 200
    assert validate_review_structure(response.json())
    
def test_get_my_review_for_nonexistent_room(client):
    token = test_login(client)
    response = client.get("/review/api/my-room-review?room_name=nonexistent", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Room 'nonexistent' not found."}

def test_get_my_review_for_room_invalid_input(client):
    token = test_login(client)
    response = client.get("/review/api/my-room-review", params={"room_name": "#&!!**"}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 422
    assert response.json() == {"detail": "Invalid input: #&!!**"}

def test_get_my_review_for_room_max_length(client):
    token = test_login(client)
    response = client.get("/review/api/my-room-review?room_name=" + "a" * (MAX_LENGTH + 1), headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 422
    assert response.json() == {"detail": f"Input exceeds maximum length of {MAX_LENGTH} characters."}
    
# Get my reviews tests
def test_get_my_reviews(client):
    token = test_login(client)
    response = client.get("/review/api/my-reviews", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    reviews = response.json()
    for review in reviews:
        assert validate_review_structure(review)

# Update review tests
def test_update_review(client):
    token = test_login(client)
    review = get_test_review_id(client)
    response = client.put(f"/review/api/update-review/{review}", params={"review_score": 5, "review_text": "This is for testing purposes"}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == {'message': 'Review successfully updated'}

# Delete review tests
def test_delete_review(client):
    token = test_login(client)
    review = get_test_review_id(client)
    response = client.delete(f"/review/api/delete-review/{review}?review_score=5", params={'review_text': 'This text had been changed'},  headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == {'message': 'Review successfully deleted'}
    
def test_delete_nonexistent_review(client):
    token = test_login(client)
    response = client.delete("/review/api/delete-review/nonexistent", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404
    assert response.json() == {'detail': "No review found with review ID 'nonexistent'"}

def test_delete_review_invalid_input(client):
    token = test_login(client)
    response = client.delete("/review/api/delete-review/%20%23%26%21%21%2A%2A" , headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 422
    assert response.json() == {'detail': 'Invalid input:  #&!!**'}
    
def test_delete_review_max_length(client):
    token = test_login(client)
    response = client.delete("/review/api/delete-review/" + "a" * (MAX_LENGTH + 1), headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 422
    assert response.json() == {"detail": f"Input exceeds maximum length of {MAX_LENGTH} characters."}
    
    
