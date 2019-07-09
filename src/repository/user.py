from typing import List, Dict, Union, Optional

from src.models.user import User, FavoriteMovie
from src.repository.movie import MovieRepository


class UserRepository(object):

    @staticmethod
    def create_user(name: str, email: str, password: str, **kwargs) -> Optional[User]:
        existing_user = UserRepository.get_by_email(email)
        if existing_user:
            return None

        new_user = User(name, email, password, **kwargs)
        return new_user.save()

    @staticmethod
    def update_user(user: User, **kwargs) -> User:
        updatable_columns = user.updatable_columns()
        for key in kwargs.keys():
            if key not in updatable_columns:
                kwargs.pop(key)

        return user.update(**kwargs)

    @staticmethod
    def get_all() -> List[User]:
        return User.query.all()

    @staticmethod
    def get_by_id(id: int) -> User:
        # TODO: implement mechanism to get user form cache
        return User.query.get(id)

    @staticmethod
    def get_by_email(email: str) -> User:
        return User.query.filter(
            User.email == email
        ).first()

    @staticmethod
    def get_favorite_movie_by_imdb_id(user: User, imdb_id: str) -> FavoriteMovie:
        return FavoriteMovie.query.filter(
            (FavoriteMovie.user_id == user.id) &
            (FavoriteMovie.imdb_id == imdb_id)
        ).first()

    @staticmethod
    def add_user_favorite_movie(user: User, imdb_id: str):
        existing_fav = UserRepository.get_favorite_movie_by_imdb_id(user, imdb_id)
        if existing_fav:
            existing_fav.delete()
            return None

        fav_movie = FavoriteMovie(user_id=user.id, imdb_id=imdb_id)
        return fav_movie.save()

    @staticmethod
    def get_users_favorite_movies(user: User) -> List[FavoriteMovie]:
        movies = [
            movie
            for movie in user.rel_favorite_movies
        ]
        return movies

    @staticmethod
    def get_users_favorite_movie_details(user: User) -> List[Dict[str, str]]:
        fav_movies = UserRepository.get_users_favorite_movies(user=user)
        movie_details = []
        for movie in fav_movies:
            movie_info = MovieRepository.get_movie_info(movie=movie)
            movie_info["favorite"] = True
            movie_details.append(movie_info)

        return movie_details

    @staticmethod
    def add_attribute_to_favorite_movies(user: User, movie_details: Union[List[Dict[str, str]], Dict[str, str]]):
        fav_movies = UserRepository.get_users_favorite_movies(user=user)
        fav_movies = {movie.imdb_id for movie in fav_movies}

        if isinstance(movie_details, list):
            for movie_info in movie_details:
                if movie_info.get("imdbID") in fav_movies:
                    movie_info.update({"favorite": True})
        elif isinstance(movie_details, dict):
            if movie_details.get("imdbID") in fav_movies:
                movie_details.update({"favorite": True})

        return movie_details
