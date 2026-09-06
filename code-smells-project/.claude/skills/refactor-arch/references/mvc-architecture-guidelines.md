# Guidelines de Arquitetura MVC Alvo (Fase 3)

Regras de camada agnósticas de tecnologia, mais o mapeamento concreto para os dois ecossistemas cobertos pelos projetos deste desafio (Python/Flask e Node.js/Express). Para outra stack, aplique as mesmas regras de camada usando a convenção idiomática equivalente do framework detectado na Fase 1.

## Regras de camada (agnósticas)

- **Model**: só acessa e valida dados de uma única entidade/domínio. Não conhece HTTP (sem `request`/`response`), não decide o que fazer em caso de erro de negócio — apenas representa e persiste o dado, e expõe métodos de consulta/validação puros (ex.: `is_overdue()`).
- **View / Routes**: só faz parsing da requisição (path params, query params, body), chama o Controller correspondente, e formata a resposta (status code + serialização). Não contém regra de negócio, não acessa o banco diretamente.
- **Controller**: orquestra um ou mais Models/Services para executar um caso de uso completo, concentra a regra de negócio (validações de domínio, cálculos, decisões condicionais) e retorna um resultado ou erro estruturado para a camada de rota formatar.
- **Config**: única fonte de configuração da aplicação (chaves, URIs de banco, credenciais de serviços externos), sempre lida de variáveis de ambiente — nunca um literal hardcoded no meio do código de negócio.
- **Middleware/Error handling**: um único ponto central de tratamento de erro por aplicação, que captura exceções não tratadas e produz uma resposta de erro consistente (nunca `except:`/`catch` genérico espalhado pelos handlers).
- **Entry point**: um único arquivo (`main.py`/`app.py`/`app.js`) que monta a aplicação (composition root) — carrega config, registra rotas/middlewares, e inicia o servidor. Não deve conter lógica de negócio.

## Mapeamento para Flask (Python)

| Camada | Convenção |
|---|---|
| Model | `models/<dominio>.py` — classe/funções de acesso a dados desse domínio |
| Routes (View) | `routes/<dominio>_routes.py` (Blueprint) — parsing + chamada ao controller + `jsonify` |
| Controller | `controllers/<dominio>_controller.py` — regra de negócio, chamado pela rota |
| Config | `config/settings.py` — lê `os.environ`, expõe `SECRET_KEY`, `DATABASE_URI`, etc. |
| Middleware/erro | `middlewares/error_handler.py` — registrado via `@app.errorhandler(Exception)` no entry point |
| Entry point | `app.py` (ou `main.py`) — `create_app()` que monta tudo e é chamado no `if __name__ == "__main__":` |

## Mapeamento para Express (Node.js)

| Camada | Convenção |
|---|---|
| Model | `src/models/<dominio>Model.js` — funções/classe de acesso a dados desse domínio |
| Routes (View) | `src/routes/<dominio>Routes.js` — `express.Router()`, parsing + chamada ao controller |
| Controller | `src/controllers/<dominio>Controller.js` — regra de negócio, chamado pela rota |
| Config | `src/config/index.js` — lê `process.env` (via `dotenv`), exporta objeto de config |
| Middleware/erro | `src/middlewares/errorHandler.js` — `app.use((err, req, res, next) => {...})`, montado por último |
| Entry point | `src/app.js` — cria `express()`, registra middlewares/rotas, chama `.listen()` |

## Regras de decisão ao refatorar

1. **Um arquivo de Model por domínio de negócio** identificado na Fase 1 (ex.: produto, usuário, pedido → 3 arquivos de model, não 1).
2. **Toda regra de negócio que hoje vive dentro de uma rota ou de um Model vira Controller** — Model fica só com acesso a dados e validações de campo; Controller decide o que fazer com esse dado.
3. **Toda leitura de segredo/config hardcoded migra para `config/`**, lendo de variável de ambiente, com um `.env.example` documentando as chaves esperadas (valores placeholder, nunca o valor real antigo).
4. **Endpoints administrativos/sensíveis identificados no catálogo (#3) recebem um guard de autenticação explícito** na camada de rota, antes de chamar o controller.
5. **Um endpoint cuja única função é executar código arbitrário vindo da requisição (ex.: `/admin/query` executando SQL livre) é removido**, não adaptado — documentar essa decisão no relatório final, não é uma regressão da refatoração.
6. **Um único middleware de erro por aplicação**, registrado no entry point, substituindo todo `try/except`/`try/catch` genérico espalhado pelos handlers antigos.

## Validação da Fase 3

Depois de aplicar a refatoração, a aplicação deve ser validada antes de considerar a Fase 3 concluída:

1. Subir a aplicação em background (respeitando a porta padrão do projeto), com timeout.
2. Fazer polling em um endpoint leve (ex.: `/` ou `/health`) até responder, ou até o timeout estourar.
3. Reexercitar a lista de endpoints capturada nas Fases 1/2 com um payload mínimo válido para cada método.
4. Checar ausência de respostas 5xx nesses endpoints (um 4xx esperado, ex. "não encontrado", não é falha).
5. Encerrar o processo/porta ao final da validação, mesmo se algum passo falhar.
6. Imprimir uma tabela PASS/FAIL por endpoint, nunca só um booleano único de "funcionou/não funcionou".
