# Etapa 5N.2 — diagnóstico da falha operacional pós-isolamento da chamada cnes()

## Objetivo
Diagnosticar com precisão a causa da falha da chamada `cnes(state="ES", year=2024, month=1, group="ST")` após isolamento de ambiente aplicado na 5N.1.

## Pré-condições
Foram confirmados os documentos:
- `docs/migracao_python/05N_reinicio_cnes_python_api_pysus.md`
- `docs/migracao_python/05N1_isolamento_pysus_duckdb_cnes.md`

## Tentativas realizadas (descartando hipóteses)
1. **Hipótese A — lock DuckDB persistente**: descartada. O isolamento cria `config.db` em diretório temporário e não reproduz lock em `/root/pysus/config.db`.
2. **Hipótese B — pacote PySUS quebrado (`pysus.api.utils` ausente)**: descartada nesta rodada. A importação de `pysus.api.utils` funcionou no ambiente de teste.
3. **Hipótese C — erro de conectividade/rede na chamada remota**: observada de forma intermitente (`httpx.ReadTimeout`) em uma execução e descartada como falha estrutural após nova execução bem-sucedida.

## Implementação desta etapa
Arquivos criados/atualizados:
- `python/observatorio_sus/extract/diagnosticar_falha_cnes_pysus.py`
- `tests/python/test_diagnosticar_falha_cnes_pysus_cli.py`
- `docs/migracao_python/05N2_diagnostico_falha_cnes_pos_isolamento.md`

## Estratégia técnica
- Isolamento com `tempfile.TemporaryDirectory()`.
- Redefinição de `HOME`, `XDG_CONFIG_HOME` e `XDG_CACHE_HOME` antes de `from pysus import cnes`.
- Chamada diagnóstica controlada sem persistência em `data_*`.
- Retry com backoff exponencial + jitter foi implementado no script de diagnóstico (`--tentativas`, `--base-backoff`, `--jitter-max`).
- Captura de classe de exceção, mensagem e traceback resumido.
- Classificação da causa conforme taxonomia da etapa 5N.2.

## Resultado desta execução
Executado `--modo chamada_diagnostica` com `ES/2024/1/ST` em múltiplas tentativas.
- Isolamento aplicado: sim.
- Lock DuckDB: não detectado.
- `config.db` temporário: detectado no diretório isolado.
- Tentativa 1: `httpx.ReadTimeout` (classificado como `ERRO_DE_REDE`).
- Tentativa 2: retorno `DataFrame` (classificado como `CHAMADA_FUNCIONOU`).
- Conclusão diagnóstica: a falha pós-isolamento é **intermitente de rede/latência**, não lock DuckDB e não erro fixo de parâmetro/grupo.

## Próxima recomendação
Implementar retry/backoff e timeout explícito para chamada CNES no próximo script operacional, mantendo isolamento de ambiente, e só então avançar ao mapeamento ST/LT/SR.

## Conformidade de escopo
- Nenhum script R alterado.
- Nenhum dado em `data_raw`, `data_interim` ou `data_processed` alterado.
- Nenhum metadado alterado.
- Nenhum arquivo em `docs/cnes` alterado.
- Nenhum workflow alterado.
