from flask import Flask
from flask_cors import CORS

from src.config import settings
from src.database import create_connection, init_schema, seed_data
from src.middlewares.error_handler import register_error_handlers
from src.views.routes import register_routes


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = settings.SECRET_KEY
    app.config["DEBUG"] = settings.DEBUG
    app.config["ADMIN_TOKEN"] = settings.ADMIN_TOKEN
    CORS(app)

    app.db = create_connection(settings.DB_PATH)
    init_schema(app.db)
    seed_data(app.db)

    register_routes(app)
    register_error_handlers(app)

    return app
