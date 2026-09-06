# ecommerce-api-legacy

LMS API (com fluxo de checkout) em Node.js/Express, refatorada para o padrão MVC pela skill `refactor-arch` (ver `.claude/skills/refactor-arch/` e o relatório de auditoria em `../reports/audit-project-2.md`).

## Estrutura

```
src/
├── app.js                # composition root + entry point
├── config/index.js       # configuração via variável de ambiente (dotenv)
├── database/db.js        # factory de conexão + helpers promisificados
├── models/                # acesso a dados por domínio
├── controllers/           # regra de negócio por domínio
├── routes/                 # registro de rotas por domínio
├── middlewares/            # error handler central + guard de auth admin
├── services/cacheService.js  # cache encapsulado (substitui estado global mutável)
└── utils/crypto.js        # hashing de senha real (bcryptjs)
```

## Como rodar

```bash
npm install
cp .env.example .env   # ajuste os valores antes de subir em produção
npm start
```

A aplicação sobe em `http://localhost:3000`. O banco SQLite é em memória e já carrega seeds automaticamente no boot.

> `GET /api/admin/financial-report` agora exige o header `X-Admin-Token` (valor de `ADMIN_TOKEN` no `.env`). `DELETE /api/users/:id` agora remove matrículas e pagamentos associados (cascade explícito) antes de remover o usuário.

Exemplos de requisições estão em `api.http`.
