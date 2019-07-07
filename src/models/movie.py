from typing import Dict, List


class Movie(object):
    __extra_attributes = {'Rated', 'Released', 'Runtime', 'Director', 'Writer', 'Actors', 'Plot', 'Language',
                          'Country',
                          'Awards', 'Ratings', 'Metascore', 'imdbRating', 'imdbVotes', 'Type', 'DVD', 'BoxOffice',
                          'Production',
                          'Website', 'Response', 'Genre'}

    def __init__(self, title, year, imdb_id, movie_type, poster, **kwargs):
        self.title = title
        self.year = year
        self.imdb_id = imdb_id
        self.movie_type = movie_type
        self.poster = poster

        for key in kwargs:
            if not hasattr(self, key) and not hasattr(self, key.lower()):
                setattr(self, key, kwargs[key])

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
            title = movie_data.pop("Title", None)
            year = movie_data.pop("Year", None)
            imdb_id = movie_data.pop("imdbID", None)
            movie_type = movie_data.pop("Type", None)
            poster = movie_data.pop("Poster", None)

            movie = Movie(title, year, imdb_id, movie_type, poster, **movie_data)
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
