from typing import Dict, List, Union

from ..models import OMDBClient
from ..redis_utilities import RedisCacheFactory

redis_movie_cache = RedisCacheFactory.get_redis_client(storage="movie")


class MovieRepository(object):

    @staticmethod
    def get_movie_info(imdb_id: str) -> Dict[str, Union[str, int, List, Dict]]:
        cached_movie_data = redis_movie_cache.get(imdb_id)
        if not cached_movie_data:
            omdb_client = OMDBClient()
            movie_data = omdb_client.get_full_movie_info(imdb_id=imdb_id)
            redis_movie_cache.set(key=imdb_id, value=movie_data)
            return movie_data
        return cached_movie_data
