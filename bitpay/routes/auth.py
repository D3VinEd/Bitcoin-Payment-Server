from fastapi import APIRouter, HTTPException
from fastapi.security import HTTPBasicCredentials
from bitpay.services.user import User

router = APIRouter()


@router.post("/register")
def register_user(username: str, password: str):
    """
    Register a new user
    :param username:
    :param password:
    :return:
    """
    try:
        User.register(username, password)
        return {"message": "User registered"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
def login(credentials: HTTPBasicCredentials):
    """
    Login a user
    :param credentials:
    :return:
    """
    try:
        User.authenticate(credentials)
        access_token = create_access_token(credentials.username)
        return {"access_token": access_token}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
