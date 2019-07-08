from typing import List, Dict

from .movie import Movie
from .omdb import OMDBClient


class MovieSearch:
    def __init__(self, omdb_client: OMDBClient = None, **kwargs):
        if not omdb_client:
            omdb_client = OMDBClient()
        self._client = omdb_client
        self._s = None
        self._page = kwargs.get("page", 1)

    def set_query(self, s: str):
        self._s = s
        self._page = 1

    def search(self, page: int = 1) -> List[Movie]:
        if not self._s:
            raise Exception("nothing to search for")

        if page != 1:
            self._page = page

        self._client.set_page(self._page)
        return self._client.search_movies(self._s)

    def search_movie(self, imdb_id: str, **kwargs) -> Dict:
        return self._client.get_full_movie_info(imdb_id=imdb_id, **kwargs)

    def next_page(self) -> List[Movie]:
        self._page += 1
        return self.search()
