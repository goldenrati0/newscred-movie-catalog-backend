from typing import Dict, List, Union, Optional

from src.models.movie import Movie
from src.models.user import FavoriteMovie
from src.models.omdb import OMDBClient
from src.redis_utilities import RedisCacheFactory


class MovieRepository(object):
    redis_movie_cache = RedisCacheFactory.get_redis_client(storage="movie")
    omdb_client = OMDBClient()

    @staticmethod
    def get_movie_info(movie: Union[FavoriteMovie, Movie]) -> Optional[Dict[str, Union[str, int, List, Dict]]]:
        cached_movie_data = MovieRepository.redis_movie_cache.get(movie.imdb_id)
        if not cached_movie_data:
            movie_data = MovieRepository.omdb_client.get_full_movie_info(imdb_id=movie.imdb_id)
            if not movie_data:
                return None

            movie_data["ShortPlot"] = movie_data.get("Plot", "N/A")[:50]
            MovieRepository.redis_movie_cache.set(key=movie.imdb_id, value=movie_data)
            cached_movie_data = movie_data
        return cached_movie_data
