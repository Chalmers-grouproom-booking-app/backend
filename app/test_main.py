from fastapi import FastAPI
from fastapi.testclient import TestClient
from main import app
from models.response import RoomModel

client = TestClient(app)

def test_get_all_rooms():
    response = client.get("/api/v1/all_rooms")
    assert response.status_code == 200
    assert isinstance(response.json()[4], RoomModel)
    # for room in response.json():
    #     assert isinstance(room, RoomModel)

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
    assert response.json() == {"detail": "Room not found"}
    
def test_get_room_info_invalid_input():
    response = client.get("/api/v1/room?input=#&!!**")
    assert response.status_code == 422
    assert response.json() == {"detail": "Invalid input"}

def test_search_db():
    response = client.get("/api/v1/search?input=Jupiter")
    assert response.status_code == 200
    assert len(response.json()) == 1
    
def test_get_reservation():
    response = client.get("/api/v1/room/reservation?input=Jupiter123")
    assert response.status_code == 200
    assert len(response.json()) == 1
 
def test_get_all_reservations():
    response = client.get("/api/v1/room/reservation/all?input=Jupiter123")
    assert response.status_code == 200
    assert len(response.json()) == 36
    


