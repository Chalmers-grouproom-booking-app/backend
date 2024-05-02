from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

from app.automatisation.timeedit_api import TimeEditAPI
from database.accounts import AccountPB, AccountNotFoundError, AccountCreationError, InvalidDataError
from hashlib import sha256

router = APIRouter(prefix="/account", tags=["Account"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/account/token")

class User(BaseModel):
    token: str
    email: str
    display_name: str
    cookies: dict = None

def generate_token(email: str, password: str):
    # Generates a SHA-256 hash as the token
    return sha256(f'{email}{password}'.encode()).hexdigest()

def get_user_by_token(token: str) -> User:
    try:
        account = AccountPB.get_account(token)
        return User(
            token=account.token,
            email=account.email,
            display_name=account.display_name,
            cookies=account.timeedit_cookies()
        )
    except AccountNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    return get_user_by_token(token)

@router.get("/me")
async def read_users_me(current_user: User = Depends(get_current_user)) -> User:
    return current_user

# make router to update account display name
@router.put("/display_name")
async def update_display_name(display_name: str, current_user: User = Depends(get_current_user)):
    try:
        account = AccountPB.get_account(current_user.token)
        if (display_name == account.display_name):
            return {"message": "Display name is already set to this value"}
        if (not AccountPB.is_display_name_unique(display_name)):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Display name already exists")
        account.update_account(display_name=display_name)
        return {"message": "Display name updated successfully"}
    except AccountNotFoundError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Account not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    email, password = form_data.username, form_data.password
    token = generate_token(email, password)
    try:
        timeedit = TimeEditAPI(email, password)
        cookies = timeedit.get_cookies()
        try:
            user = AccountPB.get_account(token)
            user.update_account(cookies=cookies)
        except AccountNotFoundError:
            try:
                user = AccountPB.create_account(token, email, cookies=cookies)
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Account creation failed: {str(e)}")
        return {"access_token": token, "token_type": "bearer"}
    except Exception as e:
        print(f"Login failed: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
