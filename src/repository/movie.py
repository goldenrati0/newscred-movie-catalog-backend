from typing import Dict, List, Union

from ..models import OMDBClient, FavoriteMovie
from ..redis_utilities import RedisCacheFactory


class MovieRepository(object):
    redis_movie_cache = RedisCacheFactory.get_redis_client(storage="movie")
    omdb_client = OMDBClient()

    @staticmethod
    def get_movie_info(movie: FavoriteMovie) -> Dict[str, Union[str, int, List, Dict]]:
        cached_movie_data = MovieRepository.redis_movie_cache.get(movie.imdb_id)
        if not cached_movie_data:
            movie_data = MovieRepository.omdb_client.get_full_movie_info(imdb_id=movie.imdb_id)
            MovieRepository.redis_movie_cache.set(key=movie.imdb_id, value=movie_data)
            cached_movie_data = movie_data
        return cached_movie_data
