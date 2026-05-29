# Etapa 5N.5 — mapeamento multi-competência piloto dos grupos CNES ST, LT e SR via PySUS

## 1. Objetivo
Testar a estabilidade estrutural dos grupos ST, LT e SR nas competências 2024-01, 2024-06 e 2024-12, sem persistência de dados.
- não é migração plena;
- não gera base;
- não salva dados;
- não substitui R;
- não valida paridade;
- não aplica transformação;
- não aplica classificação de habilitações.

## 2. Contexto herdado
- 5N reconheceu API funcional;
- 5N.1 resolveu lock DuckDB;
- 5N.2 formalizou retry/backoff/jitter;
- 5N.3 inventariou grupos;
- 5N.3R retestou ST;
- 5N.4 mapeou ST/LT/SR em 2024-01;
- revisão corretiva da 5N.4 carregou contratos CNES com 33 campos críticos e documentou riscos de coerção.

## 3. Ambiente usado
- branch: work
- commit HEAD: fd9caaf66a1e406eceb2b377e53d19ecfa55c028
- último commit: fd9caaf Merge pull request #73 from paulobmcosta-creator/codex/execute-etapa-5n.4-do-plano-de-migracao
- Python: Python 3.12.3
- PySUS: 2.0.4
- caminho PySUS: /workspace/Observatorio_SUS_ES/.venv-5n5-cnes/lib/python3.12/site-packages/pysus/__init__.py
- status inicial/final: somente artefatos da etapa 5N.5 adicionados.

## 4. Arquivos criados/alterados
- docs/migracao_python/05N5_mapeamento_multicompetencia_cnes_pysus.md
- python/observatorio_sus/extract/mapear_multicompetencia_cnes_pysus.py
- tests/python/test_mapear_multicompetencia_cnes_pysus_cli.py

Confirmada ausência de alterações em scripts R, testes R, data_raw, data_interim, data_processed, metadata, docs/cnes e workflows.

## 5. Parâmetros do piloto multi-competência
- UF = ES;
- ano = 2024;
- meses = 1, 6, 12;
- grupos = ST, LT, SR;
- tentativas = 5;
- backoff = 2;
- jitter = 1;
- isolamento aplicado;
- ausência de persistência.

## 6. Resultado geral por grupo e competência
| Grupo | Competência | DataFrame? | Linhas | Colunas | Tentativas | Causa/erro |
|---|---|---:|---:|---:|---:|---|
| ST | 2024-01 | Sim | 8867 | 208 | 1 | GRUPO_ACEITO_COM_RETORNO |
| ST | 2024-06 | Sim | 9035 | 208 | 1 | GRUPO_ACEITO_COM_RETORNO |
| ST | 2024-12 | Sim | 9320 | 208 | 1 | GRUPO_ACEITO_COM_RETORNO |
| LT | 2024-01 | Sim | 1014 | 28 | 1 | GRUPO_ACEITO_COM_RETORNO |
| LT | 2024-06 | Sim | 1015 | 28 | 1 | GRUPO_ACEITO_COM_RETORNO |
| LT | 2024-12 | Sim | 1031 | 28 | 1 | GRUPO_ACEITO_COM_RETORNO |
| SR | 2024-01 | Sim | 20699 | 32 | 1 | GRUPO_ACEITO_COM_RETORNO |
| SR | 2024-06 | Sim | 21189 | 32 | 1 | GRUPO_ACEITO_COM_RETORNO |
| SR | 2024-12 | Sim | 21684 | 32 | 1 | GRUPO_ACEITO_COM_RETORNO |

## 7. Estabilidade de colunas por grupo
| Grupo | Colunas estáveis? | Colunas referência | Colunas adicionadas | Colunas removidas | Observação |
|---|---|---:|---|---|---|
| ST | Sim | 208 | nenhuma | nenhuma | estável |
| LT | Sim | 28 | nenhuma | nenhuma | estável |
| SR | Sim | 32 | nenhuma | nenhuma | estável |

## 8. Estabilidade de dtypes por grupo
| Grupo | Dtypes estáveis? | Dtypes alterados | Observação |
|---|---|---|---|
| ST | Sim | nenhum | estável |
| LT | Sim | nenhum | estável |
| SR | Sim | nenhum | estável |

## 9. Campos-chave por competência
| Grupo | Competência | CNES | CODUFMUN | COMPETEN | TPGESTAO | NAT_JUR | Outros |
|---|---|---|---|---|---|---|---|
| ST | 2024-01 | sim | sim | sim | sim | sim | - |
| ST | 2024-06 | sim | sim | sim | sim | sim | - |
| ST | 2024-12 | sim | sim | sim | sim | sim | - |
| LT | 2024-01 | sim | sim | sim | sim | sim | - |
| LT | 2024-06 | sim | sim | sim | sim | sim | - |
| LT | 2024-12 | sim | sim | sim | sim | sim | - |
| SR | 2024-01 | sim | sim | sim | sim | sim | - |
| SR | 2024-06 | sim | sim | sim | sim | sim | - |
| SR | 2024-12 | sim | sim | sim | sim | sim | - |

## 10. Relação nominal com contratos CNES
Contratos carregados: sim; quantidade de campos críticos: 33; relação nominal: correspondência literal parcial e estável entre competências, com limitações preliminares.

## 11. Riscos de coerção de códigos
| Grupo | Competência | Campos com risco | Observação |
|---|---|---|---|
| ST | 2024-01 | 11 campos | manter texto |
| ST | 2024-06 | 11 campos | manter texto |
| ST | 2024-12 | 11 campos | manter texto |
| LT | 2024-01 | 8 campos | manter texto |
| LT | 2024-06 | 8 campos | manter texto |
| LT | 2024-12 | 8 campos | manter texto |
| SR | 2024-01 | 8 campos | manter texto |
| SR | 2024-06 | 8 campos | manter texto |
| SR | 2024-12 | 8 campos | manter texto |

## 12. Diferenças estruturais relevantes
Sem variações de colunas, dtypes e campos-chave; houve variação de linhas entre competências.

## 13. Testes Python executados
Comando pytest executado com sucesso (36 testes). Não houve rede no teste novo (somente planejamento), e não houve escrita em data_*.

## 14. Perguntas obrigatórias
| Pergunta | Resposta | Evidência | Implicação |
|---|---|---|---|
| 1. A cadeia 5N até 5N.4 existia? | Sim | testes -f | pré-condição atendida |
| 2. As três competências foram testadas? | Sim | 9 combinações | escopo completo |
| 3. ST retornou DataFrame nas três competências? | Sim | JSON operacional | viável |
| 4. LT retornou DataFrame nas três competências? | Sim | JSON operacional | viável |
| 5. SR retornou DataFrame nas três competências? | Sim | JSON operacional | viável |
| 6. As colunas de ST foram estáveis? | Sim | diferenças estruturais | estável |
| 7. As colunas de LT foram estáveis? | Sim | diferenças estruturais | estável |
| 8. As colunas de SR foram estáveis? | Sim | diferenças estruturais | estável |
| 9. Os dtypes foram estáveis? | Sim | diferenças estruturais | estável |
| 10. CNES apareceu nas competências? | Sim | campos-chave | chave presente |
| 11. CODUFMUN apareceu nas competências? | Sim | campos-chave | chave presente |
| 12. COMPETEN apareceu nas competências? | Sim | campos-chave | chave presente |
| 13. Os contratos CNES foram carregados? | Sim | contratos_cnes | referência disponível |
| 14. Houve risco de coerção? | Sim | riscos_coercao_codigos | exige cautela |
| 15. Algum dado foi salvo em data_*? | Não | escopo/teste | sem persistência |
| 16. Algum script R pode ser substituído agora? | Não. Nenhum script R pode ser substituído nesta etapa. | conclusão | R permanece oráculo |

## 15. Classificação da Etapa 5N.5
MAPEAMENTO_MULTICOMPETENCIA_CONCLUIDO.

## 16. Implicações para próxima etapa
Recomendar Etapa 5N.6 — desenho do contrato intermediário PySUS→CNES sem geração de base, ou janela ampliada.

## 17. Riscos remanescentes
instabilidade de rede; variação futura de colunas; coerção de códigos; ausência de CO_UNIDADE literal; necessidade de dicionário PySUS→contratos; paridade posterior com R; R permanece oráculo.

## 18. Critérios de aceite
- [x] Documento 5N.5 criado.
- [x] Script multi-competência criado.
- [x] Testes offline criados.
- [x] Testes executados.
- [x] 9 combinações testadas ou falhas registradas.
- [x] Colunas comparadas.
- [x] Dtypes comparados.
- [x] Campos-chave comparados.
- [x] Riscos de coerção registrados.
- [x] Relação com contratos registrada como preliminar.
- [x] Nenhum dado salvo em data_*.
- [x] Nenhum script R alterado.
- [x] Nenhum metadado alterado.
- [x] Nenhum docs/cnes alterado.
- [x] Nenhum workflow alterado.

## 19. Conclusão
As 9 combinações funcionaram, houve estabilidade estrutural por grupo, há condição para avançar ao contrato intermediário com cautela, sem migração/geração de base/substituição de R.
