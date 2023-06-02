from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import bcrypt
import jwt
from bitpay.services.redis import RedisHandler
from bitpay.services.config_manager import ConfigManager

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
redis = RedisHandler()
config = ConfigManager()


class Auth:
    """
    Authentication class.
    """

    @staticmethod
    def check_auth(username: str, password: str):
        """
        Check if a username/password combination is valid.
        """
        stored_password = redis.get_password(username)
        return Auth.check_password(password, stored_password.decode())

    @classmethod
    def auth_required(cls, token: str = Depends(oauth2_scheme)):
        """
        Verify if a user is authenticated.
        """
        username = cls.verify_token(token)
        if not redis.user_exists(username):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return username

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a password for storing.
        """
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    @staticmethod
    def verify_token(token: str = Depends(oauth2_scheme)):
        """
        Verifies a JWT token.
        """
        try:
            secret_key = config.read_config("JWT", "secret_key")
            algorithm = config.read_config("JWT", "algorithm")
            payload = jwt.decode(token, secret_key, algorithms=[algorithm])
            username: str = payload.get("sub")
            if username is None or not redis.user_exists(username):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            return username
        except jwt.PyJWTError:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate credentials",
            )

    @staticmethod
    def authenticate(username: str, password: str) -> str:
        """
        Authenticate a user
        """
        hashed_password = redis.get_password(username)
        if not hashed_password or not bcrypt.checkpw(password.encode(), hashed_password.encode()):
            raise HTTPException(status_code=401, detail="")

        access_token = Auth.create_access_token(username)
        return access_token

    @staticmethod
    def create_access_token(username: str) -> str:
        """
        Create a new access token
        """
        secret_key = config.read_config("JWT", "secret_key")
        algorithm = config.read_config("JWT", "algorithm")
        payload = {"sub": username}
        token = jwt.encode(payload, secret_key, algorithm=algorithm)
        return token

    @staticmethod
    def check_password(input_password: str, stored_password: str) -> bool:
        """
        Compare input_password with stored_password
        """
        return bcrypt.checkpw(input_password.encode(), stored_password.encode())
