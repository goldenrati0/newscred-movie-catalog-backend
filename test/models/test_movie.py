import os
import unittest

from src.models import OMDBClient, MovieSearch, Movie


class TestMovie(unittest.TestCase):

    def setUp(self) -> None:
        self.omdb_client = OMDBClient(apikey=os.getenv("OMDB_API_KEY"))
        self.client = MovieSearch(s="godfather", omdb_client=self.omdb_client)

    def test_movie(self):
        movies = self.client.search()
        for m in movies:
            self.assertTrue(isinstance(m, Movie))

    def test_movie_todict(self):
        self.client.set_query("train")
        movies = self.client.search(page=2)
        first_movie = movies[0]
        movie_dict = first_movie.to_dict()

        self.assertEqual(first_movie.imdb_id, movie_dict["imdb_id"])
        self.assertEqual(first_movie.title, movie_dict["title"])
        self.assertEqual(first_movie.year, movie_dict["year"])
