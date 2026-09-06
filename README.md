# refactor-arch — Skill de Auditoria e Refatoração Arquitetural

Este repositório contém a entrega de um desafio de MBA: uma Claude Code Custom Skill (`refactor-arch`) capaz de analisar qualquer codebase, auditá-la contra um catálogo de anti-patterns e refatorá-la para o padrão MVC — de forma agnóstica de tecnologia. A skill é validada em três projetos legados de exemplo: `code-smells-project/` (Python/Flask), `ecommerce-api-legacy/` (Node.js/Express) e `task-manager-api/` (Python/Flask, parcialmente organizado).

## Escala de Severidade

As auditorias (manual e automatizada) usam a seguinte escala, baseada em violações de MVC e SOLID:

- **CRITICAL** — falhas graves de arquitetura ou segurança que impedem o funcionamento correto, expõem dados sensíveis ou violam completamente a separação de responsabilidades.
- **HIGH** — fortes violações do padrão MVC/SOLID que dificultam muito manutenção e testes.
- **MEDIUM** — problemas de padronização, duplicação de código ou gargalos de performance moderada.
- **LOW** — melhorias de legibilidade, nomenclatura ruim ou "magic numbers".

## A. Análise Manual

Levantamento feito por leitura direta do código dos 3 projetos, antes da construção da skill, para servir de base de comparação com o que a Fase 2 (Auditoria) da skill deveria encontrar.

### 1. code-smells-project (Python/Flask 3.1.1 + flask-cors)

**[CRITICAL] SQL Injection generalizada por concatenação de string**
- Arquivo: `code-smells-project/models.py:28,48-50,58-61,68,92,109-111,126-129,140,148-151,155,158-161,163-166,174,188,192,206-207,220,224,280,291-297`
- Descrição: praticamente toda função de acesso a dados monta a query SQL concatenando strings com valores vindos direto da requisição (ex.: `"SELECT * FROM produtos WHERE id = " + str(id)`), sem parâmetros preparados.
- Justificativa: qualquer campo de texto (nome, categoria, termo de busca) pode ser usado para injetar SQL arbitrário e ler/alterar/apagar dados do banco inteiro.

**[CRITICAL] Endpoint `/admin/query` executa SQL arbitrário vindo do request, sem autenticação**
- Arquivo: `code-smells-project/app.py:59-78`
- Descrição: o handler `executar_query()` pega `dados.get("sql", "")` do corpo da requisição e chama `cursor.execute(query)` diretamente, sem nenhuma checagem de identidade/role.
- Justificativa: é literalmente um console SQL exposto na internet — qualquer pessoa pode ler, alterar ou apagar todo o banco.

**[CRITICAL] Credenciais hardcoded e modo debug ligado em produção**
- Arquivo: `code-smells-project/app.py:7-8,88`
- Descrição: `SECRET_KEY = "minha-chave-super-secreta-123"` fixo no código-fonte e `app.run(..., debug=True)`.
- Justificativa: uma `SECRET_KEY` fixa e pública no repositório quebra a segurança de sessão/assinatura da aplicação; `debug=True` expõe stack traces e o debugger interativo do Werkzeug em produção.

**[HIGH] God Module concentrando 4 domínios de negócio**
- Arquivo: `code-smells-project/models.py:1-315`
- Descrição: um único arquivo contém acesso a dados, regra de negócio e serialização para produtos, usuários, pedidos e itens de pedido.
- Justificativa: viola a separação de responsabilidades do MVC (Model deveria ser só dados/validação por domínio); qualquer mudança em um domínio arrisca quebrar os outros três, e o arquivo é impossível de testar em isolamento.

**[MEDIUM] Query N+1 na listagem de pedidos**
- Arquivo: `code-smells-project/models.py:171-201,203-233`
- Descrição: `get_pedidos_usuario()` e `get_todos_pedidos()` fazem um laço por pedido, abrindo um novo cursor para buscar os itens (`cursor2`) e, dentro dele, mais um cursor por item para buscar o nome do produto (`cursor3`).
- Justificativa: para N pedidos com M itens cada, isso gera 1 + N + N×M queries em vez de 2-3 queries com JOIN — degrada rapidamente com o crescimento da base.

**[MEDIUM] Vazamento de dados sensíveis em endpoint público**
- Arquivo: `code-smells-project/controllers.py:276-290`
- Descrição: `health_check()` retorna no JSON público `"db_path": "loja.db"`, `"debug": True` e `"secret_key": "minha-chave-super-secreta-123"`.
- Justificativa: um endpoint de saúde, tipicamente sem autenticação, está vazando a chave secreta da aplicação e detalhes de infraestrutura.

**[LOW] Logging ad-hoc via `print()` em vez de logger estruturado**
- Arquivo: `code-smells-project/controllers.py:8,11,57,61,106,161,179,182,208-210,219,248-250`
- Descrição: mensagens de operação e erro são emitidas com `print()` espalhado pelos controllers, sem nível de log, timestamp ou destino configurável.
- Justificativa: dificulta observabilidade em produção (não dá para filtrar por severidade, redirecionar para um serviço de logs, etc.).

**[LOW] Senha armazenada e comparada em texto plano**
- Arquivo: `code-smells-project/database.py:75-79`, `code-smells-project/models.py:105-120`
- Descrição: os usuários de seed são criados com senha em texto plano (`"admin123"`, `"123456"`, `"senha123"`) e `login_usuario()` compara a senha recebida diretamente contra o valor salvo, sem hashing.
- Justificativa: qualquer vazamento do banco expõe todas as senhas dos usuários diretamente; classificado LOW aqui apenas porque o projeto já tem um problema CRITICAL de SQL Injection que expõe o banco de qualquer forma — em um projeto sem esse agravante, isso seria HIGH.

### 2. ecommerce-api-legacy (Node.js/Express ^4.18.2 + sqlite3)

**[CRITICAL] Segredos de produção hardcoded no código-fonte**
- Arquivo: `ecommerce-api-legacy/src/utils.js:1-7`
- Descrição: o objeto `config` tem `dbPass: "senha_super_secreta_prod_123"` e `paymentGatewayKey: "pk_live_1234567890abcdef"` (formato de chave *live* de gateway de pagamento) fixos no código.
- Justificativa: qualquer pessoa com acesso ao repositório tem a chave de um gateway de pagamento de produção e a senha do banco.

**[CRITICAL] Hash de senha falso**
- Arquivo: `ecommerce-api-legacy/src/utils.js:17-23`
- Descrição: `badCrypto()` não é uma função de hash — repete 10.000 vezes uma conversão para base64 e concatena os 2 primeiros caracteres, produzindo uma string curta e reversível na prática.
- Justificativa: não oferece nenhuma proteção real contra vazamento de senha; usada para gerar `pass` no cadastro de usuário durante o checkout.

**[HIGH] God Class `AppManager` misturando DB, rotas e 3 fluxos de negócio**
- Arquivo: `ecommerce-api-legacy/src/AppManager.js:1-141`
- Descrição: uma única classe cuida de schema/seed do banco (`initDb`), roteamento (`setupRoutes`) e a lógica completa de checkout, relatório financeiro e exclusão de usuário.
- Justificativa: impede testar cada fluxo isoladamente e concentra todo o risco de regressão em um único arquivo.

**[HIGH] Lógica de negócio pesada dentro do route handler, em pirâmide de callbacks**
- Arquivo: `ecommerce-api-legacy/src/AppManager.js:28-78`
- Descrição: o handler de `POST /api/checkout` aninha callbacks de banco em até 5 níveis, misturando busca de curso, criação de usuário, "processamento" de pagamento (`cc.startsWith("4")`), matrícula e log de auditoria tudo dentro da própria rota.
- Justificativa: viola a separação Controller/Model do MVC; qualquer erro de um passo intermediário é fácil de esquecer de tratar (ex.: nem todo `err` de callback é verificado), e o fluxo é muito difícil de testar unitariamente.

**[MEDIUM] Query N+1 aninhada com controle manual de conclusão assíncrona**
- Arquivo: `ecommerce-api-legacy/src/AppManager.js:80-129`
- Descrição: `/api/admin/financial-report` busca cursos, depois matrículas por curso, depois usuário e pagamento por matrícula — tudo com callbacks aninhados e contadores manuais (`coursesPending`, `enrPending`) para saber quando a resposta pode ser enviada.
- Justificativa: além do problema de performance (N+1), o controle manual de contagem é frágil — qualquer callback que não decrementa o contador trava a resposta indefinidamente.

**[MEDIUM] Exclusão de usuário sem cascade, gerando dados órfãos**
- Arquivo: `ecommerce-api-legacy/src/AppManager.js:131-137`
- Descrição: `DELETE /api/users/:id` remove a linha de `users` sem tratar `enrollments`/`payments` associados; a própria resposta da API admite isso: `"...matrículas e pagamentos ficaram sujos no banco."`.
- Justificativa: corrompe a integridade referencial do banco a cada exclusão de usuário.

**[LOW] Estado global mutável em nível de módulo**
- Arquivo: `ecommerce-api-legacy/src/utils.js:9-10`
- Descrição: `globalCache` e `totalRevenue` são variáveis mutáveis no escopo do módulo, compartilhadas entre todas as requisições.
- Justificativa: em qualquer cenário com mais de um processo/instância (ou testes concorrentes), esse estado gera condições de corrida e resultados inconsistentes.

**[LOW] Tratamento de erro ad hoc, sem middleware centralizado**
- Arquivo: `ecommerce-api-legacy/src/AppManager.js:38,41,51,55,84`
- Descrição: cada callback trata erro chamando `res.status(500).send("Erro DB")` (ou variações) individualmente, sem um middleware de erro único.
- Justificativa: mensagens de erro inconsistentes para o cliente e lógica de tratamento duplicada em todos os pontos de falha.

### 3. task-manager-api (Python/Flask 3.0.0 + Flask-SQLAlchemy, parcialmente organizado)

**[CRITICAL] Hash de senha com MD5**
- Arquivo: `task-manager-api/models/user.py:29,32`
- Descrição: `set_password()`/`check_password()` usam `hashlib.md5(pwd.encode()).hexdigest()` para armazenar e validar senha.
- Justificativa: MD5 é um algoritmo de hash criptograficamente quebrado para uso em senhas (rápido de forçar bruta e sem salt) — é um dos itens de API/prática deprecated mais citados em auditorias de segurança.

**[CRITICAL] Emissão de token de autenticação falso**
- Arquivo: `task-manager-api/routes/user_routes.py:210`
- Descrição: o endpoint de login retorna `'token': 'fake-jwt-token-' + str(user.id)` — uma string previsível, não assinada e sem expiração.
- Justificativa: qualquer cliente pode forjar um token válido para qualquer `user_id` só concatenando o prefixo, quebrando toda a autenticação da API.

**[HIGH] `SECRET_KEY` hardcoded**
- Arquivo: `task-manager-api/app.py:13`
- Descrição: `app.config['SECRET_KEY'] = 'super-secret-key-123'` fixo no código-fonte, junto com `debug=True` em `app.run(...)` (linha 34).
- Justificativa: mesma classe de risco do projeto 1 — chave de sessão pública e debugger exposto.

**[HIGH] Credenciais SMTP hardcoded no código-fonte**
- Arquivo: `task-manager-api/services/notification_service.py:9-10`
- Descrição: `self.email_user` e `self.email_password` (`'senha123'`) são atribuídos como literais na classe `NotificationService`.
- Justificativa: expõe credenciais de uma conta de e-mail real (`taskmanager@gmail.com`) a qualquer pessoa com acesso ao repositório.

**[MEDIUM] Query N+1 na listagem de tasks**
- Arquivo: `task-manager-api/routes/task_routes.py:41-57`
- Descrição: `get_tasks()` itera todas as tasks e, para cada uma, chama `User.query.get(t.user_id)` e `Category.query.get(t.category_id)` individualmente em vez de usar `joinedload`/`selectinload`.
- Justificativa: uma listagem de N tasks gera até 1 + 2N queries em vez de 1 query com join.

**[MEDIUM] Lógica de "overdue" duplicada em 3 arquivos, ignorando método já existente**
- Arquivo: `task-manager-api/routes/task_routes.py:30-39`, `task-manager-api/routes/user_routes.py:171-180`, `task-manager-api/routes/report_routes.py:34-43` (vs. `task-manager-api/models/task.py:50-60`)
- Descrição: o mesmo bloco de `if due_date < utcnow() and status not in (done, cancelled)` é reescrito manualmente em 3 rotas diferentes, enquanto `Task.is_overdue()` já existe no model e não é chamado em nenhum lugar.
- Justificativa: viola DRY — qualquer mudança na regra de "atrasado" (ex.: considerar fuso horário) precisa ser replicada em 3 lugares, com alto risco de ficar inconsistente.

**[LOW] `except:` genérico engolindo exceções**
- Arquivo: `task-manager-api/routes/task_routes.py:62`
- Descrição: `get_tasks()` envolve toda a lógica num `try/except:` sem tipo, retornando sempre `{'error': 'Erro interno'}` e descartando a exceção real (sem log).
- Justificativa: torna erros de produção praticamente impossíveis de diagnosticar — qualquer bug vira a mesma mensagem genérica.

**[LOW] Ausência de paginação nas listagens**
- Arquivo: `task-manager-api/routes/task_routes.py:14`, `task-manager-api/routes/user_routes.py:12`
- Descrição: `get_tasks()` e `get_users()` retornam `Task.query.all()` / `User.query.all()` sem parâmetros de `page`/`limit`.
- Justificativa: à medida que a base cresce, esses endpoints degradam performance e podem estourar memória/tempo de resposta.

## B. Construção da Skill

_A preencher após a Fase F2 do handoff de execução (`.doc/HANDOFF.md`): decisões de design da skill `refactor-arch`, anti-patterns incluídos e por quê, como a skill garante agnosticismo de tecnologia, e desafios encontrados na construção._

## C. Resultados

_A preencher após a execução da skill nos 3 projetos (Fases F3, F5, F6 do handoff): resumo dos relatórios de auditoria (`reports/audit-project-{1,2,3}.md`), comparação antes/depois, checklist de validação do PRD preenchido, e evidência dos 3 gates humanos de confirmação (pergunta feita à revisora + resposta literal) exigidos antes de cada Fase 3._

## D. Como Executar

_A preencher na Fase F8 do handoff de execução: pré-requisitos, comando para rodar a skill em cada um dos 3 projetos e como validar que a refatoração funcionou._
