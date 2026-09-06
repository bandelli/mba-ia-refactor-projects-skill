from flask import current_app, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash

from src.models import usuario_model


def listar_usuarios():
    usuarios = usuario_model.get_todos_usuarios(current_app.db)
    for usuario in usuarios:
        usuario.pop("senha", None)
    return jsonify({"dados": usuarios, "sucesso": True}), 200


def buscar_usuario(id):
    usuario = usuario_model.get_usuario_por_id(current_app.db, id)
    if not usuario:
        return jsonify({"erro": "Usuário não encontrado"}), 404
    usuario.pop("senha", None)
    return jsonify({"dados": usuario, "sucesso": True}), 200


def criar_usuario():
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Dados inválidos"}), 400

    nome = dados.get("nome", "")
    email = dados.get("email", "")
    senha = dados.get("senha", "")

    if not nome or not email or not senha:
        return jsonify({"erro": "Nome, email e senha são obrigatórios"}), 400

    senha_hash = generate_password_hash(senha, method="pbkdf2:sha256")
    id = usuario_model.criar_usuario(current_app.db, nome, email, senha_hash)
    current_app.logger.info("Usuário criado: %s", email)
    return jsonify({"dados": {"id": id}, "sucesso": True}), 201


def login():
    dados = request.get_json() or {}
    email = dados.get("email", "")
    senha = dados.get("senha", "")

    if not email or not senha:
        return jsonify({"erro": "Email e senha são obrigatórios"}), 400

    usuario = usuario_model.get_usuario_por_email(current_app.db, email)
    if not usuario or not check_password_hash(usuario["senha"], senha):
        current_app.logger.info("Login falhou: %s", email)
        return jsonify({"erro": "Email ou senha inválidos", "sucesso": False}), 401

    current_app.logger.info("Login bem-sucedido: %s", email)
    usuario.pop("senha", None)
    return jsonify({"dados": usuario, "sucesso": True, "mensagem": "Login OK"}), 200
