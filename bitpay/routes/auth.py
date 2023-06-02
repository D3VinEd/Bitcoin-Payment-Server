from fastapi import APIRouter, HTTPException
from fastapi.security import HTTPBasicCredentials
from bitpay.services.user import User
from bitpay.services.authentication import Auth
from pydantic import BaseModel
router = APIRouter()


class UserRegister(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


@router.post("/register")
def register_user(user: UserRegister):  # user parameter is of type UserRegister now
    try:
        user_instance = User(user.username)
        user_instance.register(user.password)
        return {"message": "User registered"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
def login(user: UserLogin):  # user parameter is of type UserLogin now
    try:
        user_instance = User(user.username)
        user_instance.login(user.password)
        access_token = Auth.create_access_token(user.username)
        return {"access_token": access_token}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))