import pickle

from redis import Redis

from src.core.config import Configuration

DEFAULT_EXPIRATION_TIME = 10 * 24 * 60 * 60  # 10 days


class CacheBase:

    def __init__(self, host, port, db, password, **kwargs):
        self.client = Redis(host=host, port=port, db=db, password=password, **kwargs)
        self.ex = kwargs.get("ex", DEFAULT_EXPIRATION_TIME)

    def set(self, key, value, **kwargs) -> bool:
        raise NotImplementedError

    def get(self, key):
        raise NotImplementedError


class RedisCache(CacheBase):

    def __init__(self, db: int = 0):
        super(RedisCache, self).__init__(Configuration.REDIS_HOST, Configuration.REDIS_PORT, db,
                                         Configuration.REDIS_PASSWORD)

    def set(self, key, value, **kwargs) -> bool:
        return self.client.set(name=key, value=pickle.dumps(value), ex=kwargs.get("ex", self.ex))

    def get(self, key):
        obj = self.client.get(name=key)
        if not obj:
            return None
        return pickle.loads(obj)


class RedisUserCache(RedisCache):

    def __init__(self):
        super(RedisUserCache, self).__init__(db=0)


class RedisMovieCache(RedisCache):
    client = None

    def __init__(self):
        super(RedisMovieCache, self).__init__(db=1)


class RedisCacheFactory:
    clients = {}

    @staticmethod
    def get_redis_client(storage: str) -> RedisCache:
        if storage not in RedisCacheFactory.clients:
            c = None
            if storage == "user":
                c = RedisUserCache()
            elif storage == "movie":
                c = RedisMovieCache()
            if c:
                RedisCacheFactory.clients[storage] = c

        return RedisCacheFactory.clients[storage]
