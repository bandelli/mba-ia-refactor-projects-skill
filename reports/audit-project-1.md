================================
ARCHITECTURE AUDIT REPORT
================================
Project: code-smells-project
Stack:   Python + Flask 3.1.1
Files:   4 analyzed | ~780 lines of code

Summary
CRITICAL: 3 | HIGH: 1 | MEDIUM: 2 | LOW: 2

Findings

[CRITICAL] SQL Injection generalizada por concatenação de string
File: models.py:28,48-50,58-61,68,92,109-111,126-129,140,148-151,155,158-161,163-166,174,188,192,206-207,220,224,280,291-297
Description: praticamente toda função de acesso a dados monta a query SQL concatenando strings com valores vindos direto da requisição (ex.: "SELECT * FROM produtos WHERE id = " + str(id)), sem parâmetros preparados.
Impact: qualquer campo de texto (nome, categoria, termo de busca) pode ser usado para injetar SQL arbitrário e ler/alterar/apagar dados do banco inteiro.
Recommendation: Aplicar P2 — parametrizar todas as queries com placeholders (?).

[CRITICAL] Endpoint /admin/query executa SQL arbitrário vindo do request, sem autenticação
File: app.py:59-78
Description: o handler executar_query() pega dados.get("sql", "") do corpo da requisição e chama cursor.execute(query) diretamente, sem nenhuma checagem de identidade/role.
Impact: é um console SQL exposto publicamente — qualquer pessoa pode ler, alterar ou apagar todo o banco.
Recommendation: Aplicar P2 — remover o endpoint por completo (não há forma segura de expor execução de SQL livre a partir de input externo).

[CRITICAL] Credenciais hardcoded e modo debug ligado em produção
File: app.py:7-8,88
Description: SECRET_KEY = "minha-chave-super-secreta-123" fixo no código-fonte e app.run(..., debug=True) sem condicional de ambiente.
Impact: quebra a segurança de sessão/assinatura da aplicação; debug=True expõe stack traces e o debugger interativo em produção.
Recommendation: Aplicar P1 (mover SECRET_KEY para variável de ambiente) e P7 (debug controlado por config de ambiente).

[HIGH] God Module concentrando 4 domínios de negócio
File: models.py:1-314
Description: um único arquivo contém acesso a dados, regra de negócio e serialização para produtos, usuários, pedidos e itens de pedido.
Impact: impossível testar em isolamento; qualquer mudança em um domínio arrisca quebrar os outros três.
Recommendation: Aplicar P4 — separar em um model por domínio (produto, usuário, pedido, item de pedido) e mover regra de negócio para controllers.

[MEDIUM] Query N+1 na listagem de pedidos
File: models.py:171-201,203-233
Description: get_pedidos_usuario() e get_todos_pedidos() fazem um laço por pedido, abrindo um cursor para os itens e outro por item para o nome do produto.
Impact: para N pedidos com M itens cada, gera 1 + N + N×M queries em vez de 2-3 queries com JOIN.
Recommendation: Aplicar P9 — substituir os laços aninhados por uma única query com JOIN.

[MEDIUM] Vazamento de dados sensíveis em endpoint público
File: controllers.py:276-290
Description: health_check() retorna no JSON público db_path, debug e secret_key.
Impact: um endpoint sem autenticação está vazando a chave secreta da aplicação e detalhes de infraestrutura.
Recommendation: Aplicar P1 (segredo isolado em config) e P10 (remover esses campos do payload de resposta).

[LOW] Logging ad-hoc via print() em vez de logger estruturado
File: controllers.py:8,11,57,61,106,161,179,182,208-210,219,248-250
Description: mensagens de operação e erro são emitidas com print() espalhado pelos controllers, sem nível de log, timestamp ou destino configurável.
Impact: dificulta observabilidade em produção.
Recommendation: Aplicar P13 — substituir por logger configurável (módulo logging).

[LOW] Senha armazenada e comparada em texto plano
File: database.py:75-79, models.py:105-120
Description: usuários de seed criados com senha em texto plano; login_usuario() compara a senha recebida diretamente contra o valor salvo, sem hashing.
Impact: qualquer vazamento do banco expõe todas as senhas dos usuários diretamente.
Recommendation: Aplicar P5 — hashing real de senha (werkzeug.security).

================================
Total: 8 findings
================================

Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]
