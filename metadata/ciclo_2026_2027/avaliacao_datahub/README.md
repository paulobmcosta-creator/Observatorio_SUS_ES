# Evidências da complementação DataHub — 22/10/2026

Ler a [avaliação](../../../docs/ciclo_2026_2027/avaliacao_datahub_2026-10-22.md) e a [matriz](../../../docs/ciclo_2026_2027/matriz_decisao_ferramentas.csv). Instantes de execução em UTC.

- `identificacao.json`, `historico_git.txt`, `fontes_originais.csv`: identidade fornecida pelo usuário, pin, licença, manutenção e 37 arquivos originais com hashes/URLs.
- `datahub-metadados.csv`, `datahub-pa-metadados.csv`: cópias exatas do repositório original pinado; metadados declarados pelo mantenedor, sem auditoria dos microdados Kaggle.
- `poc_20261022/`: seis casos locais, versões, hashes de todo checkout, insumos/produtos e resultados agregados. Microdados derivados permanecem no cache ignorado; valores de registros publicados nos resultados são exclusivamente sintéticos.
- `poc_execucao.txt`: log integral. O código original não foi alterado. `integridade` e `equivalencia_metodologica` são conclusões distintas do sucesso da execução.
- `ambiente_base.txt`, `dependencias_isoladas.json`: ambiente base preservado e dois extras de PoC; a pilha completa do candidato não foi instalada.
- `verificacao.json`, `preservacao_sha256.csv`, `artefatos_sha256.csv`: conferência dos resultados/artefatos e preservação do estado anterior. Os manifestos históricos de `avaliacao_ferramentas/` não foram reescritos; hashes documentais daquela rodada referem-se ao estado anterior, recuperável pelo novo ZIP.

Reprodução a partir da raiz, com checkout original no pin e referência R disponível com o mesmo hash:

```bash
git clone https://github.com/rafa-trindade/kaggle-datahub.git .cache/datahub-original
git -C .cache/datahub-original checkout --detach 60aa9cbd82509e0595d5c99ec74794e6be1588bd
UV_CACHE_DIR=/workspace/.setup-observatorio/uv-cache UV_SYSTEM_CERTS=true \
  uv pip install --python .venv/bin/python --no-deps \
  --target .cache/avaliacao_datahub/dependencias datasus-dbc==0.1.3 simpledbf==0.2.6
PYTHONPATH=.cache/avaliacao_datahub/dependencias \
  .venv/bin/python scripts/executar_poc_datahub.py \
  .cache/datahub-original .cache/avaliacao_datahub/repeticao \
  metadata/ciclo_2026_2027/avaliacao_datahub/repeticao
```

Usar destinos novos; não sobrescrever o ensaio preservado. A execução registrada usou o checkout externo `/workspace/.cache/avaliacao-ferramentas/kaggle-datahub`; argumentos exatos em `poc_20261022/execucao.json`. A versão do ambiente base é relevante: a PoC não valida automaticamente outras versões de DuckDB/Arrow. Não executar os programas de aquisição/publicação ou baixar todas as bases para reproduzir estes casos. Nenhuma credencial Kaggle/MinIO é necessária para a prova local.
