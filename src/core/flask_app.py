from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from src.core.config import Configuration

app = Flask(__name__)
CORS(app)
app.config.from_object(Configuration)
jwt = JWTManager(app)
