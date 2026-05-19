# Fluxo de Trabalho no Observatório SUS ES

Este documento da raiz é um **resumo executivo** do fluxo de trabalho do projeto.

## Documento canônico

A referência oficial e normativa para o fluxo operacional de contribuição é:

- `docs/fluxo_trabalho.md`

Em caso de divergência entre este resumo e o documento completo, **prevalece** `docs/fluxo_trabalho.md`.

## Resumo em 8 passos

1. Definir a tarefa e registrar issue com escopo e critérios de aceite.
2. Criar branch a partir de `main`.
3. Desenvolver mudanças pequenas, rastreáveis e alinhadas às convenções metodológicas.
4. Validar localmente estrutura, caminhos, metadados e dependências.
5. Executar testes/checks aplicáveis e registrar os comandos.
6. Abrir PR com resumo, solução, arquivos alterados, validações e limitações.
7. Realizar revisão técnica/metodológica conforme risco da mudança.
8. Fazer merge após aprovação e checks satisfatórios.

## Convenção única de branch naming

As branches devem seguir os prefixos:

- `feat/` para novas funcionalidades
- `fix/` para correções
- `docs/` para documentação
- `test/` para testes
- `chore/` para manutenção

## Observações

- Mudanças científicas, metodológicas e de dados sensíveis devem seguir a governança definida em `AGENTS.md`.
- Para detalhes operacionais completos (inclusive checklist de PR), consulte o documento canônico em `docs/fluxo_trabalho.md`.
