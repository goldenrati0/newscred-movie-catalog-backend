from typing import Dict, List, Union

from ..models import OMDBClient
from ..redis_utilities import RedisUtilities


class MovieRepository(object):

    @staticmethod
    def get_movie_info(imdb_id: str) -> Dict[str, Union[str, int, List, Dict]]:
        cached_movie_data = RedisUtilities.get_item(imdb_id)
        if not cached_movie_data:
            omdb_client = OMDBClient()
            movie_data = omdb_client.get_full_movie_info(imdb_id=imdb_id)
            RedisUtilities.set_item(key=imdb_id, data=movie_data)
            return movie_data
        return cached_movie_data
