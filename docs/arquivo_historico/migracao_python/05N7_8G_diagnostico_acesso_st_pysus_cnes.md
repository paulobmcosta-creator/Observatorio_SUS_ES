# Etapa 5N.7-8G — diagnóstico de acesso ST via PySUS/CNES

## 1. Objetivo

Diagnosticar se a falha de ST 2024-01 ocorre no acesso PySUS/CNES ou no transformador, comparando caminhos já existentes que chamam a API pública `from pysus import cnes` sem transformar, sem salvar dados, sem alterar contratos e sem substituir scripts R.

## 2. Contexto

- A 5N.7-8E corrigiu o caminho padrão da transformação para `direto_sem_subprocesso`.
- LT 2024-01 funcionou no caminho direto.
- Na execução ST/LT/SR 2024-01, LT e SR funcionaram, mas ST retornou `TIMEOUT_CONTROLADO`.
- A 5N.7-8F mostrou `TIMEOUT_NA_CHAMADA_PYSUS` para ST, com `ReadTimeout` antes de qualquer transformação.
- A hipótese principal desta etapa é diferenciar instabilidade de acesso PySUS/CNES/ST de problema específico do transformador.

## 3. Hipóteses

- instabilidade PySUS/DATASUS;
- timeout interno da chamada PySUS;
- cache frio;
- isolamento temporário;
- diferença entre scripts;
- problema no transformador.

## 4. Controle 1 — inventariar ST

Comando executado:

```bash
python python/observatorio_sus/extract/inventariar_grupos_cnes_pysus.py --uf ES --ano 2024 --mes 1 --modo testar_grupos --grupos-candidatos ST --tentativas 5 --base-backoff 2 --jitter-max 1
```

Resultado:

| Retornou DataFrame? | Linhas | Colunas | Erro |
|---|---:|---:|---|
| Sim | 8867 | 208 | Nenhum |

Interpretação: o caminho de inventário conseguiu acessar ST 2024-01 e retornar DataFrame no ambiente atual.

## 5. Controle 2 — mapear estrutura ST

Comando executado:

```bash
python python/observatorio_sus/extract/mapear_estrutura_grupos_cnes_pysus.py --uf ES --ano 2024 --mes 1 --grupos ST --modo mapear_estrutura --tentativas 5 --base-backoff 2 --jitter-max 1
```

Resultado:

| Retornou DataFrame? | Linhas | Colunas | Erro |
|---|---:|---:|---|
| Sim | 8867 | 208 | Nenhum |

Interpretação: o caminho de mapeamento estrutural também conseguiu acessar ST 2024-01 e retornar DataFrame.

## 6. Controle 3 — mapear multi-competência reduzido ST

Comando executado:

```bash
python python/observatorio_sus/extract/mapear_multicompetencia_cnes_pysus.py --uf ES --ano 2024 --meses 1 --grupos ST --modo mapear_multicompetencia --tentativas 5 --base-backoff 2 --jitter-max 1
```

Resultado:

| Retornou DataFrame? | Linhas | Colunas | Erro |
|---|---:|---:|---|
| Sim | 8867 | 208 | Nenhum |

Interpretação: o caminho multi-competência reduzido, executando apenas ST 2024-01, também retornou DataFrame.

## 7. Controle 4 — transformação diagnóstico ST

Comando executado:

```bash
python python/observatorio_sus/transform/transformar_memoria_multicompetencia_cnes_pysus.py --uf ES --ano 2024 --meses 1 --grupos ST --modo diagnostico_st_fases --sem-transformacao --payload-resumido --timeout-por-chamada 600 --timeout-global 900
```

Resultado:

| Retornou DataFrame? | Linhas | Colunas | Fase mais lenta | Tempo da chamada CNES (s) | Erro |
|---|---:|---:|---|---:|---|
| Sim | 8867 | 208 | chamada_cnes | 106.378 | Nenhum |

Interpretação: o diagnóstico do transformador, sem transformação e com payload resumido, retornou DataFrame. O tempo da fase `chamada_cnes` foi substancialmente maior que o tempo observado nos caminhos de mapeamento, mas não houve erro nesta execução.

## 8. Chamada mínima direta, se executada

A chamada mínima direta opcional não foi executada, porque os quatro controles obrigatórios retornaram resultado suficiente para comparação: os três caminhos de extração/mapeamento e o diagnóstico do transformador acessaram ST 2024-01 e retornaram DataFrame.

## 9. Comparação dos caminhos

| Caminho | Retornou DataFrame? | Linhas | Colunas | Erro | Interpretação |
|---|---|---:|---:|---|---|
| Inventariar ST | Sim | 8867 | 208 | Nenhum | Acesso ST funcionou fora do transformador. |
| Mapear estrutura ST | Sim | 8867 | 208 | Nenhum | Acesso ST funcionou fora do transformador. |
| Mapear multi-competência reduzido ST | Sim | 8867 | 208 | Nenhum | Acesso ST funcionou fora do transformador. |
| Diagnóstico ST no transformador | Sim | 8867 | 208 | Nenhum | O transformador também acessou ST quando executado sem transformação, mas a chamada foi lenta. |

## 10. Diagnóstico

Classificação da Etapa 5N.7-8G:

`ACESSO_ST_INSTAVEL_INTERMITENTE`

Justificativa:

- Na 5N.7-8F, ST falhou antes de retornar DataFrame, com `ReadTimeout` na fase `chamada_cnes`.
- Na 5N.7-8G, todos os quatro caminhos obrigatórios retornaram DataFrame para ST 2024-01, com 8867 linhas e 208 colunas.
- O diagnóstico do transformador sem transformação também retornou DataFrame, portanto a falha anterior não parece ser causada por transformação, renomeação, preservação textual, metadados ou serialização JSON.
- O tempo de `chamada_cnes` no transformador foi alto, 106.378 segundos, sugerindo sensibilidade a rede, serviço remoto, cache frio ou estado transitório da chamada PySUS/ST.

Classificações consideradas:

- `ACESSO_ST_FUNCIONA_FORA_TRANSFORMADOR`: parcialmente verdadeiro, mas insuficiente porque o transformador também funcionou nesta execução.
- `ACESSO_ST_FALHA_EM_TODOS_OS_CAMINHOS`: descartado nesta execução.
- `ACESSO_ST_INSTAVEL_INTERMITENTE`: adotado, pois houve falha na 5N.7-8F e sucesso na 5N.7-8G.
- `PROBLEMA_ESPECIFICO_TRANSFORMADOR`: descartado nesta execução.
- `DIAGNOSTICO_ST_ACESSO_INCONCLUSIVO`: não adotado, pois os controles comparativos foram suficientes para indicar intermitência.

## 11. Implicações

Como ST foi bem-sucedido em todos os caminhos nesta execução, mas havia falhado na 5N.7-8F:

- não há evidência atual de problema específico do transformador;
- não há evidência de que a transformação em memória seja a causa do timeout, pois o diagnóstico sem transformação retornou DataFrame;
- recomenda-se tratar ST como acesso instável/intermitente;
- recomenda-se adotar retry específico para ST, registro de tempo por fase e eventual estratégia de cache controlado apenas em memória;
- recomenda-se não persistir dados e não executar as 9 combinações até validar ST com transformação resumida e depois transformação padrão em escopo único;
- recomenda-se manter `CO_UNIDADE` bloqueado e não inferido.

## 12. Conclusão

ST 2024-01 pode voltar a ser testado em transformação de escopo único, mas com ressalvas operacionais: o acesso PySUS/CNES/ST mostrou comportamento intermitente entre 5N.7-8F e 5N.7-8G. Nesta etapa, todos os controles retornaram DataFrame com 8867 linhas e 208 colunas, inclusive o diagnóstico do transformador sem transformação.

A causa provável não é o transformador em si, mas instabilidade/intermitência no acesso ST via PySUS/CNES ou sensibilidade a cache/rede/serviço remoto. A próxima etapa deve testar ST 2024-01 com transformação e payload resumido, sem persistência e sem criação de `CO_UNIDADE`, antes de retomar qualquer execução multi-competência.
