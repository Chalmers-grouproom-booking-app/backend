import re
from exceptions.exceptions import InvalidInputException

def validate_input(input: str) -> str:
    if input == '':
        return input
    if len(input) > 15:
        raise InvalidInputException("Input exceeds maximum length of 15 characters.")
    if not re.match(r"^[a-zA-Z0-9\s_\-,åÅäÄöÖ]*$", input):
        raise InvalidInputException(f"Invalid input: {input}")
    return input
