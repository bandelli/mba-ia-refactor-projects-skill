import logging

from flask import jsonify

logger = logging.getLogger(__name__)


def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(_error):
        return jsonify({"error": "Recurso não encontrado"}), 404

    @app.errorhandler(Exception)
    def handle_exception(error):
        logger.exception("Erro não tratado: %s", error)
        return jsonify({"error": "Erro interno"}), 500
