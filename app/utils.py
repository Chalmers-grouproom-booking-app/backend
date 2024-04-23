import re
from fastapi import HTTPException, status

def validate_input(input: str) -> str:
    if input == '':
        return input
    elif not re.match(r"^[a-zA-Z0-9\s_\-,åÅäÄöÖ]*$", input):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid input, try again >:("
        )
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