import json
from typing import Dict, List, Any, Union, Optional

import requests
from requests.models import Response

from src.models.movie import MovieFactory
from src.core.flask_app import app


class OMDBClient(object):
    _params: Dict[str, Any] = {}
    _headers: Dict[str, Any] = {}

    def __init__(self, **kwargs):
        self._apikey = kwargs.get("apikey", app.config.get("OMDB_API_KEY", ""))
        if not self._apikey:
            raise Exception("omdb api key not found. Pass apikey argument or set OMDB_API_KEY in flask app config")

        self._base_url: str = f"http://www.omdbapi.com/"

        self._params["apikey"] = self._apikey
        self._headers["Accept"] = "application/json"

        if "params" in kwargs:
            if isinstance(kwargs["params"], dict):
                params = kwargs["params"]
                for key in params.keys():
                    self._params[key] = params[key]

        if "headers" in kwargs:
            if isinstance(kwargs["headers"], dict):
                headers = kwargs["headers"]
                for key in headers.keys():
                    self._headers[key] = headers[key]

    def set_page(self, page: int = 1):
        self._params["page"] = page

    def _make_request(self, s: str) -> Response:
        url = self._base_url
        params = self._params.copy()
        params["s"] = s
        response = requests.get(url, params=params, headers=self._headers)
        response.raise_for_status()
        return response

    def _search_string(self, s: str) -> Dict:
        response = self._make_request(s)
        json_res = response.json()
        assert json_res["Response"] == "True", f"invalid response from omdb api, error: {json_res['Error']}"
        return json_res

    def search_movies(self, s: str) -> List[Dict[str, Union[str, int, List, Dict]]]:
        data = self._search_string(s)
        if "Search" not in data:
            return []

        from src.repository.movie import MovieRepository

        movies = MovieFactory.get_movies(data["Search"])
        movie_details = []
        for movie in movies:
            movie_info = MovieRepository.get_movie_info(movie=movie)
            if movie_info:
                movie_details.append(movie_info)
        return movie_details

    def get_full_movie_info(self, imdb_id: str, plot: str = "full", type: str = "movie") -> Optional[Dict]:
        url = self._base_url
        params = {
            "apikey": self._apikey,
            "i": imdb_id,
            "plot": plot,
            "type": type
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        try:
            return response.json()
        except json.decoder.JSONDecodeError as _e:
            return None
