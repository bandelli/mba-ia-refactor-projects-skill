from flask import current_app, jsonify, request

from src.models import produto_model

CATEGORIAS_VALIDAS = ["informatica", "moveis", "vestuario", "geral", "eletronicos", "livros"]


def listar_produtos():
    produtos = produto_model.get_todos_produtos(current_app.db)
    return jsonify({"dados": produtos, "sucesso": True}), 200


def buscar_produto(id):
    produto = produto_model.get_produto_por_id(current_app.db, id)
    if produto:
        return jsonify({"dados": produto, "sucesso": True}), 200
    return jsonify({"erro": "Produto não encontrado", "sucesso": False}), 404


def _validar_dados_produto(dados):
    for campo in ("nome", "preco", "estoque"):
        if campo not in dados:
            return f"{campo.capitalize()} é obrigatório"

    if dados["preco"] < 0:
        return "Preço não pode ser negativo"
    if dados["estoque"] < 0:
        return "Estoque não pode ser negativo"
    if len(dados["nome"]) < 2:
        return "Nome muito curto"
    if len(dados["nome"]) > 200:
        return "Nome muito longo"

    categoria = dados.get("categoria", "geral")
    if categoria not in CATEGORIAS_VALIDAS:
        return f"Categoria inválida. Válidas: {CATEGORIAS_VALIDAS}"

    return None


def criar_produto():
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Dados inválidos"}), 400

    erro = _validar_dados_produto(dados)
    if erro:
        return jsonify({"erro": erro}), 400

    id = produto_model.criar_produto(
        current_app.db,
        dados["nome"],
        dados.get("descricao", ""),
        dados["preco"],
        dados["estoque"],
        dados.get("categoria", "geral"),
    )
    current_app.logger.info("Produto criado com ID: %s", id)
    return jsonify({"dados": {"id": id}, "sucesso": True, "mensagem": "Produto criado"}), 201


def atualizar_produto(id):
    produto_existente = produto_model.get_produto_por_id(current_app.db, id)
    if not produto_existente:
        return jsonify({"erro": "Produto não encontrado"}), 404

    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Dados inválidos"}), 400

    erro = _validar_dados_produto(dados)
    if erro:
        return jsonify({"erro": erro}), 400

    produto_model.atualizar_produto(
        current_app.db,
        id,
        dados["nome"],
        dados.get("descricao", ""),
        dados["preco"],
        dados["estoque"],
        dados.get("categoria", "geral"),
    )
    return jsonify({"sucesso": True, "mensagem": "Produto atualizado"}), 200


def deletar_produto(id):
    produto = produto_model.get_produto_por_id(current_app.db, id)
    if not produto:
        return jsonify({"erro": "Produto não encontrado"}), 404

    produto_model.deletar_produto(current_app.db, id)
    current_app.logger.info("Produto %s deletado", id)
    return jsonify({"sucesso": True, "mensagem": "Produto deletado"}), 200


def buscar_produtos():
    termo = request.args.get("q", "")
    categoria = request.args.get("categoria", None)
    preco_min = request.args.get("preco_min", None)
    preco_max = request.args.get("preco_max", None)

    if preco_min:
        preco_min = float(preco_min)
    if preco_max:
        preco_max = float(preco_max)

    resultados = produto_model.buscar_produtos(current_app.db, termo, categoria, preco_min, preco_max)
    return jsonify({"dados": resultados, "total": len(resultados), "sucesso": True}), 200
