from functools import wraps

from flask import current_app, jsonify, request


def require_admin_auth(handler):
    """Guard simples baseado em token para rotas administrativas.

    Um cenário de produção real usaria um esquema de autenticação completo
    (sessão, OAuth, JWT com roles) — este guard existe para demonstrar o
    ponto de checagem de autorização que faltava antes da refatoração,
    mantendo o escopo do exercício.
    """

    @wraps(handler)
    def wrapper(*args, **kwargs):
        token = request.headers.get("X-Admin-Token")
        if not token or token != current_app.config["ADMIN_TOKEN"]:
            return jsonify({"erro": "Não autorizado"}), 401
        return handler(*args, **kwargs)

    return wrapper
