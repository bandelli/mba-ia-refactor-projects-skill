# Playbook de Refatoração (Fase 3)

Cada padrão abaixo ataca um anti-pattern do `anti-patterns-catalog.md` (referenciado pelo número `#`). Cada padrão é descrito de forma estrutural, com um exemplo Python e um exemplo Node.js lado a lado — isso é o que garante que o mesmo playbook funcione nas duas stacks (e, por extensão, em qualquer outra, aplicando a mesma transformação estrutural na sintaxe do ecossistema encontrado).

## P1 — Externalizar segredos para config via variável de ambiente
**Ataca**: #1 (Hardcoded Credentials), contribui para #10 (Vazamento em resposta pública)

Antes (Python):
```python
app.config["SECRET_KEY"] = "minha-chave-super-secreta-123"
```
Depois (Python):
```python
# config/settings.py
import os
SECRET_KEY = os.environ["SECRET_KEY"]
```

Antes (Node.js):
```javascript
const config = { dbPass: "senha_super_secreta_prod_123" };
```
Depois (Node.js):
```javascript
// src/config/index.js
require('dotenv').config();
module.exports = { dbPass: process.env.DB_PASS };
```

Sempre criar um `.env.example` com placeholders óbvios (`SECRET_KEY=CHANGE_ME`), nunca reaproveitando o valor hardcoded antigo.

## P2 — Parametrizar SQL / remover execução de SQL livre
**Ataca**: #2 (SQL Injection / Execução Arbitrária)

Antes (Python):
```python
cursor.execute("SELECT * FROM produtos WHERE id = " + str(id))
```
Depois (Python):
```python
cursor.execute("SELECT * FROM produtos WHERE id = ?", (id,))
```

Antes (Node.js):
```javascript
db.all("SELECT * FROM courses WHERE title = '" + title + "'");
```
Depois (Node.js):
```javascript
db.all("SELECT * FROM courses WHERE title = ?", [title]);
```

Se o anti-pattern for um endpoint que executa SQL vindo diretamente do body da requisição (`/admin/query`), o endpoint é **removido**, não parametrizado — não existe forma segura de expor execução de SQL arbitrário a partir de input externo.

## P3 — Guard de autenticação em rotas sensíveis
**Ataca**: #3 (Endpoint Sensível sem Autenticação)

Antes (Python):
```python
@app.route("/admin/reset-db", methods=["POST"])
def reset_database():
    ...
```
Depois (Python):
```python
@app.route("/admin/reset-db", methods=["POST"])
@require_admin_auth
def reset_database():
    ...
```

Antes (Node.js):
```javascript
app.get('/api/admin/financial-report', (req, res) => { ... });
```
Depois (Node.js):
```javascript
app.get('/api/admin/financial-report', requireAdminAuth, (req, res) => { ... });
```

## P4 — Separar God Class/Module em Model + Controller por domínio
**Ataca**: #4 (God Class/Module)

Antes (Python): um `models.py` único com SQL cru para produtos, usuários e pedidos misturados.
Depois (Python):
```
models/produto_model.py       # só acesso a dados de produto
controllers/produto_controller.py  # regra de negócio de produto
```

Antes (Node.js): uma classe `AppManager` fazendo setup de DB + rotas + checkout + relatório.
Depois (Node.js):
```
src/models/courseModel.js
src/controllers/checkoutController.js
src/controllers/financialReportController.js
```

## P5 — Hashing de senha real
**Ataca**: #5 (Hashing/Criptografia Falsa)

Antes (Python):
```python
self.password = hashlib.md5(pwd.encode()).hexdigest()
```
Depois (Python):
```python
from werkzeug.security import generate_password_hash, check_password_hash
self.password = generate_password_hash(pwd)
```

Antes (Node.js):
```javascript
function badCrypto(pwd) { /* base64 repetido */ }
```
Depois (Node.js):
```javascript
const bcrypt = require('bcrypt');
const hash = await bcrypt.hash(pwd, 10);
```

## P6 — Estado global mutável → injeção de dependência / app factory
**Ataca**: #6 (Estado Global Mutável)

Antes (Python):
```python
db_connection = None
def get_db():
    global db_connection
    if db_connection is None:
        db_connection = sqlite3.connect(db_path)
    return db_connection
```
Depois (Python):
```python
# database.py
def create_connection(db_path):
    return sqlite3.connect(db_path, check_same_thread=False)
# app.py (composition root)
def create_app():
    app = Flask(__name__)
    app.db = create_connection(settings.DB_PATH)
    return app
```

Antes (Node.js):
```javascript
let globalCache = {};
function logAndCache(key, data) { globalCache[key] = data; }
```
Depois (Node.js):
```javascript
class CacheService {
  constructor() { this.store = {}; }
  set(key, data) { this.store[key] = data; }
}
// instanciado uma vez no composition root e injetado onde for necessário
```

## P7 — Atualizar defaults inseguros / substituir API deprecated
**Ataca**: #7 (Defaults Inseguros / API Deprecated)

Antes (Python):
```python
app.run(host="0.0.0.0", port=5000, debug=True)
```
Depois (Python):
```python
app.run(host="0.0.0.0", port=5000, debug=settings.DEBUG)  # settings.DEBUG vem de env, default False
```

Para APIs deprecated: substituir o símbolo/método deprecated pelo equivalente atual indicado no changelog/release notes da dependência pinada, mantendo o mesmo comportamento observável.

## P8 — Emissão de token assinado real
**Ataca**: #8 (Token Falso/Não Assinado)

Antes (Python):
```python
return jsonify({'token': 'fake-jwt-token-' + str(user.id)})
```
Depois (Python):
```python
import jwt, datetime
token = jwt.encode(
    {'user_id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=8)},
    settings.SECRET_KEY, algorithm='HS256'
)
return jsonify({'token': token})
```

Equivalente Node.js: `jsonwebtoken.sign({ userId: user.id }, config.secretKey, { expiresIn: '8h' })`, validado por um middleware de autenticação central.

## P9 — Eliminar N+1 com eager loading / join único
**Ataca**: #9 (Query N+1)

Antes (Python):
```python
for t in tasks:
    user = User.query.get(t.user_id)
```
Depois (Python):
```python
tasks = Task.query.options(db.joinedload(Task.user), db.joinedload(Task.category)).all()
```

Antes (Node.js):
```javascript
enrollments.forEach(enr => {
    db.get("SELECT name FROM users WHERE id = ?", [enr.user_id], ...);
});
```
Depois (Node.js):
```javascript
const ids = enrollments.map(e => e.user_id);
db.all(`SELECT id, name FROM users WHERE id IN (${ids.map(() => '?').join(',')})`, ids, ...);
```

## P10 — Error handling centralizado
**Ataca**: #11 (Exception Handling Genérico), contribui para #10 (Vazamento em resposta pública)

Antes (Python):
```python
try:
    ...
except:
    return jsonify({'error': 'Erro interno'}), 500
```
Depois (Python):
```python
# middlewares/error_handler.py
@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.exception("Unhandled error")
    return jsonify({'error': 'Erro interno'}), 500
# handlers de rota deixam a exceção subir, sem try/except genérico local
```

Antes (Node.js):
```javascript
this.db.run(sql, params, (err) => { if (err) return res.status(500).send("Erro DB"); });
```
Depois (Node.js):
```javascript
// src/middlewares/errorHandler.js, montado por último em app.js
app.use((err, req, res, next) => {
  console.error(err);
  res.status(500).json({ error: 'Erro interno' });
});
// controllers usam next(err) em vez de responder o erro diretamente
```

## P11 — Extrair lógica duplicada para um único método/função
**Ataca**: #12 (Duplicação de Lógica / Utilitário Morto)

Antes (Python): o mesmo bloco `if due_date < now() and status not in (...)` reescrito em 3 arquivos de rota.
Depois (Python):
```python
# usar o método já existente no model em vez de duplicar
task_data['overdue'] = task.is_overdue()
```

Regra geral: antes de escrever uma nova função utilitária durante a refatoração, procurar se uma equivalente já existe no código (como `is_overdue()` já existia, mas não era chamada) — reaproveitar em vez de recriar.

## P12 — Adicionar paginação
**Ataca**: #13 (Ausência de Paginação)

Antes (Python):
```python
tasks = Task.query.all()
```
Depois (Python):
```python
page = request.args.get('page', 1, type=int)
per_page = request.args.get('per_page', 20, type=int)
tasks = Task.query.paginate(page=page, per_page=per_page, error_out=False).items
```

Equivalente Node.js/SQL: `SELECT * FROM tasks LIMIT ? OFFSET ?` com `limit`/`offset` calculados a partir de `page`/`per_page` recebidos por query string.

## P13 — Logging estruturado em vez de print/console.log
**Ataca**: #14 (Logging Ad-hoc)

Antes (Python): `print("Erro: " + str(e))`
Depois (Python):
```python
import logging
logger = logging.getLogger(__name__)
logger.error("Erro ao processar pedido", exc_info=e)
```

Antes (Node.js): `console.log(...)`
Depois (Node.js): usar um logger configurável (ex.: `winston`/`pino`) com níveis (`info`, `warn`, `error`) e formato estruturado.

## P14 — Cascade explícito no delete
**Ataca**: #15 (Delete sem Cascade)

Antes (Node.js):
```javascript
this.db.run("DELETE FROM users WHERE id = ?", [id], ...);
```
Depois (Node.js):
```javascript
this.db.serialize(() => {
  this.db.run("DELETE FROM payments WHERE enrollment_id IN (SELECT id FROM enrollments WHERE user_id = ?)", [id]);
  this.db.run("DELETE FROM enrollments WHERE user_id = ?", [id]);
  this.db.run("DELETE FROM users WHERE id = ?", [id], ...);
});
```

Equivalente Python/SQLAlchemy: usar `cascade="all, delete-orphan"` na relação do ORM, ou deletar explicitamente os filhos antes do pai dentro da mesma transação.

---

Este playbook tem 14 padrões, cobrindo folgadamente o mínimo de 8 exigido, com cobertura 1:1 contra todos os itens do catálogo de anti-patterns (o item #16, Magic Numbers, é resolvido pela extração pontual de constante nomeada dentro do padrão que estiver sendo aplicado ao trecho, sem um P dedicado).
