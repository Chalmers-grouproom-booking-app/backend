from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
from typing import Optional

from app.automatisation.timeedit_api import TimeEditAPI
from app.exceptions.exceptions import AccountCreationError, AccountNotFoundError
from database.accounts import AccountPB 
from utils import format_cid_username
from hashlib import sha256

router = APIRouter(prefix="/account", tags=["Account"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/account/token")

class User(BaseModel):
    id: str
    token: str
    email: str
    display_name: str
    cookies: Optional[dict] = None

class DisplayNameUpdate(BaseModel):
    display_name: str = Field(..., min_length=1)

def generate_token(email: str, password: str) -> str:
    return sha256(f'{email}{password}'.encode()).hexdigest()

def get_user_by_token(token: str) -> User:
    account = AccountPB.get_account(token)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
        )
    return User(
        id = account.id,
        token=account.token,
        email=account.email,
        display_name=account.display_name,
        cookies=account.timeedit_cookies(),
    )

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    user = get_user_by_token(token)
    timeedit_test = TimeEditAPI(cookies=user.cookies).test()
    if not timeedit_test:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid TimeEdit session",
        )
    return user

@router.get("/me")
async def read_users_me(current_user: User = Depends(get_current_user)) -> User:
    return current_user

@router.put("/display_name")
async def update_display_name(update: DisplayNameUpdate, current_user: User = Depends(get_current_user)):
    account = AccountPB.get_account(current_user.token)
    if not account:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Account not found")
    if update.display_name == account.display_name:
        return {"message": "Display name is already set to this value"}
    if not AccountPB.is_display_name_unique(update.display_name):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Display name already exists")
    account.update_account(display_name=update.display_name)
    return {"message": "Display name updated successfully"}

from fastapi import HTTPException, status

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    email = format_cid_username(form_data.username)
    if not email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email format or missing email.")
    password = form_data.password

    try:
        timeedit = TimeEditAPI(email, password)
        cookies = timeedit.get_cookies()
    except Exception as e:  
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        ) from e

    token = generate_token(email, password)
    try:
        user = AccountPB.get_or_create_account(token, email, cookies=cookies)
    except AccountCreationError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Account creation failed: {str(e)}")
    except AccountNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Account not found: {str(e)}")
    except Exception as e:  # Catch any other unexpected exceptions
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred: {str(e)}")

    return {"access_token": token, "token_type": "bearer"}

@router.delete("/token")
async def logout(current_user: User = Depends(get_current_user)):
    try:
        account = AccountPB.get_account(current_user.token)
        account.update_account(cookies={})  
        return {"message": "Logged out successfully."}
    except AccountNotFoundError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Account not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))