from flask import Blueprint

from src.controllers import produto_controller

produto_bp = Blueprint("produtos", __name__)


@produto_bp.route("/produtos", methods=["GET"])
def listar_produtos():
    return produto_controller.listar_produtos()


@produto_bp.route("/produtos/busca", methods=["GET"])
def buscar_produtos():
    return produto_controller.buscar_produtos()


@produto_bp.route("/produtos/<int:id>", methods=["GET"])
def buscar_produto(id):
    return produto_controller.buscar_produto(id)


@produto_bp.route("/produtos", methods=["POST"])
def criar_produto():
    return produto_controller.criar_produto()


@produto_bp.route("/produtos/<int:id>", methods=["PUT"])
def atualizar_produto(id):
    return produto_controller.atualizar_produto(id)


@produto_bp.route("/produtos/<int:id>", methods=["DELETE"])
def deletar_produto(id):
    return produto_controller.deletar_produto(id)
