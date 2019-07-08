from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from .config import Configuration

app = Flask(__name__)
CORS(app)
app.config.from_object(Configuration)
jwt = JWTManager(app)

from ..models import User
from ..repository import UserRepository


@jwt.user_loader_callback_loader
def flask_jwt_user_loader_callback(identity) -> User:
    return UserRepository.get_by_id(id=identity)
