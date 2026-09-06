def criar_item_pedido(db, pedido_id, produto_id, quantidade, preco_unitario):
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO itens_pedido (pedido_id, produto_id, quantidade, preco_unitario) VALUES (?, ?, ?, ?)",
        (pedido_id, produto_id, quantidade, preco_unitario),
    )
    db.commit()
    return cursor.lastrowid


def get_itens_por_pedidos(db, pedido_ids):
    """Busca os itens de uma lista de pedidos em uma única query (evita N+1)."""
    if not pedido_ids:
        return {}

    cursor = db.cursor()
    placeholders = ",".join("?" for _ in pedido_ids)
    cursor.execute(
        f"""
        SELECT itens_pedido.pedido_id, itens_pedido.produto_id, itens_pedido.quantidade,
               itens_pedido.preco_unitario, produtos.nome AS produto_nome
        FROM itens_pedido
        JOIN produtos ON produtos.id = itens_pedido.produto_id
        WHERE itens_pedido.pedido_id IN ({placeholders})
        """,
        pedido_ids,
    )

    itens_por_pedido = {}
    for row in cursor.fetchall():
        itens_por_pedido.setdefault(row["pedido_id"], []).append({
            "produto_id": row["produto_id"],
            "produto_nome": row["produto_nome"],
            "quantidade": row["quantidade"],
            "preco_unitario": row["preco_unitario"],
        })
    return itens_por_pedido
