from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from automatisation.timeedit_api import TimeEditAPI

from database.accounts import AccountPB
from hashlib import sha256

router = APIRouter(prefix="/account", tags=["Account"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/account/token")

class User(BaseModel):
    token: str
    email: str
    display_name: str
    timeedit_cookies: str = None

def generate_token(email: str, password: str):
    # Generates a SHA-256 hash as the token
    return sha256(f'{email}{password}'.encode()).hexdigest()

def get_user_by_token(token: str):
    try:
        account = AccountPB.get_account(token)
        return User(
            token=account.token,
            email=account.email,
            display_name=account.display_name,
            timeedit_cookies=account.timeedit_cookies
        )
    except Exception:
        return None

async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = get_user_by_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

@router.get("/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    email, password = form_data.username, form_data.password
    token = generate_token(email, password)
    try:
        # Try to login 
        timeedit = TimeEditAPI(email, password)
        cookies = timeedit.get_cookies()
        try:
            user = AccountPB.get_account(token)
            print( user.display_name )
            user.update(cookies=cookies)
        except Exception:
            user = AccountPB.create_account(token, email, cookies=cookies)
        finally:
            return {"access_token": token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
