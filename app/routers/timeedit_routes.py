import json

from fastapi import APIRouter, Depends, HTTPException,Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from automatisation.timeedit_api import TimeEditAPI
from exceptions.exceptions import ErrorResponse
from models.timeedit import Login, AllReservations
from utils import validate_email, validate_password

router = APIRouter(prefix="/timedit/api", tags=["Timedit API"])


async def get_timeedit_cookies(request: Request):
    timeedit_cookies = request.cookies.get("timeedit_cookies")
    if not timeedit_cookies:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        cookies_dict = json.loads(timeedit_cookies)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid cookie format")
    return cookies_dict

@router.post("/login", response_model=Login, responses={400: {"model": ErrorResponse}}, summary="Login to TimeEdit")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = validate_email(form_data.username)
    password = validate_password(form_data.password)
    try:
        timeedit = TimeEditAPI(username, password)
        timeedit_cookies = timeedit.get_cookies() 
        serialized_cookies = json.dumps(timeedit_cookies)
        response = JSONResponse(content={"login": "success", "username": username})
        response.set_cookie(key="timeedit_cookies", value=serialized_cookies, httponly=False, secure=True, samesite='None')
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/all_reservations", summary="Get all reservations", response_model=AllReservations, responses={400: {"model": ErrorResponse}})
async def get_all_reservations(cookies_dict: dict = Depends(get_timeedit_cookies)):
    try:
        timeedit = TimeEditAPI(cookies=cookies_dict)
        reservations_data = timeedit.get_all_my_reservations()
        all_reservations = AllReservations(reservations=reservations_data)
        return all_reservations
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



@router.post("/add_reservation", summary="Add a new reservation")
async def add_reservation(
    grouproom_id: str,
    date: str,
    starttime: str,
    endtime: str,
    cookies_dict: dict = Depends(get_timeedit_cookies)):
    try:
        timeedit = TimeEditAPI(cookies=cookies_dict)
        response = timeedit.reserve_grouproom(grouproom_id, date, starttime, endtime)
        return {"message": "Reservation added successfully", "details": response.text}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    
@router.delete("/delete_reservation/{reservation_id}", summary="Delete a reservation")
async def delete_reservation(reservation_id: str, cookies_dict: dict = Depends(get_timeedit_cookies)):
    try:
        timeedit = TimeEditAPI(cookies=cookies_dict)
        response = timeedit.delete_reservation(reservation_id)
        return {"message": "Reservation deleted successfully", "details": response.text}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/edit_reservation/{reservation_id}", summary="Edit an existing reservation")
async def edit_reservation(
    reservation_id: str,
    date: str,
    starttime: str,
    endtime: str,
    cookies_dict: dict = Depends(get_timeedit_cookies)):
    try:
        timeedit = TimeEditAPI(cookies=cookies_dict)
        response = timeedit.edit_reservation(reservation_id, date, starttime, endtime)
        return {"message": "Reservation edited successfully", "details": response.text}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



@router.get("/logout", summary="Logout from TimeEdit")
async def logout():
    response = JSONResponse(content={"logout": "success"})
    response.delete_cookie("timeedit_cookies")
    return response
