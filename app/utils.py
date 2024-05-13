import re, os
from exceptions.exceptions import InvalidInputException
from database.encryption import get_encryption_test
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()

key = os.getenv('ENCRYPTION_KEY')
if not key:
    raise ValueError("ENCRYPTION_KEY is not set in the environment variables.")
cipher = Fernet(key)


def encrypt_data(data: str) -> str:
    """Encrypt data."""
    return cipher.encrypt(data.encode()).decode()

def decrypt_data(encrypted_data: str) -> str:
    """Decrypt data."""
    return cipher.decrypt(encrypted_data.encode()).decode()

def test_encryption_key():
    encrypted_chalmers = get_encryption_test()
    decrypted_chalmers = decrypt_data(encrypted_chalmers)
    if decrypted_chalmers != "chalmers":
        raise ValueError("Encryption key is invalid.")
    print("Encryption key is valid.")
    return True

def format_cid_username(username):
    if not re.match(r'^[\w.-]+(@[a-zA-Z\d.-]*\.[a-zA-Z]{2,})?$', username):
        return None
    match = re.match(r'^([\w.-]+)(@)?', username)
    if match:
        return f"{match.group(1)}@net.chalmers.se"
    else:
        return None

MAX_LENGTH = 50
def validate_input(input: str) -> str:
    if input == '':
        return input
    if len(input) > MAX_LENGTH:
        raise InvalidInputException(f"Input exceeds maximum length of {MAX_LENGTH} characters.")
    if not re.match(r"^[a-zA-Z0-9\s_\-,åÅäÄöÖ]*$", input):
        raise InvalidInputException(f"Invalid input: {input}")
    return input

def validate_input_V2(input: str) -> str:
    if input == '':
        return input
    if len(input) > MAX_LENGTH:
        raise InvalidInputException(f"Input exceeds maximum length of {MAX_LENGTH} characters.")
    if not re.match(r"^[a-zA-Z0-9\s_\-,|()åÅäÄöÖé]*$", input):
        raise InvalidInputException(f"Invalid input: {input}")
    return input

def validate_integer_input(input: int) -> int:
    # Check if input is of less than 20 characters
    if len(str(input)) > MAX_LENGTH:
        raise InvalidInputException(f"Input exceeds maximum length of {MAX_LENGTH} characters.")
    return input

def validate_float_input(input: float) -> float:
    # Check if input is of less than 20 characters
    if len(str(input)) > MAX_LENGTH:
        raise InvalidInputException(f"Input exceeds maximum length of {MAX_LENGTH} characters.")
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