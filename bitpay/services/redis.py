import redis


class RedisHandler:
    def __init__(self, host='localhost', port=6379, db=0):
        self.redis_client = redis.Redis(host=host, port=port, db=db)

    def save_credentials(self, username, password):
        """
        Save username and password in redis
        :param username:
        :param password:
        :return:
        """
        self.redis_client.set(username, password)

    def get_password(self, username):
        """
        Get password from redis
        :param username:
        :return:
        """
        return self.redis_client.get(username)

    def delete_credentials(self, username):
        """
        Delete credentials from redis
        :param username:
        :return:
        """
        self.redis_client.delete(username)
