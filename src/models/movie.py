from typing import Dict, List


class Movie(object):
    def __init__(self, title, year, imdb_id, movie_type, poster):
        self.title = title
        self.year = year
        self.imdb_id = imdb_id
        self.movie_type = movie_type
        self.poster = poster

    def to_dict(self):
        return {
            "title": self.title,
            "year": self.year,
            "imdb_id": self.imdb_id,
            "movie_type": self.movie_type,
            "poster": self.poster
        }


class MovieFactory(object):
    @staticmethod
    def get_movie(movie_data: Dict) -> Movie:
        try:
            title = movie_data["Title"]
            year = movie_data["Year"]
            imdb_id = movie_data["imdbID"]
            movie_type = movie_data["Type"]
            poster = movie_data["Poster"]

            movie = Movie(title, year, imdb_id, movie_type, poster)
            return movie
        except Exception as _e:
            raise Exception(_e)

    @staticmethod
    def get_movies(movie_data_list: List[Dict[str, str]]) -> List[Movie]:
        movies = []
        for movie_data in movie_data_list:
            m = MovieFactory.get_movie(movie_data)
            movies.append(m)
        return movies
