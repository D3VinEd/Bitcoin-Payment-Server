import redis
import bcrypt
import jwt
from fastapi import HTTPException
from fastapi.security import HTTPBasicCredentials

redis_db = redis.Redis(host='localhost', port=6379, db=0)


class User:
    """
    User service
    """

    @staticmethod
    def register(username: str, password: str) -> None:
        """
        Register a new user
        :param username:
        :param password:
        :return:
        """
        if redis_db.get(username):
            raise HTTPException(status_code=409, detail="User already exists")

        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        redis_db.set(username, hashed_password)

    @staticmethod
    def authenticate(credentials: HTTPBasicCredentials, secret_key: str) -> str:
        """
        Authenticate a user
        :param credentials:
        :param secret_key:
        :return:
        """
        username = credentials.username
        password = credentials.password.encode()

        hashed_password = redis_db.get(username)
        if not hashed_password or not bcrypt.checkpw(password, hashed_password):
            raise HTTPException(status_code=401, detail="")

        access_token = create_access_token(username, secret_key)
        return access_token

    @staticmethod
    def get_user(username: str) -> dict:
        """
        Get user from redis
        :param username:
        :return:
        """
        hashed_password = redis_db.get(username)
        if not hashed_password:
            raise HTTPException(status_code=404, detail="User not found")
        return {"username": username}

    @staticmethod
    def create_access_token(username: str, secret_key: str,) -> str:
        """
        Create a new access token
        :param username:
        :param secret_key:
        :return:
        """
        payload = {"sub": username}
        token = jwt.encode(payload, secret_key, algorithm="HS256",)
        return token
