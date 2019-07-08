import os
import unittest

from src.models.omdb import OMDBClient
from src.models.search import MovieSearch


class TestMovieSearch(unittest.TestCase):

    def setUp(self) -> None:
        self.omdb_client = OMDBClient(apikey=os.getenv("OMDB_API_KEY"))
        self.client = MovieSearch(omdb_client=self.omdb_client)

    def test_search(self):
        movies = self.client.search(search_query="godfather")

        self.assertNotEqual(movies, [])
        self.assertTrue(len(movies) >= 1)

        imdb_ids = {m["imdbID"] for m in movies}
        for imdbid in ["tt0068646", "tt0071562", "tt0099674"]:
            self.assertTrue(imdbid in imdb_ids)

    def test_search_movie(self):
        movie_info = self.client.search_movie(imdb_id="tt0068646")

        self.assertEqual(movie_info["Title"], "The Godfather")
        self.assertEqual(movie_info["imdbID"], "tt0068646")
