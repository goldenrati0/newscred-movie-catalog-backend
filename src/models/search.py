from typing import List, Dict, Union

from src.models.omdb import OMDBClient


class MovieSearch:
    def __init__(self, omdb_client: OMDBClient = None):
        if not omdb_client:
            omdb_client = OMDBClient()
        self._client = omdb_client

    def search(self, search_query: str, page: int = 1) -> List[Dict[str, Union[str, int, List, Dict]]]:
        if not search_query:
            raise Exception("nothing to search for")

        self._client.set_page(page)
        return self._client.search_movies(search_query)

    def search_movie(self, imdb_id: str, **kwargs) -> Dict:
        return self._client.get_full_movie_info(imdb_id=imdb_id, **kwargs)
