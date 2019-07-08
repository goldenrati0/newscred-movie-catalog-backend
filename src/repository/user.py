from typing import List, Dict, Set

from ..models import User, FavoriteMovie


class UserRepository(object):

    @staticmethod
    def create_user(name: str, email: str, password: str, **kwargs) -> User:
        existing_user = UserRepository.get_by_email(email)
        if existing_user:
            return existing_user

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
    def add_user_favorite_movie(user: User, imdb_id: str):
        fav_movie = FavoriteMovie(user_id=user.id, imdb_id=imdb_id)
        fav_movie.save()

    @staticmethod
    def get_favorite_movies(user: User) -> Set[str]:
        return {
            movie.imdb_movie_id
            for movie in user.rel_favorite_movies
        }

    @staticmethod
    def filter_favorite_movies(user: User, movies: List[Dict[str, str]]) -> List[Dict[str, str]]:
        fav_movies = UserRepository.get_favorite_movies(user)
        for movie in movies:
            if movie.get("imdb_id") in fav_movies:
                movie["favorite"] = True

        return movies
