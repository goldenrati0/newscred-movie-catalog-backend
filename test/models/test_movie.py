import os
import unittest

from src.models.movie import Movie
from src.models.omdb import OMDBClient
from src.models.search import MovieSearch


class TestMovie(unittest.TestCase):

    def setUp(self) -> None:
        self.omdb_client = OMDBClient(apikey=os.getenv("OMDB_API_KEY"))
        self.client = MovieSearch(omdb_client=self.omdb_client)

    def test_movie(self):
        movies = self.client.search(search_query="godfather")
        for movie in movies:
            self.assertTrue(isinstance(movie, dict))
