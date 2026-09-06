from flask import Blueprint

from src.controllers import relatorio_controller

relatorio_bp = Blueprint("relatorios", __name__)


@relatorio_bp.route("/relatorios/vendas", methods=["GET"])
def relatorio_vendas():
    return relatorio_controller.relatorio_vendas()
