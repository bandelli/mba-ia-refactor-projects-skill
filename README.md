# refactor-arch — Skill de Auditoria e Refatoração Arquitetural

Este repositório contém a entrega de um desafio de MBA: uma Claude Code Custom Skill (`refactor-arch`) capaz de analisar qualquer codebase, auditá-la contra um catálogo de anti-patterns e refatorá-la para o padrão MVC — de forma agnóstica de tecnologia. A skill é validada em três projetos legados de exemplo: `code-smells-project/` (Python/Flask), `ecommerce-api-legacy/` (Node.js/Express) e `task-manager-api/` (Python/Flask, parcialmente organizado).

Este documento tem duas partes: o **enunciado original do desafio** (para contexto de quem for avaliar) e as **respostas exigidas por ele** (o trabalho de fato entregue).

---

# Enunciado do Desafio

> Reprodução do enunciado do desafio, para que o repositório seja autossuficiente (o documento original não faz parte do código versionado).

Ao longo do curso você aprendeu o que são Skills e como elas permitem que um agente de IA atue como um especialista em tarefas específicas. Agora imagine o seguinte cenário: você herdou 3 projetos legados com problemas de arquitetura, segurança e qualidade de código. Revisar e corrigir tudo manualmente levaria dias.

Neste desafio, você vai criar uma Skill que automatiza esse processo — analisando, auditando e refatorando qualquer projeto para o padrão MVC, independente da tecnologia.

## Objetivo

Você deve entregar uma Skill capaz de:

- Analisar uma codebase detectando linguagem, framework e arquitetura atual
- Identificar anti-patterns e code smells, classificando por severidade com arquivo e linha exatos
- Gerar um relatório de auditoria estruturado com todos os achados
- Refatorar o projeto para o padrão MVC (Model-View-Controller), eliminando os problemas encontrados
- Validar o resultado garantindo que a aplicação continua funcionando após as mudanças

A skill deve ser agnóstica de tecnologia, funcionando com diferentes linguagens e frameworks.

## Contexto

### Definição de Severidades

Para padronizar a auditoria e os relatórios gerados pela IA, utilize a seguinte escala de classificação baseada em problemas de MVC e SOLID:

- **CRITICAL**: Falhas graves de arquitetura ou segurança que impedem o funcionamento correto, expõem dados sensíveis (ex: credenciais hardcoded, SQL Injection) ou violam completamente a separação de responsabilidades (ex: "God Class" contendo banco de dados, lógicas complexas e roteamento no mesmo arquivo).
- **HIGH**: Fortes violações do padrão MVC ou princípios SOLID que dificultam muito a manutenção e testes (ex: lógicas de negócio pesadas presas dentro de Controllers, forte acoplamento sem Injeção de Dependência, ou uso de estado global mutável em toda a aplicação).
- **MEDIUM**: Problemas de padronização, duplicação de código ou gargalos de performance moderada (ex: Queries N+1 no banco de dados, uso inadequado de middlewares, validações ausentes nas rotas).
- **LOW**: Melhorias de legibilidade, nomenclatura de variáveis ruins, ou "magic numbers" soltos pelo código.

## Exemplo de Uso no CLI

Executar a skill no projeto com problemas:

```bash
cd code-smells-project
claude "/refactor-arch"
```

```
================================
PHASE 1: PROJECT ANALYSIS
================================
Language:      Python
Framework:     Flask 3.1.1
Dependencies:  flask-cors
Domain:        E-commerce API (produtos, pedidos, usuários)
Architecture:  Monolítica — tudo em 4 arquivos, sem separação de camadas
Source files:  4 files analyzed
DB tables:     produtos, usuarios, ped
```

```
================================
ARCHITECTURE AUDIT REPORT
================================
Project: code-smells-project
Stack:   Python + Flask
Files:   4 analyzed | ~800 lines of code

Summary
CRITICAL: 4 | HIGH: 5 | MEDIUM: 2 | LOW: 3

Findings

[CRITICAL] God Class / God Method
File: models.py:1-350
Description: Arquivo único contém toda lógica de negócio, queries SQL,
             validação e formatação para 4 domínios diferentes.
Impact: Impossível testar em isolamento, qualquer mudança afeta tudo.
Recommendation: Separar em models e controllers por domínio.

[CRITICAL] Hardcoded Credentials
File: app.py:8
Description: SECRET_KEY hardcoded como 'minha-chave-super-secreta-123'
...

================================
Total: 14 findings
================================

Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]
> y



[... refatoração executada ...]

================================
PHASE 3: REFACTORING COMPLETE
================================
New Project Structure:
src/
├── config/settings.py
├── models/
│   ├── produto_model.py
│   └── usuario_model.py
├── views/
│   └── routes.py
├── controllers/
│   ├── produto_controller.py
│   └── pedido_controller.py
├── middlewares/error_handler.py
└── app.py (composition root)

Validation
  ✓ Application boots without errors
  ✓ All endpoints respond correctly
  ✓ Zero anti-patterns remaining
================================
```

## Tecnologias Obrigatórias

**Ferramenta** — uma das três opções abaixo (não são aceitas outras ferramentas):

- Claude Code
- Gemini CLI
- OpenAI Codex

**Recurso**: Custom Skills (ou o equivalente na ferramenta escolhida)

**Formato dos arquivos de referência**: Markdown

**Projetos-alvo**: Python/Flask (2 projetos) e Node.js/Express (1 projeto) (fornecidos no repositório base)

> **Nota**: Os exemplos deste documento usam o Claude Code (`.claude/skills/`) como referência. Se você optar por Gemini CLI ou Codex, adapte o nome da pasta e o comando de invocação conforme a convenção dela — o conceito de skill e a estrutura interna (`SKILL.md` + arquivos de referência) permanecem os mesmos.

## Requisitos

### 1. Análise Manual dos Projetos

Antes de criar a skill, você deve entender os problemas que ela vai resolver.

**Tarefas:**

- Analisar o projeto `code-smells-project/` (Python/Flask — API de E-commerce)
- Analisar o projeto `ecommerce-api-legacy/` (Node.js/Express — LMS API com fluxo de checkout)
- Analisar o projeto `task-manager-api/` (Python/Flask — API de Task Manager)

Para cada projeto, identificar e documentar no mínimo 5 problemas, incluindo pelo menos:

- 1 de severidade CRITICAL ou HIGH
- 2 de severidade MEDIUM
- 2 de severidade LOW

Documentar os achados na seção "Análise Manual" do seu `README.md`.

> **Dica**: Não precisa encontrar todos os problemas — foque nos que têm maior impacto arquitetural.

> **Por que 3 projetos?** Dois são Python/Flask (com níveis de organização diferentes) e um é Node.js/Express. Sua skill precisa funcionar nos 3 para provar que é verdadeiramente agnóstica de tecnologia.

### 2. Criação da Skill

Agora que você conhece os problemas, crie uma skill que os detecte, gere um relatório de auditoria e corrija automaticamente.

Criar a skill dentro do projeto `code-smells-project/` e implementar o `SKILL.md` com 3 fases sequenciais:

- **Fase 1 — Análise**: Detectar stack, mapear arquitetura atual, imprimir resumo
- **Fase 2 — Auditoria**: Cruzar código contra catálogo de anti-patterns, gerar relatório, pedir confirmação
- **Fase 3 — Refatoração**: Reestruturar para o padrão MVC, validar que funciona

Os arquivos de referência devem cobrir obrigatoriamente as seguintes áreas de conhecimento:

- **Análise de projeto**: Heurísticas para detecção de linguagem, framework, banco de dados e mapeamento de arquitetura
- **Catálogo de anti-patterns**: Anti-patterns com sinais de detecção e classificação de severidade
- **Template de relatório**: Formato padronizado do relatório de auditoria (Fase 2)
- **Guidelines de arquitetura**: Regras do padrão MVC alvo (camadas Models, Views/Routes e Controllers)
- **Playbook de refatoração**: Padrões concretos de transformação para cada anti-pattern (com exemplos de código)

**Requisitos da skill:**

- Deve ser agnóstica de tecnologia — deve funcionar corretamente nos 3 projetos fornecidos
- O catálogo de anti-patterns deve conter no mínimo 8 anti-patterns com severidade distribuída (CRITICAL, HIGH, MEDIUM, LOW)
- O catálogo deve incluir detecção de APIs deprecated
- O playbook deve ter no mínimo 8 padrões de transformação com exemplos de código antes/depois
- A Fase 2 deve pausar e pedir confirmação antes de modificar qualquer arquivo
- A Fase 3 deve validar o resultado (boot da aplicação + endpoints funcionando)

### 3. Execução da Skill

**Projeto 1 — code-smells-project (Python/Flask)**

```bash
claude "/refactor-arch"
```

- Verificar que a Fase 1 detecta corretamente a stack e imprime o resumo
- Verificar que a Fase 2 encontra no mínimo 5 dos problemas documentados na sua análise manual
- Confirmar a execução da Fase 3
- Verificar que a Fase 3 cria a estrutura MVC, a aplicação inicia sem erros e os endpoints originais continuam respondendo
- Salvar o relatório de auditoria em `reports/audit-project-1.md`
- Commitar o código refatorado no repositório

**Projeto 2 — ecommerce-api-legacy (Node.js/Express)**

```bash
cd ../ecommerce-api-legacy
claude "/refactor-arch"
```

- Copiar a pasta `.claude/skills/refactor-arch/` para dentro de `ecommerce-api-legacy/`
- Verificar que as 3 fases executam corretamente neste projeto
- Salvar o relatório em `reports/audit-project-2.md`
- Commitar o código refatorado no repositório

**Projeto 3 — task-manager-api (Python/Flask)**

```bash
cd ../task-manager-api
claude "/refactor-arch"
```

- Copiar a pasta `.claude/skills/refactor-arch/` para dentro de `task-manager-api/`
- Verificar que a Fase 1 detecta Python/Flask e o domínio de Task Manager
- Verificar que a Fase 2 identifica problemas mesmo em um projeto parcialmente organizado
- Verificar que a Fase 3 melhora a estrutura sem quebrar a aplicação
- Salvar o relatório em `reports/audit-project-3.md`
- Commitar o código refatorado no repositório

## Checklist de Validação

**Fase 1 — Análise**

- [ ] Linguagem detectada corretamente
- [ ] Framework detectado corretamente
- [ ] Domínio da aplicação descrito corretamente
- [ ] Número de arquivos analisados condiz com a realidade

**Fase 2 — Auditoria**

- [ ] Relatório segue o template definido nos arquivos de referência
- [ ] Cada finding tem arquivo e linhas exatos
- [ ] Findings ordenados por severidade (CRITICAL → LOW)
- [ ] Mínimo de 5 findings identificados
- [ ] Detecção de APIs deprecated incluída (se aplicável)
- [ ] Skill pausa e pede confirmação antes da Fase 3

**Fase 3 — Refatoração**

- [ ] Estrutura de diretórios segue padrão MVC
- [ ] Configuração extraída para módulo de config (sem hardcoded)
- [ ] Models criados para abstrair dados
- [ ] Views/Routes separadas para roteamento
- [ ] Controllers concentram o fluxo da aplicação
- [ ] Error handling centralizado
- [ ] Entry point claro
- [ ] Aplicação inicia sem erros
- [ ] Endpoints originais respondem corretamente

## Entregável

Repositório público no GitHub (fork do repositório base) contendo:

- Skill completa em `.claude/skills/refactor-arch/` (dentro dos 3 projetos)
- Código refatorado dos 3 projetos (resultado da execução da Fase 3, commitado no repositório)
- Relatórios de auditoria em `reports/` (3 arquivos)
- `README.md` atualizado

### Estrutura do repositório

```
desafio-skills/
├── README.md
│
├── code-smells-project/
│   ├── .claude/
│   │   └── skills/
│   │       └── refactor-arch/
│   │           ├── SKILL.md
│   │           └── (arquivos de referência)
│   ├── app.py
│   ├── controllers.py
│   ├── models.py
│   ├── database.py
│   └── requirements.txt
│
├── ecommerce-api-legacy/
│   ├── .claude/
│   │   └── skills/
│   │       └── refactor-arch/
│   ├── src/
│   │   ├── app.js
│   │   ├── GodManager.js
│   │   └── utils.js
│   ├── api.http
│   └── package.json
│
├── task-manager-api/
│   ├── .claude/
│   │   └── skills/
│   │       └── refactor-arch/
│   ├── app.py
│   ├── database.py
│   ├── requirements.txt
│   ├── models/
│   ├── routes/
│   ├── services/
│   └── utils/
│
└── reports/
    ├── audit-project-1.md
    ├── audit-project-2.md
    └── audit-project-3.md
```

> A estrutura acima mostra o estado **inicial** (boilerplate) dos projetos, antes da skill rodar. A estrutura final de cada projeto, já refatorada para MVC, está descrita na seção ["Respostas do Desafio"](#respostas-do-desafio) abaixo.

### README.md deve conter

**A) Seção "Análise Manual"**: lista dos problemas identificados, classificação por severidade e justificativa de por que cada problema é relevante.

**B) Seção "Construção da Skill"**: decisões de design, quais anti-patterns incluiu e por quê, como garantiu que a skill é agnóstica de tecnologia e desafios encontrados.

**C) Seção "Resultados"**: resumo dos relatórios de auditoria, comparação antes/depois, checklist de validação preenchido, screenshots ou logs das aplicações rodando após refatoração.

**D) Seção "Como Executar"**: pré-requisitos, comandos para executar a skill em cada projeto e como validar que a refatoração funcionou.

## Ordem de execução sugerida

1. **Analisar os projetos manualmente** — leia o código dos três projetos e documente os problemas encontrados.
2. **Criar a skill** — escreva o `SKILL.md` e os arquivos de referência.
3. **Executar nos 3 projetos**:

   ```bash
   # Projeto 1
   cd code-smells-project
   claude "/refactor-arch"

   # Projeto 2
   cd ../ecommerce-api-legacy
   claude "/refactor-arch"

   # Projeto 3
   cd ../task-manager-api
   claude "/refactor-arch"
   ```

4. **Iterar** — se a skill não detectou problemas suficientes ou a refatoração falhou, ajuste os arquivos de referência e execute novamente. É normal precisar de 2-4 iterações.

## Critérios de Aceite

A skill deve atingir os seguintes mínimos em todos os 3 projetos:

- Fase 1 detecta stack corretamente — **OBRIGATÓRIO** (3/3 projetos)
- Fase 2 encontra ≥ 5 findings — **OBRIGATÓRIO** (3/3 projetos)
- Fase 2 inclui pelo menos 1 CRITICAL ou HIGH — **OBRIGATÓRIO** (3/3 projetos)
- Fase 3 aplicação funciona após refatoração — **OBRIGATÓRIO** (3/3 projetos)

> Todos os critérios devem ser atingidos nos 3 projetos, não apenas em um!

## Referências

- **Claude Code: Skills** — Documentação oficial sobre como criar e estruturar Skills
- **Claude Code: Overview** — Visão geral do Claude Code e suas capacidades
- **The Complete Guide to Building Skills for Claude** (PDF) — Guia completo da Anthropic sobre construção de Skills
- **Equipping Agents for the Real World with Agent Skills** — Blog oficial da Anthropic sobre Agent Skills

## Dicas Finais

- Comece pela análise manual — entender os problemas profundamente é essencial para criar uma skill que os detecte.
- O `SKILL.md` é um prompt — ele instrui o agente sobre o que fazer, enquanto os arquivos de referência fornecem o conhecimento de domínio.
- Seja específico nos sinais de detecção — "código ruim" não ajuda; "query SQL dentro de loop for" é acionável.
- Teste incrementalmente — não tente criar a skill perfeita de primeira.
- A skill deve ser copiável — se ela só funciona em um projeto específico, está acoplada demais. Teste nos 3 projetos para validar.
- Pedir confirmação na Fase 2 é obrigatório — o humano deve revisar o relatório antes de qualquer modificação.
- Consulte as referências do curso — revise a documentação oficial da ferramenta escolhida e os materiais das aulas.

---

# Respostas do Desafio

> A partir daqui, o conteúdo é a entrega em si — as seções A/B/C/D exigidas pelo enunciado acima.

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

A skill `refactor-arch` foi criada uma única vez dentro de `code-smells-project/.claude/skills/refactor-arch/` e depois copiada, sem nenhuma alteração, para `ecommerce-api-legacy/` e `task-manager-api/`. Ela segue exatamente o formato de Custom Skill do Claude Code: um `SKILL.md` curto que orquestra 3 fases (Análise → Auditoria → Refatoração) e 5 arquivos de referência em `references/` que concentram todo o conhecimento de domínio, para o `SKILL.md` nunca precisar duplicar conteúdo.

**Decisões de design:**

- **Nenhuma heurística é amarrada a uma linguagem específica.** `project-analysis-heuristics.md` detecta linguagem/framework/banco a partir de uma tabela de "arquivo-sinal → ecossistema" (`requirements.txt` → Python, `package.json` → Node.js, etc.), com um ramo explícito para "desconhecido". Foi assim que a mesma skill detectou corretamente Flask nos dois projetos Python e Express no projeto Node, sem nenhum código condicional por projeto.
- **O catálogo de anti-patterns (16 itens) descreve sinais de detecção estruturais**, não sintáticos — por exemplo, N+1 é descrito como "uma chamada de banco dentro do corpo de um laço que itera sobre uma coleção já buscada", com um exemplo em Python (ORM) e um em Node.js (callback). Isso permitiu que o mesmo catálogo encontrasse o problema tanto no `SQLAlchemy` do `task-manager-api` quanto nos callbacks aninhados do `AppManager.js` do `ecommerce-api-legacy`.
- **Anti-patterns incluídos**: cobrem exatamente os 3 pilares pedidos pelo desafio — segurança (credenciais hardcoded, SQL Injection, endpoint sem auth, hashing falso, token falso), arquitetura/SOLID (God Class/Module, estado global mutável, ausência de DI) e qualidade/performance (N+1, duplicação de lógica, exception handling genérico, ausência de paginação, logging ad-hoc, delete sem cascade, magic numbers). O item de **API/prática deprecated** (`debug=True` fixo, MD5 para senha) foi incluído como exigido pelo enunciado.
- **O playbook de refatoração (14 padrões) tem exemplo antes/depois em Python e Node.js lado a lado** para cada padrão aplicável aos dois ecossistemas — isso é o que tornou a tradução do catálogo genérico em código real, nos 3 projetos, uma aplicação direta do playbook em vez de uma reinterpretação ad hoc por projeto.
- **O gate humano da Fase 2 foi tratado como regra de execução, não como detalhe do prompt.** O `SKILL.md` proíbe textualmente qualquer chamada de ferramenta de escrita antes de uma confirmação explícita do usuário, mas a garantia real veio de fora da skill: em cada uma das 3 execuções, a sessão parou de fato e perguntou à responsável pela revisão antes de tocar em qualquer arquivo (ver evidência na seção C).

**Como a agnosticismo de tecnologia foi validado**: a mesma pasta `.claude/skills/refactor-arch/` (idêntica, verificada por `diff -r`) foi copiada sem edição para os 3 projetos, e as 3 execuções encontraram corretamente a stack, geraram ≥8 findings cada e refatoraram para MVC — a prova de agnosticismo não é uma alegação, é o fato de a mesma pasta ter funcionado nas 3 vezes sem qualquer ajuste, incluindo em testes ao vivo independentes com o comando real `claude "/refactor-arch"` (ver seção C).

**Desafios encontrados:**

- O ambiente de validação local não tinha suporte a `hashlib.scrypt` (dependência padrão do `werkzeug.security.generate_password_hash` em versões recentes), quebrando o boot do `code-smells-project` na primeira tentativa. Resolvido especificando explicitamente `method="pbkdf2:sha256"` — mais portátil e ainda uma escolha de hashing segura.
- A porta padrão 5000 estava ocupada pelo AirPlay Receiver do macOS durante a validação local — contornado usando uma variável de ambiente `PORT` (adicionada à config dos 3 projetos) em vez de alterar o comportamento padrão da aplicação.
- No `ecommerce-api-legacy`, `bcrypt` (nativo) exigiria compilação C durante a instalação; optou-se por `bcryptjs` (implementação pura em JavaScript, sem dependência de build), que resolve o mesmo anti-pattern (#5) sem risco de falha de instalação em ambientes diferentes.
- Corrigir a paginação ausente no `task-manager-api` (finding LOW) muda o formato de resposta de `GET /tasks` e `GET /users` (de lista crua para `{"items": [...], "page", ...}`) — uma mudança de contrato intencional, decorrente diretamente da recomendação do catálogo, documentada no README do projeto para não ser confundida com uma regressão.
- Um teste ao vivo da skill (rodando `claude "/refactor-arch"` de verdade, em processo separado, numa cópia temporária de `code-smells-project`) revelou uma organização de rotas divergente entre os 3 projetos entregues: `code-smells-project` usava um único `views/routes.py`, enquanto os outros dois já usavam um arquivo de rota por domínio. Corrigido reestruturando `code-smells-project` para o mesmo padrão e documentando explicitamente a convenção de header do guard de admin (`X-Admin-Token`) na guideline, que antes não estava especificada.

## C. Resultados

### Resumo dos relatórios de auditoria

| Projeto | Stack | Findings | CRITICAL | HIGH | MEDIUM | LOW |
|---|---|---|---|---|---|---|
| [`reports/audit-project-1.md`](reports/audit-project-1.md) — code-smells-project | Python/Flask | 8 | 3 | 1 | 2 | 2 |
| [`reports/audit-project-2.md`](reports/audit-project-2.md) — ecommerce-api-legacy | Node.js/Express | 8 | 2 | 2 | 2 | 2 |
| [`reports/audit-project-3.md`](reports/audit-project-3.md) — task-manager-api | Python/Flask + SQLAlchemy | 8 | 2 | 2 | 2 | 2 |

Todos os 3 projetos superaram o mínimo de 5 findings exigido pelo desafio, com folga, e todos têm pelo menos 1 CRITICAL ou HIGH entre os achados (na prática, todos têm ≥2).

### Comparação antes/depois

| Projeto | Antes | Depois |
|---|---|---|
| code-smells-project | 4 arquivos monolíticos, SQL concatenado, `/admin/query` executando SQL livre sem auth, `secret_key` vazada no health check, senha em texto plano | `src/{config,models,controllers,routes,middlewares}/`, queries parametrizadas, `/admin/query` removido, `/admin/reset-db` com guard de token, health check sem vazamento, senha hasheada (`pbkdf2:sha256`), N+1 de pedidos resolvido com 1 JOIN |
| ecommerce-api-legacy | `AppManager.js` (God Class, 141 linhas) com pirâmide de callbacks, segredos hardcoded, hash de senha fake, delete sem cascade | `src/{config,models,controllers,routes,middlewares,services,utils}/`, `async/await` em vez de callbacks aninhados, segredos via `.env`, `bcryptjs` real, relatório financeiro sem N+1 (4 queries fixas), delete com cascade explícito |
| task-manager-api | Rotas com regra de negócio embutida, MD5 para senha, token de login falso, overdue duplicado 3x, `except:` genérico | `controllers/` novo absorvendo a lógica das rotas, hashing real (`pbkdf2:sha256`), JWT real e assinado (`pyjwt`), `Task.is_overdue()` reaproveitado nos 3 pontos, error handler central, paginação em `/tasks` e `/users` |

### Checklist de Validação (do enunciado)

**Fase 1 — Análise**
- [x] Linguagem detectada corretamente (Python nos projetos 1 e 3, JavaScript/Node.js no projeto 2)
- [x] Framework detectado corretamente (Flask 3.1.1, Express ^4.18.2, Flask 3.0.0 + Flask-SQLAlchemy)
- [x] Domínio da aplicação descrito corretamente (e-commerce, LMS/checkout, task manager)
- [x] Número de arquivos analisados condiz com a realidade (4, 3 e 15 arquivos, respectivamente)

**Fase 2 — Auditoria**
- [x] Relatório segue o template definido nos arquivos de referência
- [x] Cada finding tem arquivo e linhas exatos
- [x] Findings ordenados por severidade (CRITICAL → LOW)
- [x] Mínimo de 5 findings identificados (8 em cada projeto)
- [x] Detecção de APIs deprecated incluída (`debug=True` fixo nos 3 projetos; MD5 no projeto 3)
- [x] Skill pausa e pede confirmação antes da Fase 3 — evidência abaixo

**Fase 3 — Refatoração**
- [x] Estrutura de diretórios segue padrão MVC
- [x] Configuração extraída para módulo de config (sem hardcoded)
- [x] Models criados/mantidos para abstrair dados
- [x] Views/Routes separadas para roteamento
- [x] Controllers concentram o fluxo da aplicação
- [x] Error handling centralizado
- [x] Entry point claro
- [x] Aplicação inicia sem erros (validado nos 3 projetos, ver tabelas PASS/FAIL abaixo)
- [x] Endpoints originais respondem corretamente (nos 3 projetos)

### Evidência dos 3 gates humanos de confirmação

Em cada um dos 3 projetos, ao final da Fase 2, a execução parou e apresentou o resumo do relatório de auditoria, perguntando explicitamente: *"Relatório completo em `reports/audit-project-N.md`. Posso prosseguir para a Fase 3 (refatoração para MVC) neste projeto?"* — com as opções "Sim, prosseguir" e "Não, quero ajustar o relatório antes". Nenhuma ferramenta de escrita foi usada nos arquivos dos projetos antes dessa resposta.

| Projeto | Pergunta feita | Resposta da revisora |
|---|---|---|
| code-smells-project | Confirmar Fase 3 após 8 findings (3 CRITICAL, 1 HIGH, 2 MEDIUM, 2 LOW) | "Sim, prosseguir" |
| ecommerce-api-legacy | Confirmar Fase 3 após 8 findings (2 CRITICAL, 2 HIGH, 2 MEDIUM, 2 LOW) | "Sim, prosseguir" |
| task-manager-api | Confirmar Fase 3 após 8 findings (2 CRITICAL, 2 HIGH, 2 MEDIUM, 2 LOW) | "Sim, prosseguir" |

### Teste ao vivo da skill via `claude "/refactor-arch"`

Além da execução guiada (a construtora da skill seguindo manualmente as 3 fases para produzir os relatórios e o código refatorado documentados acima), a skill foi testada de forma **independente e autônoma nos 3 projetos**: recriou-se uma cópia temporária de cada projeto no estado original (a partir do commit inicial do repositório), fora do repositório de entrega, e o comando real `claude "/refactor-arch"` foi invocado em processo separado em cada uma, sem nenhuma instrução adicional além do prompt e, depois, da confirmação da Fase 3.

| Projeto | Fase 1+2 (autônoma) | Gate humano | Fase 3 (após confirmação) | Validação independente |
|---|---|---|---|---|
| code-smells-project | Python/Flask 3.1.1, 4 arquivos, ~780 linhas — correto. **14 findings** (mais que os 8 da análise manual, incluindo um bypass de login via SQL Injection não documentado antes). | Parou sozinha na linha exata `Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]`, sem tocar em nenhum arquivo além do relatório. | Reestruturou em MVC, endereçou os 14 findings, **25/25 endpoints PASS, 0 respostas 5xx** — e se autocorrigiu ao notar que o error handler genérico convertia 404/405 nativos do Flask em 500. | Subi a aplicação e confirmei manualmente: `/health` sem vazamento, `/admin/query` removido (404), `/admin/reset-db` exige token, SQL Injection no login falha corretamente. |
| ecommerce-api-legacy | Node.js/Express, correto. **13 findings** (4 CRITICAL, incluindo cartão de cliente vazado em log — um detalhe que eu não tinha documentado). | Parou sozinha, só o relatório criado. | Refatorou em MVC (`models/controllers/routes/middlewares/services`), hash de senha migrado para `scrypt` nativo do Node (sem dependência externa), cache isolado em serviço, **7/7 endpoints PASS, 0 respostas 5xx**. | Subi a aplicação e confirmei: `/api/admin/financial-report` e `DELETE /api/users/:id` exigem `X-Admin-Token` (401 sem, 200 com), checkout funciona. |
| task-manager-api | Python/Flask + SQLAlchemy, domínio Task Manager corretamente identificado. **12 findings** (3 CRITICAL, 3 HIGH). | Parou sozinha, só o relatório criado. | Reestruturou em MVC (`controllers/` novo), MD5 → `pbkdf2:sha256`, JWT real assinado, `NotificationService` morto removido, N+1 eliminado, **29/29 endpoints PASS, 0 respostas 5xx**. | Subi a aplicação e confirmei: login retorna JWT real assinado, `/reports/summary` e `DELETE` exigem `X-Admin-Token` (401 sem, 200 com). |

Em nenhum dos 3 casos a skill rodou `git commit` sozinha — cada execução parou após validar e sugeriu a mensagem de commit (sem trailer de IA), deixando a decisão para o operador, exatamente como especificado no `SKILL.md`.

Esse teste é o que dá confiança de que a skill funciona como comando real invocável, de forma consistente nos 3 projetos — não só como uma sequência de passos que a autora seguiu manualmente ao construí-la.

### Validação pós-refatoração (aplicações rodando)

**code-smells-project** (`main.py`, porta local de teste 5057):

| Endpoint | Resultado |
|---|---|
| `GET /`, `GET /health` | PASS — sem vazamento de `secret_key`/`debug`/`db_path` |
| `GET/POST/PUT /produtos*` | PASS |
| `GET /usuarios`, `POST /login` | PASS — sem campo `senha` na resposta, hash validado |
| `POST /pedidos`, `GET /pedidos*` | PASS — itens resolvidos com 1 JOIN (sem N+1) |
| `PUT /pedidos/<id>/status`, `GET /relatorios/vendas` | PASS |
| `POST /admin/query` | Removido por decisão de segurança — 404 confirmado |
| `POST /admin/reset-db` | PASS — 401 sem token, 200 com `X-Admin-Token` |

**ecommerce-api-legacy** (`src/app.js`, porta local de teste 3057):

| Endpoint | Resultado |
|---|---|
| `POST /api/checkout` | PASS — sucesso, pagamento recusado, bad request e curso inexistente cobertos |
| `GET /api/admin/financial-report` | PASS — 401 sem token, 200 com token; sem N+1 |
| `DELETE /api/users/:id` | PASS — cascade confirmado (relatório recalcula receita corretamente após o delete) |

**task-manager-api** (`app.py`, porta local de teste 5058):

| Endpoint | Resultado |
|---|---|
| `GET /`, `GET /health` | PASS |
| `GET/POST/PUT/DELETE /tasks*` | PASS — listagem paginada, `overdue` via `Task.is_overdue()` |
| `GET/POST/PUT/DELETE /users*` | PASS — listagem paginada, sem campo `password` |
| `POST /login` | PASS — JWT real assinado retornado; 401 com senha errada |
| `GET /reports/*`, `/categories*` | PASS |

## D. Como Executar

### Pré-requisitos

- Python 3.9+ e `pip` (para `code-smells-project` e `task-manager-api`)
- Node.js 18+ e `npm` (para `ecommerce-api-legacy`)
- Claude Code instalado, para invocar a skill via `claude "/refactor-arch"`

### Rodar cada projeto (aplicação já refatorada)

```bash
# Projeto 1 — code-smells-project
cd code-smells-project
pip install -r requirements.txt
cp .env.example .env
python main.py            # http://localhost:5000

# Projeto 2 — ecommerce-api-legacy
cd ecommerce-api-legacy
npm install
cp .env.example .env
npm start                 # http://localhost:3000

# Projeto 3 — task-manager-api
cd task-manager-api
pip install -r requirements.txt
cp .env.example .env
python seed.py            # popula o banco antes do primeiro boot
python app.py             # http://localhost:5000
```

### Como validar que a refatoração funcionou

1. Confirmar que a aplicação sobe sem erros no console.
2. Exercitar os endpoints documentados no `README.md` de cada projeto (ou nos exemplos de `api.http`, no caso do `ecommerce-api-legacy`) e conferir que nenhum retorna `5xx`.
3. Comparar o comportamento com o relatório de auditoria correspondente em `reports/` — as únicas respostas diferentes do comportamento original são as mudanças intencionais documentadas (remoção do `/admin/query`, guards de token, paginação, JWT real), nunca uma regressão.

### Re-executar a skill (opcional)

Cada projeto já contém sua própria cópia de `.claude/skills/refactor-arch/`. Para reexecutar a auditoria em um projeto (por exemplo, após alterações futuras no código):

```bash
cd code-smells-project      # ou ecommerce-api-legacy / task-manager-api
claude "/refactor-arch"
```

A skill vai parar ao final da Fase 2 e pedir confirmação explícita antes de tocar em qualquer arquivo — responda apenas depois de revisar o relatório gerado.
