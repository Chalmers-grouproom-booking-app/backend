from fastapi import HTTPException, status
from pydantic import BaseModel
from typing import Optional

class ErrorResponse(BaseModel):
    message: str
    code: Optional[int] = None

class RoomsNotFoundException(HTTPException):
    def __init__(self, detail: str = "Rooms not found", code: int = 404):
        super().__init__(status_code=code, detail=detail)
        
class RoomNotFoundException(HTTPException):
    def __init__(self, detail: str = "Room not found", code: int = 404):
        super().__init__(status_code=code, detail=detail)
class InvalidInputException(HTTPException):
    def __init__(self, detail: str = "Invalid input", code: int = 422):
        super().__init__(status_code=code, detail=detail)

class ReservationsNotFoundException(HTTPException):
    def __init__(self, detail: str = "No reservations found", code: int = 404):
        super().__init__(status_code=code, detail=detail)  
