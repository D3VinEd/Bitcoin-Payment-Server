from fastapi import HTTPException
from fastapi.security import HTTPBasic
from bitpay.services.redis import RedisHandler
from bitpay.services.config_manager import ConfigManager
from bitpay.services.authentication import Auth

security = HTTPBasic()
redis = RedisHandler()
config = ConfigManager()


class User:
    """
    User service
    """
    def __init__(self, username: str):
        self.username = username
        self.config = ConfigManager()
        self.redis_client = RedisHandler()

    def register(self, password: str) -> None:
        """
        Register a new user
        """
        if redis.user_exists(self.username):
            raise HTTPException(status_code=409, detail="User already exists")

        hashed_password = Auth.hash_password(password)
        redis.save_credentials(self.username, hashed_password)

    def login(self, password: str) -> None:
        if not self.redis_client.user_exists(self.username):
            raise HTTPException(status_code=404, detail="User not found")

        stored_password = self.redis_client.get_password(self.username)
        if not Auth.check_password(password, stored_password.decode()): # @ToDo decode check
            raise HTTPException(status_code=403, detail="Invalid password")

    def delete(self):
        """
        Delete a user
        """
        # Delete user from the database
        redis.delete_credentials(self.username)
