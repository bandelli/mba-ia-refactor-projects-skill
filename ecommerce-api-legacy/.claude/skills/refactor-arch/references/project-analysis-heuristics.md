# Heurísticas de Análise de Projeto (Fase 1)

Este documento descreve como detectar, de forma agnóstica de tecnologia, a stack, o domínio e a arquitetura atual de uma codebase. Nenhuma regra aqui deve assumir uma linguagem ou framework específico — cada heurística é uma tabela de sinais por ecossistema, com um ramo explícito para "desconhecido".

## 1. Detecção de linguagem/ecossistema

Procure, na raiz do projeto (e um nível abaixo se a raiz não tiver nenhum sinal), pelo primeiro arquivo-sinal que existir:

| Arquivo-sinal | Ecossistema |
|---|---|
| `requirements.txt`, `pyproject.toml`, `Pipfile`, `setup.py` | Python |
| `package.json` | Node.js/JavaScript (ou TypeScript se houver `tsconfig.json`) |
| `go.mod` | Go |
| `pom.xml`, `build.gradle`, `build.gradle.kts` | Java/Kotlin |
| `Gemfile` | Ruby |
| `composer.json` | PHP |
| `Cargo.toml` | Rust |

Se nenhum desses existir, conte a extensão de arquivo de código dominante (`.py`, `.js`/`.ts`, `.go`, etc.) entre os arquivos fonte e relate como "linguagem inferida por extensão de arquivo — nenhum manifest de dependências encontrado".

## 2. Detecção de framework

Leia as dependências declaradas no arquivo-sinal do passo 1 (seção `dependencies` do `package.json`; linhas do `requirements.txt`/`pyproject.toml`; etc.) e cruze contra os frameworks conhecidos do ecossistema detectado:

| Ecossistema | Frameworks a procurar |
|---|---|
| Python | `flask`, `django`, `fastapi`, `pyramid` |
| Node.js | `express`, `koa`, `fastify`, `nestjs`/`@nestjs/core`, `next` |
| Go | `gin-gonic/gin`, `labstack/echo`, `gofiber/fiber` |
| Java/Kotlin | `spring-boot`, `spring-web`, `micronaut` |
| Ruby | `rails`, `sinatra` |
| PHP | `laravel/framework`, `slim/slim` |

Sempre cite a versão **exatamente como está pinada** no manifest (ex.: `Flask 3.1.1`, `express ^4.18.2`). Se nenhum framework conhecido for encontrado, relate "sem framework web identificado — dependências: [lista]".

## 3. Detecção de banco de dados

Procure, nas dependências e no código-fonte:
- Driver de banco relacional: `sqlite3`, `psycopg2`/`psycopg`, `mysqlclient`/`mysql2`, `pg` (Node).
- ORM: `sqlalchemy`, `flask-sqlalchemy`, `django.db`, `sequelize`, `typeorm`, `prisma`, `gorm`.
- Se houver ORM, liste as classes/models declarados como "tabelas" (nome da classe ou `__tablename__`/`tableName` explícito).
- Se for SQL cru, procure por `CREATE TABLE` no código para listar as tabelas.

## 4. Detecção de domínio da aplicação

Extraia substantivos recorrentes de:
- Nomes de rota (`/produtos`, `/pedidos`, `/tasks`, `/courses`, `/checkout`).
- Nomes de classe/model/tabela.
- Nome de pacotes/pastas de negócio.

Monte uma frase curta de domínio a partir desses substantivos (ex.: "E-commerce API (produtos, pedidos, usuários)", "Task Manager API (tasks, categorias, usuários)", "LMS API com fluxo de checkout (cursos, matrículas, pagamentos)").

## 5. Detecção de arquitetura atual

Classifique a arquitetura contando:
- Número de arquivos de nível superior no diretório do projeto (fora de dependências/build).
- Presença ou ausência de pastas dedicadas: `models/`, `views/`, `routes/`, `controllers/`, `services/`.

Regras:
- **Nenhuma dessas pastas existe** e a lógica de negócio, acesso a dados e rotas estão nos mesmos 2-5 arquivos → **"Monolítica — tudo em N arquivos, sem separação de camadas"**.
- **Algumas dessas pastas existem** (ex.: `models/` e `routes/`, mas sem `controllers/` e com lógica de negócio ainda dentro das rotas) → **"Parcialmente em camadas — separação existente não é consistente"**.
- **Todas as camadas MVC existem e são respeitadas** → **"Já em camadas MVC"** (registrar mesmo assim, pode haver violações pontuais a auditar na Fase 2).

## 6. Contagem de arquivos/LOC

Ao contar "arquivos analisados" e linhas de código para o resumo da Fase 1:
- **Incluir** apenas arquivos de código-fonte do projeto (a linguagem detectada no passo 1).
- **Excluir** diretórios de dependências (`node_modules/`, `venv/`, `.venv/`, `vendor/`), controle de versão (`.git/`), migrations geradas automaticamente, e artefatos de build.
- O número relatado deve bater exatamente com o que um `find`/`ls` filtrado retornaria — este número é conferido no critério de aceite da Fase 1.

## 7. Formato do resumo impresso ao final da Fase 1

```
================================
PHASE 1: PROJECT ANALYSIS
================================
Language:      <linguagem>
Framework:     <framework e versão pinada>
Dependencies:  <dependências relevantes, separadas por vírgula>
Domain:        <frase de domínio>
Architecture:  <classificação da seção 5>
Source files:  <N arquivos analisados>
DB tables:     <lista de tabelas/entidades, se aplicável>
================================
```

Nesta fase, **nenhum arquivo do projeto pode ser criado, editado ou removido** — é uma fase somente-leitura.
