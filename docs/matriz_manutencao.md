# Matriz de manutenção documental

Esta matriz define responsabilidade primária, periodicidade mínima de revisão e gatilhos de atualização dos documentos críticos do repositório.

| Documento | Dono primário | Frequência de revisão | Gatilhos de atualização |
|---|---|---|---|
| `README.md` | Desenvolvedor de Dados | Mensal | Mudança de estrutura do repositório, novos scripts centrais, alteração no status do pipeline CNES. |
| `docs/governanca_codigo.md` | Testador e Integrador | Trimestral | Alteração de política de PR/branch, critérios de revisão, mudanças de CI. |
| `docs/fluxo_trabalho.md` | Pesquisador Principal (PI) | Trimestral | Ajuste de processo de contribuição, novo gate metodológico, mudança de governança. |
| `fluxo_trabalho.md` (resumo da raiz) | Desenvolvedor de Dados | Trimestral | Atualização do documento canônico em `docs/fluxo_trabalho.md`. |
| `docs/convensoes_metodologicas.md` | Pesquisador Principal (PI) | Trimestral | Revisão metodológica, mudança em padrões de reprodutibilidade, novos requisitos de documentação. |
| `docs/cnes/README.md` | Desenvolvedor de Dados | Mensal | Inclusão/remoção de scripts CNES, mudança no escopo do piloto, novos testes ou metadados obrigatórios. |
| `docs/cnes/setup_execucao_local_r.md` | Testador e Integrador | Mensal | Mudança em dependências, comandos de teste, sequência de validação ou troubleshooting recorrente. |
| `docs/cnes/roadmap_tecnico_cnes.md` | Pesquisador Principal (PI) | Trimestral | Mudança de priorização técnica, conclusão/início de ciclos, redefinição de dependências analíticas. |
| `metadata/cnes/schema_cnes_piloto.yml` e `metadata/cnes/dicionario_cnes_piloto.csv` | Curador de Metadados | Mensal | Inclusão/remoção/renomeação de campos, mudança de regra de preenchimento, nova versão de saída interim. |
| `docs/cnes/metadados_cnes_piloto.md` | Curador de Metadados | Mensal | Atualização do schema/dicionário, revisão de limitações e regras de preenchimento. |
| `tests/test_metadata_cnes.R` | Testador e Integrador | Mensal | Alteração de campos mínimos, arquivos obrigatórios de metadados, critérios de validação documental. |

## Nota operacional

Quando um gatilho ocorrer, a atualização documental deve ser feita no mesmo PR da mudança técnica correspondente, com registro dos comandos executados e limitações de ambiente no corpo do PR.
