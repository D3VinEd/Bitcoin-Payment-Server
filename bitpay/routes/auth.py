from fastapi import APIRouter
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
    User.register(username, password)
    return {"message": "User registered"}

# Authentifizierung und Ausstellung eines JWT-Tokens
@router.post("/login")
def login(credentials: HTTPBasicCredentials):
    """
    Login a user
    :param credentials:
    :return:
    """
    User.authenticate(credentials)
    access_token = create_access_token(credentials.username)
    return {"access_token": access_token}

# Geschützte Route