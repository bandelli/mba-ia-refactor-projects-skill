from flask import current_app, jsonify


def index():
    return jsonify({
        "mensagem": "Bem-vindo à API da Loja",
        "versao": "1.0.0",
        "endpoints": {
            "produtos": "/produtos",
            "usuarios": "/usuarios",
            "pedidos": "/pedidos",
            "login": "/login",
            "relatorios": "/relatorios/vendas",
            "health": "/health",
        },
    })


def health_check():
    try:
        cursor = current_app.db.cursor()
        cursor.execute("SELECT COUNT(*) FROM produtos")
        produtos = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        usuarios = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM pedidos")
        pedidos = cursor.fetchone()[0]

        return jsonify({
            "status": "ok",
            "database": "connected",
            "counts": {"produtos": produtos, "usuarios": usuarios, "pedidos": pedidos},
            "versao": "1.0.0",
        }), 200
    except Exception:
        current_app.logger.exception("Health check falhou")
        return jsonify({"status": "erro", "database": "disconnected"}), 500


def reset_database():
    cursor = current_app.db.cursor()
    cursor.execute("DELETE FROM itens_pedido")
    cursor.execute("DELETE FROM pedidos")
    cursor.execute("DELETE FROM produtos")
    cursor.execute("DELETE FROM usuarios")
    current_app.db.commit()
    current_app.logger.warning("Banco de dados resetado via /admin/reset-db")
    return jsonify({"mensagem": "Banco de dados resetado", "sucesso": True}), 200
