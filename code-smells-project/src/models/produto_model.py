def get_todos_produtos(db):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM produtos")
    return [dict(row) for row in cursor.fetchall()]


def get_produto_por_id(db, id):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM produtos WHERE id = ?", (id,))
    row = cursor.fetchone()
    return dict(row) if row else None


def criar_produto(db, nome, descricao, preco, estoque, categoria):
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO produtos (nome, descricao, preco, estoque, categoria) VALUES (?, ?, ?, ?, ?)",
        (nome, descricao, preco, estoque, categoria),
    )
    db.commit()
    return cursor.lastrowid


def atualizar_produto(db, id, nome, descricao, preco, estoque, categoria):
    cursor = db.cursor()
    cursor.execute(
        "UPDATE produtos SET nome = ?, descricao = ?, preco = ?, estoque = ?, categoria = ? WHERE id = ?",
        (nome, descricao, preco, estoque, categoria, id),
    )
    db.commit()
    return True


def deletar_produto(db, id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM produtos WHERE id = ?", (id,))
    db.commit()
    return True


def buscar_produtos(db, termo, categoria=None, preco_min=None, preco_max=None):
    cursor = db.cursor()
    query = "SELECT * FROM produtos WHERE 1=1"
    params = []

    if termo:
        query += " AND (nome LIKE ? OR descricao LIKE ?)"
        params.extend([f"%{termo}%", f"%{termo}%"])
    if categoria:
        query += " AND categoria = ?"
        params.append(categoria)
    if preco_min:
        query += " AND preco >= ?"
        params.append(preco_min)
    if preco_max:
        query += " AND preco <= ?"
        params.append(preco_max)

    cursor.execute(query, params)
    return [dict(row) for row in cursor.fetchall()]
