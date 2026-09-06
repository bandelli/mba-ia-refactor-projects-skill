================================
ARCHITECTURE AUDIT REPORT
================================
Project: task-manager-api
Stack:   Python + Flask 3.0.0 + Flask-SQLAlchemy
Files:   15 analyzed | ~1158 lines of code

Summary
CRITICAL: 2 | HIGH: 2 | MEDIUM: 2 | LOW: 2

Findings

[CRITICAL] Hash de senha com MD5
File: models/user.py:29,32
Description: set_password()/check_password() usam hashlib.md5(pwd.encode()).hexdigest() para armazenar e validar senha.
Impact: MD5 é criptograficamente quebrado para senhas (rápido de forçar bruta, sem salt) — um dos itens de prática deprecated mais citados em auditorias de segurança.
Recommendation: Aplicar P5 — usar werkzeug.security.generate_password_hash/check_password_hash.

[CRITICAL] Emissão de token de autenticação falso
File: routes/user_routes.py:210
Description: o endpoint de login retorna 'token': 'fake-jwt-token-' + str(user.id) — uma string previsível, não assinada e sem expiração.
Impact: qualquer cliente pode forjar um token válido para qualquer user_id só concatenando o prefixo, quebrando toda a autenticação da API.
Recommendation: Aplicar P8 — emitir JWT real assinado (pyjwt) com expiração.

[HIGH] SECRET_KEY hardcoded e debug ligado em produção
File: app.py:13,34
Description: app.config['SECRET_KEY'] = 'super-secret-key-123' fixo no código-fonte, e app.run(debug=True, ...) sem condicional de ambiente.
Impact: mesma classe de risco de credencial exposta e debugger habilitado em produção.
Recommendation: Aplicar P1 (SECRET_KEY via env) e P7 (debug controlado por config de ambiente).

[HIGH] Credenciais SMTP hardcoded no código-fonte
File: services/notification_service.py:9-10
Description: self.email_user e self.email_password ('senha123') são atribuídos como literais na classe NotificationService.
Impact: expõe credenciais de uma conta de e-mail real a qualquer pessoa com acesso ao repositório.
Recommendation: Aplicar P1 — mover para variáveis de ambiente.

[MEDIUM] Query N+1 na listagem de tasks
File: routes/task_routes.py:41-57
Description: get_tasks() itera todas as tasks e, para cada uma, chama User.query.get(t.user_id) e Category.query.get(t.category_id) individualmente em vez de usar joinedload/selectinload.
Impact: uma listagem de N tasks gera até 1 + 2N queries em vez de 1 query com join.
Recommendation: Aplicar P9 — eager loading com joinedload.

[MEDIUM] Lógica de "overdue" duplicada em 3 arquivos, ignorando método já existente
File: routes/task_routes.py:30-39, routes/user_routes.py:171-180, routes/report_routes.py:34-43 (vs. models/task.py:50-60)
Description: o mesmo bloco de "due_date < utcnow() and status not in (done, cancelled)" é reescrito manualmente em 3 rotas diferentes, enquanto Task.is_overdue() já existe no model e não é chamado em nenhum lugar.
Impact: qualquer mudança na regra de "atrasado" precisa ser replicada em 3 lugares, com alto risco de inconsistência.
Recommendation: Aplicar P11 — usar Task.is_overdue() nos 3 pontos em vez de duplicar a lógica.

[LOW] except: genérico engolindo exceções
File: routes/task_routes.py:62
Description: get_tasks() envolve toda a lógica num try/except: sem tipo, retornando sempre {'error': 'Erro interno'} e descartando a exceção real (sem log).
Impact: torna erros de produção praticamente impossíveis de diagnosticar.
Recommendation: Aplicar P10 — remover o try/except local e deixar o error handler central tratar e logar.

[LOW] Ausência de paginação nas listagens
File: routes/task_routes.py:14, routes/user_routes.py:12
Description: get_tasks() e get_users() retornam Task.query.all() / User.query.all() sem parâmetros de page/limit.
Impact: à medida que a base cresce, esses endpoints degradam performance e podem estourar memória/tempo de resposta.
Recommendation: Aplicar P12 — paginação via Flask-SQLAlchemy paginate().

================================
Total: 8 findings
================================

Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]
