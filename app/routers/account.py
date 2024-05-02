from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
from typing import Optional

from app.automatisation.timeedit_api import TimeEditAPI
from app.exceptions.exceptions import AccountNotFoundError
from database.accounts import AccountPB 
from utils import format_cid_username
from hashlib import sha256

router = APIRouter(prefix="/account", tags=["Account"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/account/token")

class User(BaseModel):
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

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    email = format_cid_username(form_data.username)
    if not email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email")
    password = form_data.password
    token = generate_token(email, password)
    cookies = TimeEditAPI(email, password).get_cookies()
    user = AccountPB.get_or_create_account(token, email, cookies=cookies)
    return {"access_token": token, "token_type": "bearer"}

@router.delete("/token")
async def logout(current_user: User = Depends(get_current_user)):
    try:
        account = AccountPB.get_account(current_user.token)
        account.update_account(cookies={})  # This sets the cookies to an empty dictionary, signaling a logout.
        return {"message": "Logged out successfully."}
    except AccountNotFoundError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Account not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))