# Etapa 5N.7-8E — correção do caminho padrão da transformação em memória CNES/PySUS

## 1. Objetivo
Corrigir o caminho padrão da transformação em memória CNES/PySUS, substituindo o uso padrão de subprocesso por chamada direta sem subprocesso. A correção preserva isolamento temporário, retry/backoff/jitter, ausência de persistência, proibição de `CO_UNIDADE` artificial, proibição de join relacional, preservação textual, metadados antes/depois e tratamento controlado de erro.

## 2. Justificativa
O diagnóstico 5N.7-8D indicou `TIMEOUT_CAUSADO_POR_SUBPROCESSO`: o mapeamento funcional retornou DataFrame para `LT 2024-01`, a transformação com subprocesso falhou com `TIMEOUT_CONTROLADO`/`ReadTimeout`, e a transformação sem subprocesso retornou DataFrame, transformou 1014 linhas em memória, preservou linhas, não criou `CO_UNIDADE`, não fez join e não persistiu dados.

## 3. Decisão técnica
- O caminho padrão passa a ser `direto_sem_subprocesso`.
- O subprocesso permanece disponível apenas quando o usuário informa `--usar-subprocesso`.
- `--timeout-por-chamada` e `--timeout-global` permanecem disponíveis; no caminho direto, funcionam como metadados/controle global, sem kill de subprocesso.
- Nenhuma persistência é permitida.
- Nenhum script R é substituído.
- `CO_UNIDADE` não é criado artificialmente.
- Join relacional continua proibido.

## 4. Resultado LT 2024-01
Comando executado:

```bash
python python/observatorio_sus/transform/transformar_memoria_multicompetencia_cnes_pysus.py --uf ES --ano 2024 --meses 1 --grupos LT --modo transformar_memoria --tentativas 3 --base-backoff 2 --jitter-max 1 --timeout-por-chamada 300 --timeout-global 600
```

| Caminho | Grupo | Competência | Sucesso? | DataFrame? | Linhas antes | Linhas depois | CO_UNIDADE criado? | Persistiu dados? |
|---|---|---|---|---|---:|---:|---|---|
| direto_sem_subprocesso | LT | 2024-01 | Sim | Sim | 1014 | 1014 | Não | Não |

Resultado estrutural adicional:
- colunas antes: `28`;
- colunas depois: `28`;
- renomeações aplicadas: `10`;
- classificação do script: `TRANSFORMACAO_MEMORIA_MINIMA_CONCLUIDA_COM_RESSALVAS`;
- causa classificada por combinação: `SUCESSO`.

## 5. Resultado ST/LT/SR 2024-01, se executado
Como `LT 2024-01` funcionou, a expansão para `ST/LT/SR 2024-01` foi executada sem rodar as 9 combinações multi-competência.

Comando executado:

```bash
python python/observatorio_sus/transform/transformar_memoria_multicompetencia_cnes_pysus.py --uf ES --ano 2024 --meses 1 --grupos ST LT SR --modo transformar_memoria --tentativas 3 --base-backoff 2 --jitter-max 1 --timeout-por-chamada 300 --timeout-global 1200
```

| Caminho | Grupo | Competência | Sucesso? | DataFrame? | Linhas antes | Linhas depois | CO_UNIDADE criado? | Persistiu dados? |
|---|---|---|---|---|---:|---:|---|---|
| direto_sem_subprocesso | ST | 2024-01 | Não | Não | - | - | Não | Não |
| direto_sem_subprocesso | LT | 2024-01 | Sim | Sim | 1014 | 1014 | Não | Não |
| direto_sem_subprocesso | SR | 2024-01 | Sim | Sim | 20699 | 20699 | Não | Não |

Resultado estrutural adicional:
- `ST 2024-01`: `TIMEOUT_CONTROLADO`, sem DataFrame retornado;
- `LT 2024-01`: 28 colunas antes/depois, 10 renomeações, sucesso;
- `SR 2024-01`: 32 colunas antes/depois, 10 renomeações, sucesso;
- classificação do script: `TRANSFORMACAO_MEMORIA_MINIMA_PARCIAL`.

## 6. Validações
| Validação | Resultado | Observação |
|---|---|---|
| Linhas antes = depois | Aprovado para LT e SR; não avaliado para ST | `LT` manteve 1014 linhas; `SR` manteve 20699 linhas; `ST` não retornou DataFrame. |
| `CO_UNIDADE` não criado | Aprovado | `co_unidade_criado=false` em todas as combinações executadas. |
| Join não executado | Aprovado | `join_relacional_executado=false`. |
| `data_*` não alterado | Aprovado | Nenhum dado foi salvo em `data_raw`, `data_interim` ou `data_processed`. |
| R não substituído | Aprovado | Nenhum script R foi alterado ou executado. |
| Persistência ausente | Aprovado | `persistiu_dados=false` em todos os resultados. |
| Subprocesso não padrão | Aprovado | `--usar-subprocesso` existe, mas não foi usado no caminho padrão. |

## 7. Classificação
Classificação da etapa 5N.7-8E: `CAMINHO_PADRAO_CORRIGIDO_COM_RESSALVAS`.

Justificativa: `LT 2024-01` funcionou no caminho direto padrão, comprovando que o problema do subprocesso foi contornado no caso mínimo. A expansão `ST/LT/SR 2024-01` foi parcial, pois `LT` e `SR` funcionaram, mas `ST` retornou `TIMEOUT_CONTROLADO` no ambiente atual.

Classificações de referência:
- `CAMINHO_PADRAO_CORRIGIDO_COM_SUCESSO`: não aplicável porque `ST` falhou na expansão de competência única;
- `CAMINHO_PADRAO_CORRIGIDO_COM_RESSALVAS`: aplicável;
- `CAMINHO_PADRAO_AINDA_INCONCLUSIVO`: não aplicável porque `LT` e `SR` transformaram;
- `CAMINHO_PADRAO_FALHOU`: não aplicável.

## 8. Implicações
Como `LT 2024-01` funcionou, mas `ST/LT/SR 2024-01` foi parcial, recomenda-se:
- investigar a chamada `ST 2024-01` no caminho direto antes de retomar a multi-competência completa;
- manter `direto_sem_subprocesso` como padrão operacional;
- manter `--usar-subprocesso` apenas como proteção opcional/diagnóstica;
- não executar ainda as 9 combinações multi-competência;
- não gerar base, não escrever em `data_interim` e não substituir R.

## 9. Conclusão
O problema do subprocesso foi contornado para o caso mínimo: o modo `transformar_memoria` agora usa o caminho direto sem subprocesso por padrão, e `LT 2024-01` transformou 1014 linhas em memória sem persistência, sem criação de `CO_UNIDADE` e sem join relacional. A expansão para `ST/LT/SR 2024-01` teve sucesso em `LT` e `SR`, mas `ST` ainda retornou timeout controlado. A próxima etapa deve investigar `ST 2024-01` no caminho direto ou repetir a competência única em ambiente mais estável antes de retomar a validação multi-competência completa.
