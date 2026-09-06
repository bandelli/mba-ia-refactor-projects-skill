from flask import Blueprint

from src.controllers import sistema_controller

health_bp = Blueprint("health", __name__)


@health_bp.route("/", methods=["GET"])
def index():
    return sistema_controller.index()


@health_bp.route("/health", methods=["GET"])
def health_check():
    return sistema_controller.health_check()
