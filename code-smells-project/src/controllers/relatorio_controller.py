from flask import current_app, jsonify

from src.models import pedido_model


def _calcular_desconto(faturamento):
    if faturamento > 10000:
        return faturamento * 0.1
    if faturamento > 5000:
        return faturamento * 0.05
    if faturamento > 1000:
        return faturamento * 0.02
    return 0


def relatorio_vendas():
    stats = pedido_model.get_estatisticas_vendas(current_app.db)
    faturamento = stats["faturamento_bruto"]
    total_pedidos = stats["total_pedidos"]
    desconto = _calcular_desconto(faturamento)

    relatorio = {
        "total_pedidos": total_pedidos,
        "faturamento_bruto": round(faturamento, 2),
        "desconto_aplicavel": round(desconto, 2),
        "faturamento_liquido": round(faturamento - desconto, 2),
        "pedidos_pendentes": stats["pedidos_pendentes"],
        "pedidos_aprovados": stats["pedidos_aprovados"],
        "pedidos_cancelados": stats["pedidos_cancelados"],
        "ticket_medio": round(faturamento / total_pedidos, 2) if total_pedidos > 0 else 0,
    }
    return jsonify({"dados": relatorio, "sucesso": True}), 200
