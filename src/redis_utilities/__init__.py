import pickle
from typing import Optional, Dict

from redis import Redis

from ..core.config import Configuration

RDS_CLIENT = Redis(host=Configuration.REDIS_HOST, port=Configuration.REDIS_PORT, db=Configuration.REDIS_DB,
                   password=Configuration.REDIS_PASSWORD)


class RedisUtilities:

    @staticmethod
    def get_item(key: str) -> Optional[Dict]:
        data = RDS_CLIENT.get(name=key)
        if not data:
            return None
        return pickle.loads(data)

    @staticmethod
    def set_item(key: str, data) -> bool:
        return RDS_CLIENT.set(name=key, value=pickle.dumps(data), ex=None)
