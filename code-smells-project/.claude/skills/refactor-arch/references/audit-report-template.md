# Template do Relatório de Auditoria (Fase 2)

Preencha exatamente esta estrutura ao gerar `reports/audit-project-N.md`. Os findings devem estar ordenados por severidade, **CRITICAL → HIGH → MEDIUM → LOW**, e cada um deve ter arquivo e linha(s) exatos (nunca aproximados).

```markdown
================================
ARCHITECTURE AUDIT REPORT
================================
Project: <nome do projeto>
Stack:   <linguagem + framework>
Files:   <N> analyzed | ~<LOC> lines of code

Summary
CRITICAL: <n> | HIGH: <n> | MEDIUM: <n> | LOW: <n>

Findings

[<SEVERIDADE>] <Nome do anti-pattern>
File: <caminho/arquivo.ext>:<linha ou intervalo de linhas>
Description: <o que foi encontrado, de forma objetiva e verificável>
Impact: <consequência concreta se não for corrigido>
Recommendation: <qual padrão do playbook resolve isso, em uma frase>

[... repetir para cada finding, na ordem de severidade ...]

================================
Total: <N> findings
================================

Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]
```

## Regras de preenchimento

1. **Cada finding referencia o anti-pattern correspondente do `anti-patterns-catalog.md`** pelo nome exato usado no catálogo.
2. **`File`** deve ser o caminho relativo à raiz do projeto (não da skill), e a linha deve ser a linha real onde o problema começa (ou o intervalo exato, ex.: `models.py:171-201`). Nunca aproximar (`~linha X`) — sempre confirmar lendo o arquivo antes de escrever o relatório.
3. **`Recommendation`** deve citar o padrão de refatoração pelo identificador do `refactoring-playbook.md` (ex.: "Aplicar P2 — parametrizar a query").
4. O relatório deve ter, no mínimo, **5 findings**, com pelo menos **1 CRITICAL ou HIGH** entre eles — este é um critério de aceite obrigatório.
5. Ao final, a skill **imprime a linha de confirmação literal** (`Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]`) e **para** — ver a seção de gate humano no `SKILL.md`. Nenhuma ferramenta de escrita/edição/exclusão de arquivos do projeto pode ser chamada depois deste ponto até uma confirmação explícita do usuário.
6. O único arquivo que pode ser criado durante a Fase 2 é o próprio relatório de auditoria — nada mais é escrito nesta fase.
