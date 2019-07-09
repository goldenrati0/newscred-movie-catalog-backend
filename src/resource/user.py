from flask import Blueprint, request
from flask_jwt_extended import jwt_required, current_user
from flask_restful import Api, Resource

from src.decorators.requests import json_data_required
from src.repository.user_token import UserToken
from src.repository.user import UserRepository, MovieRepository
from src.utils import ResponseGenerator

user_blueprint = Blueprint(name="userbp", import_name=__name__, url_prefix="/user")
api = Api(app=user_blueprint)


class UserRegister(Resource):
    method_decorators = [json_data_required]

    def post(self):
        data = request.get_json()

        mandatory_fields = ["name", "email", "password"]
        if any(data.get(item) is None for item in mandatory_fields):
            return ResponseGenerator.mandatory_field(fields=mandatory_fields)

        name, email, password = data.pop("name"), data.pop("email"), data.pop("password")
        user = UserRepository.create_user(name=name, email=email, password=password, **data)
        if not user:
            return ResponseGenerator.error_response(msg="Email is already registered, try to login", code=400)

        access_token = UserToken.create_user_access_token(user=user)
        return ResponseGenerator.generate_response({
            "access_token": access_token
        }, code=201)


class UserLogin(Resource):
    method_decorators = [json_data_required]

    def post(self):
        data = request.get_json()

        mandatory_fields = ["email", "password"]
        if any(data.get(item) is None for item in mandatory_fields):
            return ResponseGenerator.mandatory_field(fields=mandatory_fields)

        email = data["email"]
        password = data["password"]

        user = UserRepository.get_by_email(email=email)
        if not user:
            return ResponseGenerator.not_found(msg="user not found")

        if not user.check_password(password=password):
            return ResponseGenerator.forbidden(msg="email/password combination is invalid")

        access_token = UserToken.create_user_access_token(user=user)
        return ResponseGenerator.generate_response({
            "access_token": access_token
        }, code=200)


class UserProfile(Resource):

    @jwt_required
    def get(self):
        return ResponseGenerator.generate_response(current_user.json, code=200)


class UserFavMovies(Resource):
    method_decorators = [jwt_required]

    def get(self):
        fav_movies = UserRepository.get_users_favorite_movie_details(current_user)
        return ResponseGenerator.generate_response(fav_movies, code=200)

    @json_data_required
    def post(self):
        data = request.get_json()

        mandatory_fields = ["imdb_id"]
        if any(data.get(item) is None for item in mandatory_fields):
            return ResponseGenerator.mandatory_field(fields=mandatory_fields)

        fav_movie = UserRepository.add_user_favorite_movie(user=current_user, imdb_id=data["imdb_id"])
        if not fav_movie:
            return ResponseGenerator.generate_response(data={"msg": "disliked"}, code=204)

        fav_movie = MovieRepository.get_movie_info(fav_movie)
        return ResponseGenerator.generate_response(data=fav_movie, code=201)


api.add_resource(UserRegister, "/register")
api.add_resource(UserLogin, "/login")
api.add_resource(UserProfile, "/me")
api.add_resource(UserFavMovies, "/me/movies")
