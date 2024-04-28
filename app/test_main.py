from fastapi.testclient import TestClient
from main import app
from models.response import BookedModel, BuildingModel, ReservationModel, ReviewOutput, RoomModel, SearchModel
from typing import Dict, Any
from utils import MAX_LENGTH

client = TestClient(app)

# Helper functions
def validate_room_structure(room: Dict[str, Any]) -> bool:
    try:
        RoomModel(**room)
        return True
    except ValueError:
        return False

def validate_search_structure(search: Dict[str, Any]) -> bool: 
    try:
        SearchModel(**search)
        return True
    except ValueError:
        return False
    
def validate_reservation_structure(reservation: Dict[str, Any]) -> bool:
    try:
        ReservationModel(**reservation)
        return True
    except ValueError:
        return False
    
def validate_booked_structure(booked: Dict[str, Any]) -> bool:
    try:
        BookedModel(**booked)
        return True
    except ValueError:
        return False

def validate_building_structure(building: Dict[str, Any]) -> bool:
    try:
        BuildingModel(**building)
        return True
    except ValueError:
        return False
    
def validate_review_structure(review: Dict[str, Any]) -> bool:
    try:
        ReviewOutput(**review)
        return True
    except ValueError:
        return False


# Get all rooms tests
def test_get_all_rooms():
    response = client.get("/api/v1/all_rooms")
    assert response.status_code == 200
    for room in response.json():
        assert validate_room_structure(room)

# Get room tests
def test_get_room_info():
    response = client.get("/api/v1/room?input=Svea238")
    assert response.status_code == 200
    assert response.json() == {
        "room_name": "Svea238",
        "room_size": 10,
        "building": "Svea",
        "campus": "Lindholmen",
        "equipment": "Whiteboard",
        "longitude": 11.936445758795186,
        "latitude": 57.70633975366362,
        "entrance_latitude": 57.70633975366362,
        "entrance_longitude": 11.936445758795186,
        "description": "",
        "first_come_first_served": False,
        "floor_level": 0,
        "stair": ""
    }

def test_get_nonexistent_room_info():
    response = client.get("/api/v1/room?input=nonexistent")
    assert response.status_code == 404
    assert response.json() == {"detail": "Room 'nonexistent' not found."}
    
def test_get_room_info_invalid_input():
    response = client.get("/api/v1/room", params={"input": "#&!!**"})
    print(response.json())
    assert response.status_code == 422
    assert response.json() == {"detail": "Invalid input: #&!!**"}

def test_get_room_info_max_length_input():
    response = client.get("/api/v1/room?input=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    assert response.status_code == 422
    assert response.json() == {"detail": f"Input exceeds maximum length of {MAX_LENGTH} characters."}

# Search tests
def test_search_db():
    response = client.get("/api/v1/search?input=Jupiter")
    assert response.status_code == 200
    assert validate_search_structure(response.json())

def test_search_db_no_results():
    response = client.get("/api/v1/search?input=nonexistent")
    assert response.status_code == 404
    assert response.json() == {"detail": "No rooms found with the search term 'nonexistent'"}

def test_search_db_invalid_input():
    response = client.get("/api/v1/search", params={"input": "#&!!**"})
    assert response.status_code == 422
    assert response.json() == {"detail": "Invalid input: #&!!**"}

def test_search_db_max_length_input():
    response = client.get("/api/v1/search?input=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    assert response.status_code == 422
    assert response.json() == {"detail": f"Input exceeds maximum length of {MAX_LENGTH} characters."}
    
    
# Get reservation tests
def test_get_reservation():
    response = client.get("/api/v1/room/reservation?input=Jupiter123")
    if response.status_code == 404:
        assert response.json() == {"detail": "No reservations found for room 'Jupiter123'"}
    elif response.status_code == 200:
        for reservation in response.json():
            assert validate_reservation_structure(reservation)
    else:
        assert False
        
def test_get_reservation_no_results():
    response = client.get("/api/v1/room/reservation?input=nonexistent")
    assert response.status_code == 404
    assert response.json() == {'detail': "Room 'nonexistent' not found."}
    
def test_get_reservation_invalid_input():
    response = client.get("/api/v1/room/reservation", params={"input": "#&!!**"})
    assert response.status_code == 422
    assert response.json() == {"detail": "Invalid input: #&!!**"}

def test_get_reservation_max_length_input():
    response = client.get("/api/v1/room/reservation?input=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    assert response.status_code == 422 
    assert response.json() == {"detail": f"Input exceeds maximum length of {MAX_LENGTH} characters."}
    
    
# Get all reservations tests
def test_get_all_reservations():
    response = client.get("/api/v1/room/reservation?input=Svea238")
    if response.status_code == 404:
        assert response.json() == {"detail": "No reservations found for room 'Svea238'"}
    elif response.status_code == 200:
        for reservation in response.json():
            assert validate_reservation_structure(reservation)
    else:
        assert False
        
def test_get__all_reservation_no_results():
    response = client.get("/api/v1/room/reservation?input=nonexistent")
    assert response.status_code == 404
    assert response.json() == {'detail': "Room 'nonexistent' not found."}
    
def test_get__all_reservation_invalid_input():
    response = client.get("/api/v1/room/reservation", params={"input": "#&!!**"})
    assert response.status_code == 422
    assert response.json() == {"detail": "Invalid input: #&!!**"}

def test_get__all_reservation_max_length_input():
    response = client.get("/api/v1/room/reservation?input=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    assert response.status_code == 422
    assert response.json() == {"detail": f"Input exceeds maximum length of {MAX_LENGTH} characters."}
    
# Get room booked tests
def test_get_room_booked():
    response = client.get("/api/v1/room/booked?input=Svea238")
    assert response.status_code == 200
    if response.json() == [{"booked": False}] or response.json() == [{"booked": True}]:
        assert validate_booked_structure(response.json()[0])
        assert True
    else:
        assert False

def test_get_room_booked_no_results():
    response = client.get("/api/v1/room/booked?input=nonexistent")
    assert response.status_code == 404
    assert response.json() == {"detail": "Room 'nonexistent' not found."}

def test_get_room_booked_invalid_input():
    response = client.get("/api/v1/room/booked", params={"input": "#&!!**"})
    assert response.status_code == 422
    assert response.json() == {"detail": "Invalid input: #&!!**"}

def test_get_room_booked_max_length_input():
    response = client.get("/api/v1/room/booked?input=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    assert response.status_code == 422
    assert response.json() == {"detail": f"Input exceeds maximum length of {MAX_LENGTH} characters."}
    
# Get building color tests
def test_get_building_booked_percentage():
    response = client.get("/api/v1/building/percentage?input=Svea")
    assert response.status_code == 200
    for building in response.json():
        assert validate_building_structure(building)

def test_get_building_booked_percentage_no_results():
    response = client.get("/api/v1/building/percentage?input=nonexistent")
    assert response.status_code == 404
    assert response.json() == {"detail": "No building found called 'nonexistent'"}
    
def test_get_building_booked_percentage_invalid_input():
    response = client.get("/api/v1/building/percentage", params={"input": "#&!!**"})
    assert response.status_code == 422
    assert response.json() == {"detail": "Invalid input: #&!!**"}
    
def test_get_building_booked_percentage_max_length_input():
    response = client.get("/api/v1/building/percentage?input=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    assert response.status_code == 422
    assert response.json() == {"detail": f"Input exceeds maximum length of {MAX_LENGTH} characters."}
    
# Get all reviews tests
def test_get_all_reviews():
    response = client.get("/api/v1/review/all")
    assert response.status_code == 200
    for review in response.json():
        assert validate_review_structure(review)

# Get all reviews for room tests
def test_get_all_reviews_for_room():
    response = client.get("/api/v1/review/room/all?input=Jupiter123")
    if response.status_code == 404:
        assert response.json() == {"detail": "No reviews found for room 'Jupiter123'"}
    elif response.status_code == 200:
        for review in response.json():
            assert validate_review_structure(review)
    else:
        assert False

def test_get_all_reviews_for_room_no_results():
    response = client.get("/api/v1/review/room/all?input=nonexistent")
    assert response.status_code == 404
    assert response.json() == {"detail": "Room 'nonexistent' not found."}

def test_get_all_reviews_for_room_invalid_input():
    response = client.get("/api/v1/review/room/all", params={"input": "#&!!**"})
    assert response.status_code == 422
    assert response.json() == {"detail": "Invalid input: #&!!**"}
    
def test_get_all_reviews_for_room_max_length_input():
    response = client.get("/api/v1/review/room/all?input=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    assert response.status_code == 422
    assert response.json() == {"detail": f"Input exceeds maximum length of {MAX_LENGTH} characters."}
    
# Get review by review id tests
def test_get_review_by_review_id_no_results():
    response = client.get("/api/v1/review/id?review_id=1000")
    assert response.status_code == 404
    assert response.json() == {"detail": "No review found with review ID '1000'"}
    
def test_get_review_by_review_id_invalid_input():
    response = client.get("/api/v1/review/id", params={"review_id": "#&!!**"})
    assert response.status_code == 422
    #FIX ERROR MESSAGE
        
def test_get_review_by_review_id_max_length_input():
    response = client.get("/api/v1/review/id?review_id=1111111111111111111111111111111111111111111111111111111111111111111111111111111")
    assert response.status_code == 422
    assert response.json() == {"detail": f"Input exceeds maximum length of {MAX_LENGTH} characters."}

    

        
