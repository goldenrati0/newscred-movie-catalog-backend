from .core import app
from .resource import user_blueprint

app.register_blueprint(user_blueprint)
