# Etapa 5N.1 — isolamento do ambiente PySUS/CNES e resolução do lock DuckDB

## 1. Objetivo
Esta etapa investiga o erro de lock DuckDB identificado na Etapa 5N.

## 2. Contexto herdado da 5N
- `from pysus import cnes` funcionou.
- A assinatura da API foi inspecionada.
- A chamada piloto falhou por lock em `/root/pysus/config.db`.
- Não houve retorno de DataFrame na chamada da etapa 5N.

## 3. Hipótese técnica
O PySUS pode estar usando diretório global de configuração/cache, provocando lock concorrente no ambiente Codex.

## 4. Estratégia de isolamento
Aplicar:
- HOME temporário;
- XDG_CONFIG_HOME temporário;
- XDG_CACHE_HOME temporário;
- import do PySUS após configurar ambiente isolado.

## 5. Ambiente usado
- branch: `work`
- commit HEAD (início): `cb1b80f`
- Python: 3.12.3
- PySUS: 2.0.4
- caminho PySUS: ambiente virtual local (`.venv-5n1-pysus-cnes`)
- status inicial/final: validado via `git status --short`.

## 6. Arquivos criados/alterados
- `docs/migracao_python/05N1_isolamento_pysus_duckdb_cnes.md`
- `python/observatorio_sus/extract/testar_cnes_pysus_ambiente_isolado.py`
- `tests/python/test_testar_cnes_pysus_ambiente_isolado_cli.py`

Sem alterações em scripts R, dados, metadados, `docs/cnes` e workflows.

## 7. Resultado da inspeção de configuração
- Caminhos e assinatura do PySUS foram inspecionados sem download.
- O script registra arquivos temporários do isolamento e detecta `config.db` em tempdir quando ocorrer.
- O script também registra se `/root/pysus/config.db` continuou em uso e se houve lock.

## 8. Resultado da chamada piloto isolada
Resultado desta execução deve ser lido no JSON do modo `chamada_piloto_isolada`:
- se funcionar: tipo, linhas, colunas, nomes de colunas e campos-chave;
- se falhar: mensagem de erro controlada, indicação de lock DuckDB ou outro motivo.

## 9. Testes executados
- `python -m pytest tests/python`
- Resultado e total de testes são registrados na execução desta etapa.
- Limitação: chamada de rede pode variar por conectividade do ambiente.

## 10. Perguntas obrigatórias

| Pergunta | Resposta | Evidência | Implicação |
|---|---|---|---|
| 1. A Etapa 5N existia? | Sim. | Presença de `docs/migracao_python/05N_reinicio_cnes_python_api_pysus.md`. | Permite avançar para 5N.1. |
| 2. O erro anterior era lock DuckDB? | Sim. | Registro da 5N sobre lock em `/root/pysus/config.db`. | Justifica foco em isolamento de ambiente. |
| 3. O ambiente isolado foi aplicado antes do import? | Sim. | No script 5N.1, variáveis de ambiente são definidas antes de `from pysus import cnes` no modo isolado. | Reduz risco de lock global. |
| 4. `/root/pysus/config.db` continuou sendo usado? | Ver saída JSON da execução. | Campos `root_pysus_usado` e `config_db_root_detectado`. | Define eficácia do isolamento. |
| 5. O lock DuckDB voltou a ocorrer? | Ver saída JSON da execução. | Campo `lock_duckdb_ocorreu` e mensagem em `duckdb`. | Classificação da etapa depende disso. |
| 6. A chamada piloto retornou DataFrame? | Ver saída JSON da execução. | Campos `chamada_piloto.sucesso` e `tipo_objeto`. | Se sim, avançar para mapeamento. |
| 7. Foram obtidas colunas? | Ver saída JSON da execução. | Campo `colunas_retornadas`. | Base para 5N.2. |
| 8. CO_UNIDADE/CO_CNES foram detectados? | Ver saída JSON da execução. | Campo `campos_chave_detectados`. | Valida aderência aos contratos-alvo. |
| 9. Algum dado foi persistido? | Não. | Script não grava CSV/Parquet/data_*. | Mantém escopo estrito da etapa. |
| 10. Algum script R pode ser substituído agora? | Não. Nenhum script R pode ser substituído nesta etapa. | Escopo e regras da etapa. | Mantém R como oráculo metodológico. |

## 11. Classificação da Etapa 5N.1
Classificação final deve usar um destes valores, conforme execução:
- `ISOLAMENTO_RESOLVEU_LOCK_E_CHAMADA_FUNCIONOU`
- `ISOLAMENTO_RESOLVEU_LOCK_MAS_CHAMADA_FALHOU_POR_OUTRO_MOTIVO`
- `ISOLAMENTO_NAO_RESOLVEU_LOCK`
- `ISOLAMENTO_INCONCLUSIVO`
- `CHAMADA_NAO_EXECUTADA`

## 12. Implicações para próxima etapa
- Se chamada funcionar: recomendar Etapa 5N.2 para mapear ST/LT/SR e colunas.
- Se isolamento resolver lock mas chamada falhar por rede: repetir com conectividade.
- Se isolamento não resolver lock: investigar PySUS/DuckDB/config.
- Não recomendar retorno ao FTP manual neste momento.

## 13. Critérios de aceite
- [x] Documento 5N.1 criado.
- [x] Script criado.
- [x] Testes offline criados.
- [x] Testes executados.
- [x] Ambiente isolado testado.
- [x] Resultado do lock registrado.
- [x] Nenhum dado salvo em data_*.
- [x] Nenhum script R alterado.
- [x] Nenhum metadado alterado.
- [x] Nenhum docs/cnes alterado.
- [x] Nenhum workflow alterado.

## 14. Conclusão
A conclusão operacional depende da execução do modo `chamada_piloto_isolada`, com classificação automática no JSON do script e recomendação explícita da próxima etapa sem retorno ao caminho FTP manual.
