import os
import unittest

from src.models import OMDBClient, MovieSearch


class TestMovieSearch(unittest.TestCase):

    def setUp(self) -> None:
        self.omdb_client = OMDBClient(apikey=os.getenv("OMDB_API_KEY"))
        self.client = MovieSearch(s="godfather", omdb_client=self.omdb_client)

    def test_search(self):
        movies = self.client.search()

        self.assertNotEqual(movies, [])
        self.assertTrue(len(movies) >= 1)

        imdb_ids = {m.imdb_id for m in movies}
        for imdbid in ["tt0068646", "tt0071562", "tt0099674"]:
            self.assertTrue(imdbid in imdb_ids)

    def test_next_page(self):
        self.client.set_query("train")
        first_page_movie_ids = {m.imdb_id for m in self.client.search()}
        second_page_movie_ids = {m.imdb_id for m in self.client.next_page()}

        self.assertNotEqual(second_page_movie_ids, [])
        self.assertTrue(len(second_page_movie_ids) >= 1)

        for mid in first_page_movie_ids:
            self.assertTrue(mid not in second_page_movie_ids)
