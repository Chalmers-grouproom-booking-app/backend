import re
from fastapi import HTTPException, status

def validate_input(room_name: str) -> str:
    if not re.match(r"^[a-zA-Z0-9\s_-]*$", room_name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid input, try again >:("
        )
    return room_name
