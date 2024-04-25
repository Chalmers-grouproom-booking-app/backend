from fastapi.testclient import TestClient
from main import app
from models.response import ReservationModel, RoomModel, SearchModel
from typing import List, Dict, Any

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
        "longitude": 0,
        "latitude": 0,
        "entrance_latitude": 0,
        "entrance_longitude": 0,
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
    response = client.get("/api/v1/room?input=#&!!**")
    assert response.status_code == 422
    assert response.json() == {"detail": "Invalid input: #&!!**"}

def test_get_room_info_max_length_input():
    response = client.get("/api/v1/room?input=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    assert response.status_code == 422
    assert response.json() == {"detail": "Input exceeds maximum length of 15 characters."}

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
    response = client.get("/api/v1/search?input=#&!!**")
    assert response.status_code == 422
    assert response.json() == {"detail": "Invalid input: #&!!**"}

def test_search_db_max_length_input():
    response = client.get("/api/v1/search?input=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    assert response.status_code == 422
    assert response.json() == {"detail": "Input exceeds maximum length of 15 characters."}
    
    
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
    assert response.json() == {"detail": "No reservations found for room 'nonexistent'"}
    
def test_get_reservation_invalid_input():
    response = client.get("/api/v1/room/reservation?input=#&!!**")
    assert response.status_code == 422
    assert response.json() == {"detail": "Invalid input: #&!!**"}

def test_get_reservation_max_length_input():
    response = client.get("/api/v1/room/reservation?input=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    assert response.status_code == 422 
    assert response.json() == {"detail": "Input exceeds maximum length of 15 characters."}
    
    
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
    assert response.json() == {"detail": "No reservations found for room 'nonexistent'"}
    
def test_get__all_reservation_invalid_input():
    response = client.get("/api/v1/room/reservation?input=#&!!**")
    assert response.status_code == 422
    assert response.json() == {"detail": "Invalid input: #&!!**"}

def test_get__all_reservation_max_length_input():
    response = client.get("/api/v1/room/reservation?input=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    assert response.status_code == 422
    assert response.json() == {"detail": "Input exceeds maximum length of 15 characters."}



