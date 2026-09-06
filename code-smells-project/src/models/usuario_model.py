def get_todos_usuarios(db):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM usuarios")
    return [dict(row) for row in cursor.fetchall()]


def get_usuario_por_id(db, id):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE id = ?", (id,))
    row = cursor.fetchone()
    return dict(row) if row else None


def get_usuario_por_email(db, email):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
    row = cursor.fetchone()
    return dict(row) if row else None


def criar_usuario(db, nome, email, senha_hash, tipo="cliente"):
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO usuarios (nome, email, senha, tipo) VALUES (?, ?, ?, ?)",
        (nome, email, senha_hash, tipo),
    )
    db.commit()
    return cursor.lastrowid
