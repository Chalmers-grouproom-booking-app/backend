from typing import Annotated

from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from hashlib import sha256

from exceptions.exceptions import AccountNotFoundException

router = APIRouter( prefix="/account", tags=["Account"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/account/token")

fake_users  =  []

class User(BaseModel):
    token: str
    email: str
    display_name: str


def generate_token(email, password):
    return sha256(f'{email}{password}'.encode()).hexdigest()

def get_user(token):
    for user in fake_users:
        if user.token == token:
            return user        
    return None

def fake_decode_token(token):
    user = get_user(token)
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    email, password = form_data.username, form_data.password
    token = generate_token( email, password)
    """ if timedit login successfull"""    
    # if timeedit.login(form_data.username, form_data.password):
    
    # if user not in  database create
    if not get_user(token):
        fake_users.append(User(token=token, email=form_data.username, display_name="John Doe"))

    # return token
    return {"access_token":  token, "token_type": "bearer"}


@router.get("/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return current_user