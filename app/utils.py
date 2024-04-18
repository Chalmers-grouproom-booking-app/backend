import re
from fastapi import HTTPException, status

def validate_input(input_string: str) -> str:
    if not re.match(r"^[a-zA-Z0-9\s_-]*$", input_string):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid input, try again :)"
        )
    return input_string