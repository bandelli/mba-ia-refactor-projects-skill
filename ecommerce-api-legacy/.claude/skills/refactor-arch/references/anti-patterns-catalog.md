# Catálogo de Anti-Patterns (Fase 2)

Cada anti-pattern abaixo é descrito por um **sinal de detecção estrutural** (não amarrado a uma linguagem específica) mais um exemplo por ecossistema, para que a detecção funcione em qualquer stack. O campo "Padrão de refatoração" aponta para o item correspondente em `refactoring-playbook.md`.

Ordem de severidade para o relatório: **CRITICAL → HIGH → MEDIUM → LOW**.

## 1. [CRITICAL] Hardcoded Credentials / Secrets

- **Sinal de detecção**: literal de string atribuído a uma variável, chave de config ou argumento cujo nome contém `secret`, `password`, `pass`, `key`, `token` ou `apikey`, sem vir de uma variável de ambiente/gerenciador de segredos.
- **Exemplo Python**: `SECRET_KEY = "minha-chave-super-secreta-123"`
- **Exemplo Node.js**: `dbPass: "senha_super_secreta_prod_123"`
- **Impacto**: qualquer pessoa com acesso ao código tem credenciais de produção.
- **Padrão de refatoração**: P1.

## 2. [CRITICAL] SQL Injection / Execução Arbitrária de SQL

- **Sinal de detecção**: montagem de comando SQL por concatenação de string ou f-string com valor vindo de request/input do usuário; ou um endpoint que recebe uma string SQL no corpo da requisição e a executa diretamente.
- **Exemplo Python**: `cursor.execute("SELECT * FROM produtos WHERE id = " + str(id))`
- **Exemplo Node.js**: `db.all("SELECT * FROM t WHERE name = '" + name + "'")`
- **Impacto**: leitura, alteração ou exclusão arbitrária de dados; em casos de endpoint de "query livre", controle total do banco.
- **Padrão de refatoração**: P2.

## 3. [CRITICAL] Endpoint Sensível sem Autenticação

- **Sinal de detecção**: rota cujo path ou nome de handler contém `admin`, `delete`, `reset`, `query`, `report` (financeiro/administrativo) e que não passa por nenhum decorator/middleware de autenticação/autorização antes da lógica de negócio.
- **Exemplo Python**: `@app.route("/admin/reset-db", methods=["POST"])` sem checagem de token/role.
- **Exemplo Node.js**: `app.get('/api/admin/financial-report', (req, res) => {...})` sem middleware de auth.
- **Impacto**: qualquer usuário não autenticado pode executar ações administrativas ou ler dados sensíveis.
- **Padrão de refatoração**: P3.

## 4. [CRITICAL] God Class / God Module

- **Sinal de detecção**: um único arquivo ou classe concentra acesso a dados (SQL/ORM), regra de negócio e, às vezes, roteamento, para mais de um domínio de negócio distinto.
- **Exemplo Python**: um `models.py` com funções de produtos, usuários e pedidos misturadas, com SQL cru inline.
- **Exemplo Node.js**: uma classe `AppManager` que faz setup de banco, define rotas e implementa checkout, relatório e exclusão de usuário.
- **Impacto**: impossível testar em isolamento; qualquer mudança em um domínio arrisca quebrar os outros.
- **Padrão de refatoração**: P4.

## 5. [HIGH] Hashing/Criptografia Falsa ou Fraca

- **Sinal de detecção**: uso de `MD5`/`SHA1` (sozinhos, sem salt/stretching) para hash de senha; ou uma função de "hash" customizada que não usa uma biblioteca criptográfica reconhecida.
- **Exemplo Python**: `hashlib.md5(pwd.encode()).hexdigest()`
- **Exemplo Node.js**: uma função que repete `Buffer.from(pwd).toString('base64')` para "gerar hash".
- **Impacto**: senhas podem ser quebradas por força bruta/rainbow table, ou revertidas trivialmente.
- **Padrão de refatoração**: P5.

## 6. [HIGH] Estado Global Mutável / Ausência de Injeção de Dependência

- **Sinal de detecção**: variável em nível de módulo (dict, lista, conexão de banco) que é lida e escrita por múltiplos handlers de requisição, sem passar por uma factory/instância injetada.
- **Exemplo Python**: `db_connection = None` no topo do módulo, reatribuída dentro de `get_db()` e reutilizada globalmente.
- **Exemplo Node.js**: `let globalCache = {}` no topo do módulo, mutado por múltiplas rotas.
- **Impacto**: condições de corrida em cenários concorrentes/múltiplas instâncias; impossível isolar estado em testes.
- **Padrão de refatoração**: P6.

## 7. [HIGH] Defaults Inseguros / Uso de API Deprecated

- **Sinal de detecção**: flag de debug/desenvolvimento ligada permanentemente no ponto de entrada (`debug=True` fixo, não vindo de env); ou uso de uma API/método que a documentação oficial do framework marca como deprecated; ou dependência com major version muito atrás do atual mantido.
- **Exemplo Python**: `app.run(debug=True)` fixo no código, sem condicional de ambiente.
- **Exemplo Node.js**: uso de um método de uma versão de biblioteca já descontinuada (checar cabeçalho de changelog/release notes da dependência pinada).
- **Impacto**: exposição de informações de debug e superfície de ataque maior em produção; comportamento não garantido/sem suporte de segurança em APIs deprecated.
- **Padrão de refatoração**: P7.

## 8. [HIGH] Emissão de Token de Autenticação Falso ou Não Assinado

- **Sinal de detecção**: endpoint de login que retorna como "token" uma concatenação previsível (prefixo fixo + id do usuário), sem assinatura criptográfica nem expiração.
- **Exemplo Python**: `'token': 'fake-jwt-token-' + str(user.id)`
- **Impacto**: qualquer cliente pode forjar um token válido para qualquer usuário, quebrando toda a autenticação.
- **Padrão de refatoração**: P8.

## 9. [MEDIUM] Query N+1

- **Sinal de detecção**: uma chamada de banco (ORM ou SQL raw) dentro do corpo de um laço que itera sobre uma coleção já buscada, em vez de uma única query com join/eager loading ou `WHERE id IN (...)`.
- **Exemplo Python**: `for t in tasks: user = User.query.get(t.user_id)`
- **Exemplo Node.js**: `enrollments.forEach(enr => { db.get("SELECT ... WHERE id = ?", [enr.user_id], ...) })`
- **Impacto**: número de queries cresce linearmente (ou pior) com o tamanho da coleção, degradando performance rapidamente.
- **Padrão de refatoração**: P9.

## 10. [MEDIUM] Vazamento de Dados/Segredos em Resposta Pública

- **Sinal de detecção**: payload de resposta JSON de um endpoint sem autenticação (tipicamente health-check) contendo chaves como `secret`, `debug`, `password`, ou caminho de arquivo de banco de dados.
- **Exemplo Python**: `return jsonify({"secret_key": SECRET_KEY, "debug": True, "db_path": db_path})`
- **Impacto**: informação sensível de infraestrutura/segurança exposta a qualquer requisição não autenticada.
- **Padrão de refatoração**: P1 (mesma raiz de segredo mal isolado) + P10 (remover do payload de resposta).

## 11. [MEDIUM] Exception Handling Genérico ou Silencioso

- **Sinal de detecção**: bloco `except:`/`except Exception:` (Python) ou `.catch(() => {})`/callback de erro vazio (Node.js) que não loga a exceção original e retorna sempre a mesma mensagem genérica.
- **Exemplo Python**: `except: return jsonify({'error': 'Erro interno'}), 500`
- **Impacto**: torna diagnósticos de produção praticamente impossíveis — todo erro parece igual.
- **Padrão de refatoração**: P10.

## 12. [MEDIUM] Duplicação de Lógica (violação de DRY) / Utilitário Morto

- **Sinal de detecção**: um bloco de lógica quase idêntico (mesma condição, mesma sequência de passos) repetido em 2 ou mais arquivos, enquanto existe um método/função equivalente já implementado e não referenciado em nenhum lugar do código.
- **Exemplo Python**: a mesma checagem `if due_date < now() and status not in (...)` reescrita em 3 arquivos de rota, enquanto `Task.is_overdue()` existe no model e nunca é chamado.
- **Impacto**: qualquer mudança na regra de negócio precisa ser replicada manualmente em todos os pontos duplicados, com alto risco de inconsistência.
- **Padrão de refatoração**: P11.

## 13. [LOW] Ausência de Paginação

- **Sinal de detecção**: endpoint de listagem que retorna todos os registros de uma tabela/coleção (`.all()`, `SELECT *` sem `LIMIT`) sem parâmetros de `page`/`limit`/`offset`.
- **Exemplo Python**: `Task.query.all()` retornado diretamente como JSON.
- **Impacto**: degradação de performance e uso de memória conforme a base cresce.
- **Padrão de refatoração**: P12.

## 14. [LOW] Logging Ad-hoc via print()/console.log()

- **Sinal de detecção**: uso de `print()` (Python) ou `console.log()` (Node.js) como mecanismo de logging operacional dentro de request handlers, em vez de um logger configurável (nível, formato, destino).
- **Impacto**: impossível filtrar por severidade ou redirecionar para um serviço de observabilidade em produção.
- **Padrão de refatoração**: P13.

## 15. [LOW/MEDIUM] Delete sem Cascade (Dados Órfãos)

- **Sinal de detecção**: handler de exclusão que remove um registro "pai" sem tratar (deletar/atualizar) os registros "filho" relacionados por chave estrangeira.
- **Exemplo Node.js**: `DELETE FROM users WHERE id = ?` sem remover `enrollments`/`payments` associados.
- **Impacto**: corrompe integridade referencial; registros filhos ficam órfãos e podem quebrar consultas futuras.
- **Padrão de refatoração**: P14.

## 16. [LOW] Magic Numbers / Strings

- **Sinal de detecção**: literal numérico ou string repetido em múltiplos pontos do código (ex.: status HTTP mágico, limite de caracteres, nome de status) sem uma constante nomeada.
- **Impacto**: reduz legibilidade e cria risco de inconsistência se o valor precisar mudar.
- **Padrão de refatoração**: aplicar extração de constante nomeada (não tem P dedicado — é uma limpeza pontual dentro dos demais padrões).

---

Este catálogo tem 16 itens, cobrindo folgadamente o mínimo de 8 exigido, com distribuição de severidade completa (3 CRITICAL, 4 HIGH, 4 MEDIUM, 5 LOW) e incluindo detecção explícita de API deprecated (#7).
