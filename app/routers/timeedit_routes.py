import json
from fastapi import APIRouter, HTTPException, Header, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from automatisation.timeedit_api import TimeEditAPI
from exceptions.exceptions import ErrorResponse
from models.timeedit import Login, AllReservations
from utils import validate_email, validate_password

router = APIRouter(prefix="/timedit/api", tags=["Timedit API"])

def parse_cookies(cookies_str: str):
    try:
        cookies_str = cookies_str.replace('\\"', '"')
        cookies = json.loads(cookies_str)
        if not isinstance(cookies, dict):
            raise ValueError("Invalid cookie format")
        return cookies
    except (json.JSONDecodeError, ValueError) as e:
        raise HTTPException(status_code=400, detail="Invalid cookie data") from e

@router.post("/login", response_model=Login, responses={400: {"model": ErrorResponse}}, summary="Login to TimeEdit")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = validate_email(form_data.username)
    password = validate_password(form_data.password)
    try:
        timeedit = TimeEditAPI(username, password)
        cookies = timeedit.get_cookies()
        cookies_json = json.dumps(cookies)
        response = JSONResponse(content={"login": "success", "username": username, "cookies": cookies_json})
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/all_reservations", summary="Get all reservations", response_model=AllReservations, responses={400: {"model": ErrorResponse}})
async def get_all_reservations(x_cookies: str = Header(...)):
    cookies = parse_cookies(x_cookies)
    try:
        timeedit = TimeEditAPI(cookies=cookies)
        reservations_data = timeedit.get_all_my_reservations()
        all_reservations = AllReservations(reservations=reservations_data)
        return all_reservations
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/add_reservation", summary="Add a new reservation")
async def add_reservation(
    grouproom_id: str, date: str, starttime: str, endtime: str, x_cookies: str = Header(...)):
    cookies = parse_cookies(x_cookies)
    try:
        timeedit = TimeEditAPI(cookies=cookies)
        response = timeedit.reserve_grouproom(grouproom_id, date, starttime, endtime)
        return {"message": "Reservation added successfully", "details": response.text}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/delete_reservation/{reservation_id}", summary="Delete a reservation")
async def delete_reservation(reservation_id: str, x_cookies: str = Header(...)):
    cookies = parse_cookies(x_cookies)
    try:
        timeedit = TimeEditAPI(cookies=cookies)
        response = timeedit.delete_reservation(reservation_id)
        return {"message": "Reservation deleted successfully", "details": response.text}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/edit_reservation/{reservation_id}", summary="Edit an existing reservation")
async def edit_reservation(
    reservation_id: str, date: str, starttime: str, endtime: str, x_cookies: str = Header(...)):
    cookies = parse_cookies(x_cookies)
    try:
        timeedit = TimeEditAPI(cookies = cookies)
        response = timeedit.edit_reservation(reservation_id, date, starttime, endtime)
        return {"message": "Reservation edited successfully", "details": response.text}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

