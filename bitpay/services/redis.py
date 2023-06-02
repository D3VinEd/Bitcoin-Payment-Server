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
        self.wallet_client = redis.Redis(
            host=self.config.read_config("REDIS", "host"),
            port=self.config.read_config("REDIS", "port"),
            db=self.config.read_config("REDIS", "wallet_db"),
            password=self.config.read_config("REDIS", "password"))

    # User related methods
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

    def delete_user(self, username) -> None:
        """
        Delete credentials from redis
        :param username:
        :return:
        """
        self.user_client.delete(username)

    # Wallet related methods
    def store_keys(self, username: str, key_hex_list: list) -> None:
        """
        Store the keys in the database
        :param username: Username
        :param key_hex_list: List of key hex strings
        :return: None
        """
        for key_hex in key_hex_list:
            if key_hex is not None:
                self.wallet_client.rpush(username, key_hex)

    def delete_keys(self, username: str) -> None:
        """
        Delete all keys associated with a username
        :param username: Username
        :return: None
        """
        self.wallet_client.delete(username)

    def get_keys(self, username: str) -> list:
        """
        Get all keys associated with a username
        :param username: Username
        :return: List of key hex strings
        """
        keys = self.wallet_client.lrange(username, 0, -1)
        return [key.decode() for key in keys]

