from flask import Flask
from flask_cors import CORS

from src.config import settings
from src.database import create_connection, init_schema, seed_data
from src.middlewares.error_handler import register_error_handlers
from src.routes.admin_routes import admin_bp
from src.routes.health_routes import health_bp
from src.routes.pedido_routes import pedido_bp
from src.routes.produto_routes import produto_bp
from src.routes.relatorio_routes import relatorio_bp
from src.routes.usuario_routes import usuario_bp


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = settings.SECRET_KEY
    app.config["DEBUG"] = settings.DEBUG
    app.config["ADMIN_TOKEN"] = settings.ADMIN_TOKEN
    CORS(app)

    app.db = create_connection(settings.DB_PATH)
    init_schema(app.db)
    seed_data(app.db)

    app.register_blueprint(produto_bp)
    app.register_blueprint(usuario_bp)
    app.register_blueprint(pedido_bp)
    app.register_blueprint(relatorio_bp)
    app.register_blueprint(health_bp)
    app.register_blueprint(admin_bp)

    register_error_handlers(app)

    return app
