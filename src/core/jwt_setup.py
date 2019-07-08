from .flask_app import jwt
from ..models.user import User
from ..repository.user import UserRepository
from ..utils import ResponseGenerator


@jwt.user_loader_callback_loader
def flask_jwt_user_loader_callback(identity) -> User:
    return UserRepository.get_by_id(id=identity)


@jwt.user_loader_error_loader
def flask_jwt_user_loader_error_callback(identity):
    return ResponseGenerator.not_found(msg="User::{} not found".format(identity))
