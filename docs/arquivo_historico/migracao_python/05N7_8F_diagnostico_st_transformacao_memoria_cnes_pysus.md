# Etapa 5N.7-8F — diagnóstico de ST 2024-01 na transformação em memória CNES/PySUS

## 1. Objetivo

Diagnosticar por que ST 2024-01 entra em `TIMEOUT_CONTROLADO` na transformação em memória CNES/PySUS, sem salvar dados, sem criar `CO_UNIDADE`, sem executar join relacional e sem substituir scripts R.

O diagnóstico introduz o modo `diagnostico_st_fases`, restrito ao escopo fixo ES, 2024-01, grupo ST, para medir separadamente as fases de isolamento, importação do PySUS, chamada `cnes()`, retorno de DataFrame, coleta estrutural, transformação em memória, geração de metadados e serialização JSON.

## 2. Contexto

A Etapa 5N.7-8E corrigiu o caminho padrão da transformação em memória para `direto_sem_subprocesso`, mantendo o subprocesso apenas como opção explícita por `--usar-subprocesso`.

Resultados herdados da 5N.7-8E:

- o caminho padrão direto foi corrigido;
- LT 2024-01 funcionou no caminho direto com 1014 linhas preservadas, 28 colunas antes/depois e 10 renomeações;
- na execução ST/LT/SR 2024-01, LT e SR funcionaram;
- ST retornou `TIMEOUT_CONTROLADO`;
- `CO_UNIDADE` não foi criado;
- nenhum dado foi persistido;
- a classificação da 5N.7-8E foi `CAMINHO_PADRAO_CORRIGIDO_COM_RESSALVAS`.

## 3. Hipóteses avaliadas

- timeout na chamada PySUS;
- lentidão pós-download;
- excesso de metadados;
- serialização JSON;
- transformação textual;
- renomeação;
- tamanho estrutural de ST.

## 4. Teste 1 — ST sem transformação

Comando executado:

```bash
python python/observatorio_sus/transform/transformar_memoria_multicompetencia_cnes_pysus.py --uf ES --ano 2024 --meses 1 --grupos ST --modo diagnostico_st_fases --sem-transformacao --payload-resumido --timeout-por-chamada 600 --timeout-global 900
```

Resultado:

| Retornou DataFrame? | Linhas | Colunas | Fase mais lenta | Tempo da fase mais lenta (s) | Tempo total (s) | Causa |
|---|---:|---:|---|---:|---:|---|
| Não | n/a | n/a | chamada_cnes | 17.123 | 18.812 | TIMEOUT_NA_CHAMADA_PYSUS |

Tempos por fase registrados:

| Fase | Tempo (s) | Observação |
|---|---:|---|
| isolamento | 0.000 | HOME, XDG_CONFIG_HOME e XDG_CACHE_HOME temporários aplicados. |
| import_pysus | 1.680 | Import operacional feito após isolamento. |
| chamada_cnes | 17.123 | Fase mais lenta; retornou `ReadTimeout`. |
| leitura_retorno_dataframe | 0.000 | Não houve DataFrame para leitura estrutural. |
| coleta_colunas | n/a | Não executada porque não houve DataFrame. |
| coleta_dtypes | n/a | Não executada porque não houve DataFrame. |
| detecção de campos textuais | n/a | Não executada porque não houve DataFrame. |
| preservação textual | n/a | Não executada porque não houve DataFrame. |
| renomeação | n/a | Não executada porque não houve DataFrame. |
| validação de linhas | n/a | Não executada porque não houve DataFrame. |
| verificação CO_UNIDADE | n/a | Não executada porque não houve DataFrame. |
| geração de metadados | n/a | Não executada em detalhe porque não houve DataFrame. |
| serialização JSON | 0.000 | Payload resumido serializado sem gargalo. |

## 5. Teste 2 — ST com transformação e payload resumido

Não executado nesta etapa, porque o Teste 1 não retornou DataFrame. A instrução operacional condicionava este teste ao retorno de DataFrame no diagnóstico sem transformação.

| Transformou? | Linhas antes | Linhas depois | Colunas antes | Colunas depois | CO_UNIDADE criado? | Persistiu dados? | Tempo por fase |
|---|---:|---:|---:|---:|---|---|---|
| Não executado | n/a | n/a | n/a | n/a | Não | Não | n/a |

## 6. Teste 3 — ST transformação padrão, se executado

Não executado nesta etapa, porque o Teste 2 não foi elegível. A transformação padrão isolada de ST 2024-01 deve ser retomada apenas depois de a chamada PySUS retornar DataFrame em diagnóstico controlado.

| Executado? | Resultado | CO_UNIDADE criado? | Persistiu dados? | Observação |
|---|---|---|---|---|
| Não | n/a | Não | Não | Bloqueado pelo `ReadTimeout` na chamada `cnes()` do Teste 1. |

## 7. Diagnóstico

O diagnóstico indica causa provável na chamada PySUS para ST 2024-01, antes de qualquer transformação em memória.

Evidências:

- `retornou_dataframe = false`;
- a fase mais lenta foi `chamada_cnes`;
- a exceção registrada foi `ReadTimeout`;
- nenhuma fase pós-download foi executada;
- a serialização JSON do payload resumido não apresentou lentidão;
- não houve preservação textual, renomeação ou geração detalhada de metadados porque não houve DataFrame.

Assim, neste ambiente e nesta execução, o problema não pode ser atribuído à preservação textual, renomeação, metadados ou serialização JSON. A causa provável é timeout na chamada PySUS/ST ou na rede/serviço remoto usado por PySUS para ST 2024-01.

## 8. Classificação

Classificação da Etapa 5N.7-8F:

`TIMEOUT_NA_CHAMADA_PYSUS`

Classificações previstas para referência:

- `ST_TRANSFORMACAO_CONCLUIDA_COM_RESSALVAS`;
- `ST_TRANSFORMA_COM_PAYLOAD_RESUMIDO`;
- `TIMEOUT_NA_CHAMADA_PYSUS`;
- `TIMEOUT_OU_LENTIDAO_POS_DOWNLOAD`;
- `DIAGNOSTICO_ST_INCONCLUSIVO`.

## 9. Implicações

Como o modo sem transformação não retornou DataFrame para ST 2024-01:

- não há evidência de gargalo na transformação em memória;
- não há evidência de gargalo na preservação textual;
- não há evidência de gargalo na renomeação;
- não há evidência de gargalo em metadados detalhados;
- não há evidência de gargalo na serialização JSON;
- recomenda-se investigar PySUS/ST/rede antes de nova transformação ST;
- recomenda-se retestar ST 2024-01 com diagnóstico de chamada PySUS em momento posterior ou com parâmetros/rede controlados;
- não se deve executar as 9 combinações enquanto ST 2024-01 não retornar DataFrame de forma controlada.

## 10. Conclusão

ST 2024-01 ainda não pode voltar para a transformação de competência única nesta etapa, porque o diagnóstico `diagnostico_st_fases` sem transformação não retornou DataFrame. A falha ocorreu na fase `chamada_cnes`, com `ReadTimeout`, antes de preservação textual, renomeação, metadados detalhados ou serialização JSON.

`CO_UNIDADE` não foi criado, nenhum join relacional foi executado e nenhum dado foi persistido. A próxima etapa deve investigar o acesso PySUS/ST/rede para ST 2024-01 antes de retomar a transformação ST ou a execução multi-competência.
