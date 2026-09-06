# code-smells-project

API de E-commerce em Python/Flask, refatorada para o padrão MVC pela skill `refactor-arch` (ver `.claude/skills/refactor-arch/` e o relatório de auditoria em `../reports/audit-project-1.md`).

## Estrutura

```
src/
├── app.py                # composition root (create_app)
├── config/settings.py    # configuração via variável de ambiente
├── database.py           # factory de conexão + schema + seed
├── models/                # acesso a dados por domínio
├── controllers/           # regra de negócio por domínio
├── views/routes.py        # registro de rotas
└── middlewares/           # error handler central + guard de auth admin
main.py                   # entry point
```

## Como rodar

```bash
pip install -r requirements.txt
cp .env.example .env   # ajuste os valores antes de subir em produção
python main.py
```

A aplicação sobe em `http://localhost:5000`. O banco SQLite (`loja.db`) é criado automaticamente no primeiro boot, já com produtos e usuários de exemplo (senhas hasheadas).

> O endpoint `/admin/reset-db` agora exige o header `X-Admin-Token` (valor de `ADMIN_TOKEN` no `.env`). O endpoint `/admin/query`, que executava SQL arbitrário vindo da requisição sem autenticação, foi **removido** na refatoração — ver justificativa no relatório de auditoria.
