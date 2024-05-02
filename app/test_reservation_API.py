from fastapi.testclient import TestClient
from main import app
from models.response import BookedModel, BuildingModel, ReservationModel, ReviewOutput, RoomModel, SearchModel
from typing import Dict, Any
from utils import MAX_LENGTH


client = TestClient(app)

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