import re
from fastapi import HTTPException, status
from exceptions.exceptions import InvalidInputException

def validate_input(input: str) -> str:
    if input == '':
        return input
    elif not re.match(r"^[a-zA-Z0-9\s_\-,åÅäÄöÖ]*$", input):
        raise InvalidInputException()
    return input
