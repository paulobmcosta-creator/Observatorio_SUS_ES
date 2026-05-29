# Etapa 5N.7-8D — diagnóstico do timeout na transformação em memória CNES/PySUS

## 1. Objetivo
Diagnosticar por que `LT 2024-01` entra em `TIMEOUT_CONTROLADO` no script de transformação com subprocesso, apesar de o mapeamento PySUS já ter funcionado em etapas anteriores. O diagnóstico compara o caminho funcional de mapeamento, a transformação com subprocesso e a transformação direta sem subprocesso, sem salvar dados e sem substituir R.

## 2. Contexto
A etapa 5N.5 demonstrou mapeamento multi-competência de `ST`, `LT` e `SR` em `2024-01`, `2024-06` e `2024-12`. A etapa 5N.7-8 criou a transformação em memória PySUS→CNES. Após longa duração operacional, foi adicionado timeout controlado em subprocesso. A etapa 5N.7-8A manteve o timeout como salvaguarda, mas a validação mínima `LT 2024-01` retornou `TIMEOUT_CONTROLADO`. Esta etapa 5N.7-8D compara os caminhos para separar falha de rede/PySUS, subprocesso, serialização e lógica de transformação.

## 3. Hipóteses avaliadas
- Problema de rede/PySUS.
- Problema de subprocesso.
- Problema de isolamento.
- Problema de serialização/queue/multiprocessing.
- Problema da lógica de transformação.

## 4. Teste controle com script de mapeamento
Comando executado:

```bash
python python/observatorio_sus/extract/mapear_multicompetencia_cnes_pysus.py --uf ES --ano 2024 --meses 1 --grupos LT --modo mapear_multicompetencia --tentativas 3 --base-backoff 2 --jitter-max 1
```

Resultado observado para `LT 2024-01`:
- retorno do processo: `0`;
- `sucesso`: `true`;
- `eh_dataframe`: `true`;
- `numero_linhas`: `1014`;
- `numero_colunas`: `28`;
- `causa_classificada`: `GRUPO_ACEITO_COM_RETORNO`;
- `persistiu_dados`: `false`.

Interpretação: o caminho funcional de mapeamento conseguiu acessar PySUS/CNES e retornar DataFrame para `LT 2024-01` no ambiente atual.

## 5. Teste com transformação atual e subprocesso
Comando executado:

```bash
python python/observatorio_sus/transform/transformar_memoria_multicompetencia_cnes_pysus.py --uf ES --ano 2024 --meses 1 --grupos LT --modo transformar_memoria --tentativas 3 --base-backoff 2 --jitter-max 1 --timeout-por-chamada 300 --timeout-global 600
```

Resultado observado para `LT 2024-01`:
- retorno do processo: `0`;
- `sucesso`: `false`;
- `causa_classificada`: `TIMEOUT_CONTROLADO`;
- mensagem: `ReadTimeout`;
- `timeout_controlado`: `true`;
- `tempo_limite_usado`: `300.0`;
- `linhas_antes`/`linhas_depois`: não avaliadas;
- `co_unidade_criado`: `false`;
- `join_relacional_executado`: `false`;
- `persistiu_dados`: `false`.

Interpretação: o caminho com subprocesso falhou antes de obter DataFrame; portanto, a transformação não chegou a ser exercida nesse caminho.

## 6. Teste diagnóstico sem subprocesso
Foi adicionado o modo:

```bash
--modo diagnostico_sem_subprocesso
```

Esse modo chama PySUS diretamente no processo principal, com o mesmo isolamento temporário (`HOME`, `XDG_CONFIG_HOME`, `XDG_CACHE_HOME`), aplica a transformação em memória quando há DataFrame e registra tempos de fase sem salvar dados.

Comando executado:

```bash
python python/observatorio_sus/transform/transformar_memoria_multicompetencia_cnes_pysus.py --uf ES --ano 2024 --meses 1 --grupos LT --modo diagnostico_sem_subprocesso --tentativas 3 --base-backoff 2 --jitter-max 1
```

Resultado observado para `LT 2024-01`:
- retorno do processo: `0`;
- `usa_subprocesso`: `false`;
- `retornou_dataframe`: `true`;
- `linhas_antes`: `1014`;
- `linhas_depois`: `1014`;
- `colunas_antes`: `28`;
- `colunas_depois`: `28`;
- `renomeações`: `10` (`CNES`, `CODLEITO`, `CODUFMUN`, `COMPETEN`, `NAT_JUR`, `QT_EXIST`, `QT_NSUS`, `QT_SUS`, `TPGESTAO`, `TP_LEITO`);
- `campos_preservados_texto`: `CNPJ_MAN`, `CO_CNES`, `CO_MUNICIPIO_GESTOR`, `CPF_CNPJ`, `codigo_leito`;
- `campos_qt_textuais_nao_coercidos`: `qt_existente`, `QT_CONTR`, `qt_sus`, `qt_nsus`;
- `co_unidade_criado`: `false`;
- `join_relacional_executado`: `false`;
- `persistiu_dados`: `false`;
- `sucesso`: `true`;
- `causa_classificada`: `SUCESSO`.

Tempos de fase registrados no diagnóstico direto:

| Fase | Tempo aproximado (s) | Observação |
|---|---:|---|
| isolamento | 0.000 | Variáveis `HOME`, `XDG_CONFIG_HOME` e `XDG_CACHE_HOME` temporárias aplicadas. |
| import PySUS | 2.405 | Import direto no processo principal após isolamento. |
| chamada `cnes()` | 112.061 | Retornou DataFrame para `LT 2024-01`. |
| transformação | 0.009 | Transformação em memória aplicada. |
| geração de metadados | 0.000 | Registro estrutural sem persistência. |

## 7. Comparação dos resultados
| Teste | Retornou DataFrame? | Timeout? | Transformou? | Persistiu dados? | Interpretação |
|---|---|---|---|---|---|
| Mapeamento funcional (`mapear_multicompetencia`) | Sim | Não | Não se aplica; apenas mapeia | Não | PySUS/CNES acessível no ambiente atual para `LT 2024-01`. |
| Transformação com subprocesso | Não | Sim, `TIMEOUT_CONTROLADO`/`ReadTimeout` | Não | Não | Falha ocorre antes do retorno do DataFrame dentro do caminho com subprocesso. |
| Diagnóstico sem subprocesso | Sim | Não | Sim | Não | Transformação em memória funciona quando PySUS é chamado diretamente no processo principal. |

## 8. Diagnóstico provável
O diagnóstico provável é `TIMEOUT_CAUSADO_POR_SUBPROCESSO` no caminho atual de transformação protegida por processo filho. A evidência principal é:

- o script de mapeamento retornou DataFrame para `LT 2024-01`;
- o modo diagnóstico direto sem subprocesso retornou DataFrame e transformou 1014 linhas sem persistência;
- a transformação em memória preservou linhas, não criou `CO_UNIDADE`, não executou join e não salvou dados;
- o caminho com subprocesso falhou antes de retornar DataFrame, logo a lógica de transformação e a serialização de DataFrame transformado não são a causa provável.

A hipótese de rede/PySUS global fica menos provável nesta execução, porque dois caminhos diretos conseguiram acessar PySUS. A hipótese de serialização/queue também fica menos provável, porque o DataFrame não chegou a ser retornado pelo subprocesso.

## 9. Decisão
Como o modo sem subprocesso funcionou, recomenda-se remover o subprocesso do caminho padrão de transformação ou torná-lo uma proteção opcional. O caminho padrão recomendado deve chamar PySUS diretamente após isolamento e aplicar transformação em memória no mesmo processo, mantendo registro de tempos e sem persistência. O subprocesso pode permanecer como modo protegido opcional para cenários de travamento, mas não deve bloquear a validação mínima.

## 10. Classificação
Classificação da etapa 5N.7-8D: `TIMEOUT_CAUSADO_POR_SUBPROCESSO`.

## 11. Próxima etapa
Recomenda-se corrigir a transformação para usar o caminho direto sem subprocesso como padrão operacional controlado, preservando as salvaguardas: não salvar DataFrame, não escrever em `data_*`, não criar `CO_UNIDADE`, não fazer join relacional e não substituir R. Após essa correção, retestar `LT 2024-01` e, se continuar funcionando, avançar para `ST/LT/SR 2024-01` antes de retomar a multi-competência completa.

## Nota pós-5N.7-8E
A correção do caminho padrão foi registrada na etapa 5N.7-8E. O modo `transformar_memoria` passou a usar `direto_sem_subprocesso` por padrão, mantendo o subprocesso apenas como opção explícita via `--usar-subprocesso`.
