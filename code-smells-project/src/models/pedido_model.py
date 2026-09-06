from src.models import item_pedido_model


def _montar_pedidos(db, where_clause="", params=()):
    cursor = db.cursor()
    query = "SELECT * FROM pedidos"
    if where_clause:
        query += " WHERE " + where_clause
    cursor.execute(query, params)
    pedidos_rows = cursor.fetchall()
    if not pedidos_rows:
        return []

    pedido_ids = [row["id"] for row in pedidos_rows]
    itens_por_pedido = item_pedido_model.get_itens_por_pedidos(db, pedido_ids)

    return [
        {
            "id": row["id"],
            "usuario_id": row["usuario_id"],
            "status": row["status"],
            "total": row["total"],
            "criado_em": row["criado_em"],
            "itens": itens_por_pedido.get(row["id"], []),
        }
        for row in pedidos_rows
    ]


def get_pedidos_usuario(db, usuario_id):
    return _montar_pedidos(db, "usuario_id = ?", (usuario_id,))


def get_todos_pedidos(db):
    return _montar_pedidos(db)


def criar_pedido(db, usuario_id, itens):
    cursor = db.cursor()
    total = 0
    produtos_por_id = {}

    for item in itens:
        cursor.execute("SELECT * FROM produtos WHERE id = ?", (item["produto_id"],))
        produto = cursor.fetchone()
        if produto is None:
            return {"erro": f"Produto {item['produto_id']} não encontrado"}
        if produto["estoque"] < item["quantidade"]:
            return {"erro": f"Estoque insuficiente para {produto['nome']}"}
        produtos_por_id[item["produto_id"]] = dict(produto)
        total += produto["preco"] * item["quantidade"]

    cursor.execute(
        "INSERT INTO pedidos (usuario_id, status, total) VALUES (?, 'pendente', ?)",
        (usuario_id, total),
    )
    pedido_id = cursor.lastrowid

    for item in itens:
        produto = produtos_por_id[item["produto_id"]]
        item_pedido_model.criar_item_pedido(
            db, pedido_id, item["produto_id"], item["quantidade"], produto["preco"]
        )
        cursor.execute(
            "UPDATE produtos SET estoque = estoque - ? WHERE id = ?",
            (item["quantidade"], item["produto_id"]),
        )

    db.commit()
    return {"pedido_id": pedido_id, "total": total}


def atualizar_status_pedido(db, pedido_id, novo_status):
    cursor = db.cursor()
    cursor.execute("UPDATE pedidos SET status = ? WHERE id = ?", (novo_status, pedido_id))
    db.commit()
    return True


def get_estatisticas_vendas(db):
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM pedidos")
    total_pedidos = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(total) FROM pedidos")
    faturamento = cursor.fetchone()[0] or 0

    cursor.execute("SELECT COUNT(*) FROM pedidos WHERE status = ?", ("pendente",))
    pendentes = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM pedidos WHERE status = ?", ("aprovado",))
    aprovados = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM pedidos WHERE status = ?", ("cancelado",))
    cancelados = cursor.fetchone()[0]

    return {
        "total_pedidos": total_pedidos,
        "faturamento_bruto": faturamento,
        "pedidos_pendentes": pendentes,
        "pedidos_aprovados": aprovados,
        "pedidos_cancelados": cancelados,
    }
