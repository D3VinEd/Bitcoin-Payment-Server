from fastapi import HTTPException
from fastapi.security import HTTPBasic
from bitpay.services.redis import RedisHandler
from bitpay.services.config_manager import ConfigManager
from bitpay.services.authentication import Auth

security = HTTPBasic()
config = ConfigManager()


class User:
    """
    User service
    """

    def __init__(self, username: str):
        self.config = ConfigManager()
        self.redis_client = RedisHandler()
        self.username = username

    def register(self, password: str) -> None:
        """
        Register a new user
        """
        if self.redis_client.user_exists(self.username):
            raise HTTPException(status_code=409, detail="User already exists")

        hashed_password = Auth.hash_password(password)
        self.redis_client.save_credentials(self.username, hashed_password)

    def login(self, password: str) -> None:
        if not self.redis_client.user_exists(self.username):
            raise HTTPException(status_code=404, detail="User not found")

        stored_password = self.redis_client.get_password(self.username)
        if not Auth.check_password(password, stored_password.decode()):
            raise HTTPException(status_code=403, detail="Invalid password")

    def delete(self):
        """
        Delete a user
        """
        # Delete user from the database
        self.redis_client.delete_user(self.username)

    def check_user_exists(self, username: str) -> int:
        """
        Check if a user exists
        """
        return self.redis_client.user_exists(username)
