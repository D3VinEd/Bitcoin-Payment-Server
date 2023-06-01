import redis

class RedisHandler:
    def __init__(self, host='localhost', port=6379, db=0):
        self.redis_client = redis.Redis(host=host, port=port, db=db)

    def save_credentials(self, username, password):
        self.redis_client.set(username, password)

    def get_password(self, username):
        return self.redis_client.get(username)

    def delete_credentials(self, username):
        self.redis_client.delete(username)
