from fastapi import APIRouter, HTTPException, Request
from bitpay.services.user import User
from bitpay.services.authentication import Auth
from bitpay.models import UserRegister, UserLogin
from slowapi import Limiter
from slowapi.util import get_remote_address


router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.post("/register")
@limiter.limit("2/minute", error_message="Too many requests")
def register_user(user: UserRegister, request: Request):
    try:
        user_instance = User(user.username)
        user_instance.register(user.password)
        return {"message": "User registered"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
@limiter.limit("5/minute", error_message="Too many requests")
def login(user: UserLogin, request: Request):
    try:
        user_instance = User(user.username)
        user_instance.login(user.password)
        access_token = Auth.create_access_token(user.username)
        return {"access_token": access_token}
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid credentials")
