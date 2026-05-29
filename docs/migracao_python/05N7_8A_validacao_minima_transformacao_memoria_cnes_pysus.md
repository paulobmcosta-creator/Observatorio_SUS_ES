# Etapa 5N.7-8A — validação mínima da transformação em memória PySUS→CNES

## 1. Objetivo
Validar a transformação em memória PySUS→CNES em escopo mínimo antes de retomar a execução multi-competência. O escopo inicial definido foi o grupo `LT` na competência `2024-01`, sem persistência de dados, sem criação de `CO_UNIDADE`, sem join relacional e sem substituição de R.

## 2. Justificativa
A 5N.7-8 completa retornou `TIMEOUT_CONTROLADO` nas 9 combinações (`ST`, `LT`, `SR` × `2024-01`, `2024-06`, `2024-12`). Por isso, a transformação multi-competência não foi avaliada operacionalmente e a validação precisa recomeçar por escopo menor.

## 3. Decisão sobre timeout
O timeout controlado foi mantido, não removido. Ele impede travamento indefinido da CLI, preserva saída JSON auditável e permite classificar a limitação operacional sem persistir dados. O ajuste tornou o timeout explicitamente parametrizável por:

- `--timeout-por-chamada`
- `--timeout-global`

## 4. Parâmetros
| Parâmetro | Valor usado |
|---|---|
| Grupo inicial | `LT` |
| Competência | `2024-01` |
| Timeout por chamada | `300` segundos |
| Timeout global | `600` segundos |
| Tentativas | `3` |
| Backoff | `2` |
| Jitter | `1` |
| Persistência | Não |
| `CO_UNIDADE` artificial | Não |
| Join relacional | Não |

## 5. Resultado LT 2024-01
A execução mínima retornou de forma controlada e não persistiu dados. No ambiente atual, `LT 2024-01` não retornou DataFrame para transformação; a limitação foi classificada como timeout controlado operacional.

| Grupo | Competência | Sucesso? | Linhas antes | Linhas depois | Colunas antes | Colunas depois | Renomeações | Timeout? | Persistiu dados? |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| LT | 2024-01 | Não | - | - | 0 | 0 | 0 | Sim | Não |

## 6. Resultado ST/LT/SR 2024-01, se executado
A expansão para `ST/LT/SR 2024-01` não foi executada, porque `LT 2024-01` não transformou com sucesso no ambiente atual. Essa decisão evita ampliar o escopo enquanto a validação mínima permanece não avaliada por timeout.

| Grupo | Competência | Sucesso? | Linhas antes | Linhas depois | Colunas antes | Colunas depois | Renomeações | Timeout? | Persistiu dados? |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| ST | 2024-01 | Não executado | - | - | - | - | - | - | Não |
| LT | 2024-01 | Não executado nesta expansão | - | - | - | - | - | - | Não |
| SR | 2024-01 | Não executado | - | - | - | - | - | - | Não |

## 7. Validações
| Validação | Resultado | Observação |
|---|---|---|
| Linhas preservadas | Não avaliado | Não houve DataFrame retornado para `LT 2024-01`. |
| `CO_UNIDADE` não criado | Aprovado | O resultado controlado manteve `co_unidade_criado=false`. |
| Join não executado | Aprovado | O resultado controlado manteve `join_relacional_executado=false`. |
| `data_*` não alterado | Aprovado | O script não escreve em `data_raw`, `data_interim` ou `data_processed`. |
| R não substituído | Aprovado | Nenhum script R foi alterado ou executado. |
| Persistência ausente | Aprovado | O resultado controlado manteve `persistiu_dados=false`. |

## 8. Classificação
Classificação da 5N.7-8A no ambiente atual: `TRANSFORMACAO_MEMORIA_MINIMA_NAO_AVALIADA_POR_TIMEOUT`.

Classificações possíveis para futuras reexecuções:
- `TRANSFORMACAO_MEMORIA_MINIMA_CONCLUIDA_COM_RESSALVAS`
- `TRANSFORMACAO_MEMORIA_MINIMA_PARCIAL`
- `TRANSFORMACAO_MEMORIA_MINIMA_NAO_AVALIADA_POR_TIMEOUT`
- `TRANSFORMACAO_MEMORIA_MINIMA_FALHOU`

## 9. Implicações
- Se `LT 2024-01` funcionar em ambiente posterior, recomenda-se testar `ST/LT/SR 2024-01`.
- Se `ST/LT/SR 2024-01` funcionar, recomenda-se retomar gradualmente a validação multi-competência.
- Se continuar timeout, recomenda-se investigar desempenho, rede, ambiente PySUS, cache temporário e disponibilidade da API antes de nova transformação.

Não se recomenda gerar base, escrever em `data_interim`, substituir R, criar `CO_UNIDADE` artificial ou fazer join relacional nesta etapa.
