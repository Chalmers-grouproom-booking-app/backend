from fastapi import APIRouter, HTTPException, Depends
from routers.account import User, get_current_user
from automatisation.timeedit_api import TimeEditAPI
from exceptions.exceptions import ErrorResponse, AccountNotFoundError
from models.timeedit import  AllReservations

router = APIRouter(prefix="/timedit/api", tags=["Timedit API"])

async def get_timeedit_api(user: User = Depends(get_current_user)):
    try:
        return TimeEditAPI(cookies= user.cookies )
    except AccountNotFoundError:
        raise HTTPException(status_code=400, detail="Invalid or expired authentication token")

@router.get("/all_reservations", summary="Get all reservations", response_model=AllReservations, responses={400: {"model": ErrorResponse}})
async def get_all_reservations(timeedit_api: TimeEditAPI = Depends(get_timeedit_api)):
    try:
        reservations_data = timeedit_api.get_all_my_reservations()
        all_reservations = AllReservations(reservations=reservations_data)
        return all_reservations
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/add_reservation", summary="Add a new reservation")
async def add_reservation(grouproom_id: str, date: str, starttime: str, endtime: str, timeedit_api: TimeEditAPI = Depends(get_timeedit_api)):
    try:
        response = timeedit_api.reserve_grouproom(grouproom_id, date, starttime, endtime)
        return {"message": "Reservation added successfully", "details": response.text}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/delete_reservation/{reservation_id}", summary="Delete a reservation")
async def delete_reservation(reservation_id: str, timeedit_api: TimeEditAPI = Depends(get_timeedit_api)):
    try:
        response = timeedit_api.delete_reservation(reservation_id)
        return {"message": "Reservation deleted successfully", "details": response.text}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/edit_reservation/{reservation_id}", summary="Edit an existing reservation")
async def edit_reservation(reservation_id: str, date: str, starttime: str, endtime: str, timeedit_api: TimeEditAPI = Depends(get_timeedit_api)):
    try:
        response = timeedit_api.edit_reservation(reservation_id, date, starttime, endtime)
        return {"message": "Reservation edited successfully", "details": response.text}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
