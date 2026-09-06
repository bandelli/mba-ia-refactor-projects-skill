# task-manager-api

API de Task Manager em Python/Flask, refatorada para o padrão MVC pela skill `refactor-arch` (ver `.claude/skills/refactor-arch/` e o relatório de auditoria em `../reports/audit-project-3.md`).

## Estrutura

```
app.py                 # composition root + entry point
config/settings.py     # configuração via variável de ambiente
database.py            # instância do SQLAlchemy
models/                # entidades (user, task, category) — hashing real de senha
controllers/           # regra de negócio por domínio (extraída das rotas)
routes/                 # camada fina: parse -> controller -> jsonify
services/               # notification_service (credenciais via env)
middlewares/            # error handler central
utils/                  # helpers de validação + emissão de JWT (auth.py)
```

## Como rodar

```bash
pip install -r requirements.txt
cp .env.example .env   # ajuste os valores antes de subir em produção
python seed.py
python app.py
```

A aplicação sobe em `http://localhost:5000`. O `seed.py` popula o banco SQLite (`tasks.db`) com usuários, categorias e tasks de exemplo — **rode-o antes do primeiro boot**, caso contrário os endpoints vão retornar listas vazias.

> `GET /tasks` e `GET /users` agora retornam resultados paginados (`{"items": [...], "page", "per_page", "total", "pages"}`) em vez de uma lista crua — use `?page=&per_page=` para navegar. `POST /login` agora retorna um JWT real e assinado (antes era uma string fixa previsível).
