from pydantic import BaseModel


class User(BaseModel):
    username: str


class UserRegister(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str
