from src.core.database import app
from src.core.flask_app import jwt
from src.models.user import User
from src.repository.user import UserRepository
from src.resource.user import user_blueprint
from src.resource.search import search_blueprint
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
app.register_blueprint(search_blueprint)
