from src.core import app
from src.core.flask_app import jwt
from src.models import User
from src.repository import UserRepository
from src.resource import user_blueprint
from src.utils import ResponseGenerator


@jwt.user_loader_callback_loader
def flask_jwt_user_loader_callback(identity) -> User:
    return UserRepository.get_by_id(id=identity)


@jwt.user_loader_error_loader
def flask_jwt_user_loader_error_callback(identity):
    return ResponseGenerator.not_found(msg="User::{} not found".format(identity))


@app.route("/")
def home():
    return ResponseGenerator.generate_response("welcome to your personal movie database", 200)


app.register_blueprint(user_blueprint)
