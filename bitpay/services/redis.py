import redis
from bitpay.services.config_manager import ConfigManager


class RedisHandler:
    def __init__(self):
        self.config = ConfigManager()
        self.user_client = redis.Redis(
            host=self.config.read_config("REDIS", "host"),
            port=self.config.read_config("REDIS", "port"),
            db=self.config.read_config("REDIS", "user_db"),
            password=self.config.read_config("REDIS", "password"))
        self.user_client = redis.Redis(
            host=self.config.read_config("REDIS", "host"),
            port=self.config.read_config("REDIS", "port"),
            db=self.config.read_config("REDIS", "wallet_db"),
            password=self.config.read_config("REDIS", "password"))

    def save_credentials(self, username, hashed_password) -> None:
        """
        Save username and password in redis
        :param username:
        :param password:
        :return:
        """
        self.user_client.set(username, hashed_password)

    def get_password(self, username) -> bytes | None:
        """
        Get password from redis
        :param username:
        :return:
        """
        return self.user_client.get(username)

    def user_exists(self, username) -> int:
        """
        Check if user exists in redis
        :param username:
        :return:
        """
        return self.user_client.exists(username)

    def delete_credentials(self, username) -> None:
        """
        Delete credentials from redis
        :param username:
        :return:
        """
        self.user_client.delete(username)
