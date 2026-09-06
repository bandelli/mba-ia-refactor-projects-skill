---
name: refactor-arch
description: Audita uma codebase (qualquer linguagem/framework) contra um catálogo de anti-patterns de arquitetura e segurança, gera um relatório de auditoria, e refatora o projeto para o padrão MVC após confirmação humana explícita. Use quando o usuário pedir para analisar, auditar ou refatorar a arquitetura de um projeto.
---

# refactor-arch

Você vai executar 3 fases sequenciais sobre o projeto na raiz atual do repositório (ou no diretório indicado pelo usuário): **Análise → Auditoria → Refatoração**. Cada fase tem um entregável e um limite estrito do que pode ser tocado — respeite isso rigorosamente, mesmo que pareça mais eficiente pular etapas.

Os arquivos de referência abaixo contêm todo o conhecimento de domínio necessário. Leia-os quando a fase correspondente começar — não duplique o conteúdo deles aqui, apenas siga-os:

- `references/project-analysis-heuristics.md` — como detectar stack, domínio e arquitetura (Fase 1).
- `references/anti-patterns-catalog.md` — o que procurar e como classificar severidade (Fase 2).
- `references/audit-report-template.md` — formato exato do relatório (Fase 2).
- `references/mvc-architecture-guidelines.md` — regras da arquitetura MVC alvo (Fase 3).
- `references/refactoring-playbook.md` — como transformar cada anti-pattern em código corrigido (Fase 3).

## Resolução de caminhos

Antes de começar, resolva a raiz do repositório com `git rev-parse --show-toplevel`. O relatório de auditoria da Fase 2 deve ser salvo em `<raiz-do-repo>/reports/audit-project-N.md` (não dentro do projeto sendo analisado).

> Nota de contexto deste desafio (não portável — não repita isto em nenhum arquivo de `references/`): dentro deste repositório específico, N é 1 para `code-smells-project`, 2 para `ecommerce-api-legacy`, 3 para `task-manager-api`. Ao rodar esta skill em qualquer outro projeto fora deste desafio, pergunte ao usuário qual nome/número usar para o relatório, ou use um nome derivado do diretório do projeto.

## Fase 1 — Análise (somente leitura)

Siga `references/project-analysis-heuristics.md` integralmente. Ao final, imprima o bloco de resumo no formato definido lá (`Language / Framework / Dependencies / Domain / Architecture / Source files / DB tables`).

**Restrição**: nesta fase você só pode usar ferramentas de leitura (ler arquivos, listar diretórios, rodar comandos read-only como `find`/`grep`/`git log`). Nenhuma ferramenta de escrita, edição ou exclusão pode ser chamada.

## Fase 2 — Auditoria

Siga `references/anti-patterns-catalog.md` para identificar os anti-patterns presentes, confirmando cada finding com arquivo e linha exatos (leia o trecho antes de citá-lo — nunca aproxime). Preencha `references/audit-report-template.md` e salve o resultado em `<raiz-do-repo>/reports/audit-project-N.md`.

**Restrição**: o único arquivo que pode ser criado nesta fase é esse relatório. Nenhum arquivo do projeto analisado pode ser tocado.

**Critérios mínimos do relatório**: no mínimo 5 findings, com pelo menos 1 CRITICAL ou HIGH, ordenados CRITICAL → LOW.

### Gate humano obrigatório — pare aqui

Depois de salvar o relatório, apresente um resumo dele no chat e imprima literalmente:

```
Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]
```

Em seguida **encerre o turno e aguarde a próxima mensagem do usuário real no chat**. Isto não é uma formalidade decorativa:

- Você não pode assumir "sim" implicitamente, inferir aprovação, nem prosseguir automaticamente para a Fase 3 sob nenhuma circunstância.
- Você não pode chamar nenhuma ferramenta de escrita, edição ou exclusão de arquivos do projeto antes de receber, na próxima mensagem do usuário, uma confirmação afirmativa explícita (`y`, `yes`, `sim`, `confirmo`, ou equivalente inequívoco).
- Qualquer resposta ambígua, uma pergunta de esclarecimento do usuário, um pedido de ajuste no relatório, ou uma resposta negativa deve ser tratada como **não confirmado** — nesse caso, ajuste o relatório conforme pedido (se aplicável) e repita a pergunta; a Fase 3 não roda.
- Este projeto é parte de um exercício acadêmico onde a evidência de que essa confirmação humana realmente aconteceu (a pergunta feita e a resposta literal do usuário) deve ser documentada no `README.md` do repositório — mantenha isso em mente ao formular a pergunta, para que a troca fique clara e citável depois.

## Fase 3 — Refatoração (só após confirmação explícita)

Siga `references/mvc-architecture-guidelines.md` para decidir a árvore de diretórios alvo e `references/refactoring-playbook.md` para aplicar, padrão por padrão, a transformação de cada finding do relatório. Preserve o comportamento observável dos endpoints existentes, exceto quando a própria recomendação do catálogo for remover um endpoint (ex.: execução de SQL arbitrário sem autenticação) — nesse caso, documente a remoção explicitamente no relatório e não a trate como regressão.

Ao final:
1. Rode a validação descrita na seção "Validação da Fase 3" de `references/mvc-architecture-guidelines.md`.
2. Imprima a tabela PASS/FAIL por endpoint.
3. **Não rode `git commit` automaticamente.** Sugira ao usuário o comando de commit apropriado (conventional commits, sem qualquer trailer ou menção a IA/Claude) e pare — quem decide executar o commit é o usuário.
