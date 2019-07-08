from flask_jwt_extended import create_access_token, create_refresh_token

from src.models.user import User


class UserToken:

    @staticmethod
    def create_user_access_token(user: User) -> str:
        return create_access_token(identity=user.id)

    @staticmethod
    def create_user_refresh_token(user: User) -> str:
        return create_refresh_token(identity=user.id)
