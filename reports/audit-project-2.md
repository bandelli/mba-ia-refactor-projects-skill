================================
ARCHITECTURE AUDIT REPORT
================================
Project: ecommerce-api-legacy
Stack:   Node.js + Express ^4.18.2
Files:   3 analyzed | ~180 lines of code

Summary
CRITICAL: 2 | HIGH: 2 | MEDIUM: 2 | LOW: 2

Findings

[CRITICAL] Segredos de produção hardcoded no código-fonte
File: src/utils.js:1-7
Description: o objeto config tem dbPass: "senha_super_secreta_prod_123" e paymentGatewayKey: "pk_live_1234567890abcdef" (formato de chave live de gateway de pagamento) fixos no código.
Impact: qualquer pessoa com acesso ao repositório tem a chave de um gateway de pagamento de produção e a senha do banco.
Recommendation: Aplicar P1 — mover para variáveis de ambiente via dotenv, com .env.example de placeholder.

[CRITICAL] Hash de senha falso
File: src/utils.js:17-23
Description: badCrypto() não é uma função de hash — repete 10.000 vezes uma conversão para base64 e concatena os 2 primeiros caracteres, produzindo uma string curta e reversível na prática.
Impact: não oferece nenhuma proteção real contra vazamento de senha; usada para gerar a senha do usuário durante o checkout.
Recommendation: Aplicar P5 — usar bcrypt real.

[HIGH] God Class AppManager misturando DB, rotas e 3 fluxos de negócio
File: src/AppManager.js:1-141
Description: uma única classe cuida de schema/seed do banco (initDb), roteamento (setupRoutes) e a lógica completa de checkout, relatório financeiro e exclusão de usuário.
Impact: impede testar cada fluxo isoladamente e concentra todo o risco de regressão em um único arquivo.
Recommendation: Aplicar P4 — separar em models, controllers e rotas por domínio.

[HIGH] Lógica de negócio pesada dentro do route handler, em pirâmide de callbacks
File: src/AppManager.js:28-78
Description: o handler de POST /api/checkout aninha callbacks de banco em até 5 níveis, misturando busca de curso, criação de usuário, "processamento" de pagamento (cc.startsWith("4")), matrícula e log de auditoria tudo dentro da própria rota.
Impact: viola a separação Controller/Model do MVC; difícil de testar unitariamente e fácil de esquecer de tratar algum erro intermediário.
Recommendation: Aplicar P4 — extrair para checkoutController com funções sequenciais (idealmente com promises/async-await).

[MEDIUM] Query N+1 aninhada com controle manual de conclusão assíncrona
File: src/AppManager.js:80-129
Description: /api/admin/financial-report busca cursos, depois matrículas por curso, depois usuário e pagamento por matrícula — tudo com callbacks aninhados e contadores manuais (coursesPending, enrPending) para saber quando a resposta pode ser enviada.
Impact: além do problema de performance (N+1), o controle manual de contagem é frágil — qualquer callback que não decrementa o contador trava a resposta indefinidamente.
Recommendation: Aplicar P9 — substituir por queries agregadas com JOIN/IN e async/await.

[MEDIUM] Exclusão de usuário sem cascade, gerando dados órfãos
File: src/AppManager.js:131-137
Description: DELETE /api/users/:id remove a linha de users sem tratar enrollments/payments associados; a própria resposta da API admite isso ("...matrículas e pagamentos ficaram sujos no banco.").
Impact: corrompe a integridade referencial do banco a cada exclusão de usuário.
Recommendation: Aplicar P14 — deletar registros filhos (payments, enrollments) antes do pai, na mesma transação.

[LOW] Estado global mutável em nível de módulo
File: src/utils.js:9-10
Description: globalCache e totalRevenue são variáveis mutáveis no escopo do módulo, compartilhadas entre todas as requisições.
Impact: em cenários com mais de um processo/instância ou testes concorrentes, gera condições de corrida e resultados inconsistentes.
Recommendation: Aplicar P6 — encapsular em um serviço instanciado no composition root e injetado onde necessário.

[LOW] Tratamento de erro ad hoc, sem middleware centralizado
File: src/AppManager.js:38,41,51,55,84
Description: cada callback trata erro chamando res.status(500).send("Erro DB") (ou variações) individualmente, sem um middleware de erro único.
Impact: mensagens de erro inconsistentes para o cliente e lógica de tratamento duplicada em todos os pontos de falha.
Recommendation: Aplicar P10 — middleware de erro Express centralizado, montado por último.

================================
Total: 8 findings
================================

Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]
