from flask import Blueprint

from src.controllers import sistema_controller
from src.middlewares.auth import require_admin_auth

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/admin/reset-db", methods=["POST"])
@require_admin_auth
def reset_database():
    return sistema_controller.reset_database()
