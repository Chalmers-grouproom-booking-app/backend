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


def validate_email(email: str):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        raise ValueError("Invalid email address.")
    return email

def validate_password(password: str):
    if re.match(r"[\s]", password):
        raise ValueError("Invalid password. Whitespace is not allowed.")
    if len(password) < 8:
        raise ValueError("Invalid password. Password must be at least 8 characters long.")
    return password