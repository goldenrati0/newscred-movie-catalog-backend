from flask import Blueprint, request
from flask_jwt_extended import jwt_required, current_user
from flask_restful import Api, Resource

from ..decorators import json_data_required
from ..repository import UserRepository, UserToken
from ..utils import ResponseGenerator

user_blueprint = Blueprint(name="userbp", import_name=__name__, url_prefix="/user")
api = Api(app=user_blueprint)


class UserLogin(Resource):
    method_decorators = [json_data_required]

    def post(self):
        data = request.get_json()

        mandatory_fields = ["email", "password"]
        if any(data.get(item) is None for item in mandatory_fields):
            return ResponseGenerator.mandatory_field(fields=["email", "password"])

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

    @jwt_required
    def get(self):
        return ResponseGenerator.generate_response(list(UserRepository.get_favorite_movies(current_user)), code=200)


api.add_resource(UserLogin, "/login")
api.add_resource(UserProfile, "/me")
api.add_resource(UserFavMovies, "/me/movies")
