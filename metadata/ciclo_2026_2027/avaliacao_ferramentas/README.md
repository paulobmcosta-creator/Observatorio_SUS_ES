# Evidências da avaliação de ferramentas — 22/10/2026

Registro principal: [avaliação](../../../docs/ciclo_2026_2027/avaliacao_ferramentas_2026-10-22.md).
Todos os instantes de execução em JSON são UTC. Responsável: Codex, por solicitação
do pesquisador; não há homologação humana presumida.

| Artefato | Interpretação |
|---|---|
| `fontes_originais.csv` | Candidato, commit/data quando disponíveis, arquivo original, URL permanente e SHA-256. Pyreaddbc usa versão/sdist PyPI, sem commit inventado |
| `pins_repositorios.json` | Revisões efetivamente examinadas; versões instaladas e HEAD não são intercambiáveis |
| `busca_datahub_historico.json` | Escopo acessível pesquisado e identidade ainda não resolvida |
| `aquisicao_20261022.json` | Falha no acesso ao catálogo e na sondagem oficial; não é prova de download, conversão ou ausência de dados |
| `poc_20261022/` | Primeira execução interrompida por expectativa incorreta sobre marcadores DBC; diagnóstico preservado, não aprovada |
| `poc_20261022_v2/` | Execução integral aprovada dentro do escopo delimitado: conversão textual e paridade do percurso com R |
| `ambiente_python.txt` | Dependências base observadas; extra pyreaddbc 2.0.4 instalado separadamente em cache |
| `testes_python.txt` | 55 testes locais aprovados; aviso de depreciação dateutil sem falha |
| `testes_dependencias_ci.txt` | Quatro testes novos aprovados também em ambiente isolado com somente as dependências do workflow; CI remoto não executado |
| `preservacao_sha256.csv` | 268 arquivos preexistentes: 261 idênticos e sete documentos de estado atual atualizados com backup exato |
| `artefatos_sha256.csv` | Novos arquivos e mudanças desta rodada; exclui a si mesmo para evitar referência circular |

Em `poc_20261022_v2`, `manifestos_conversao.json` descreve os três produtos Parquet,
origem, hash, encoding, campos, contagem e digest lógico. O digest lógico serializa
cabeçalho e cada linha como JSON UTF-8 compacto terminado em newline; inclui todas
as células, ordem e multiplicidade. Não equivale a SHA-256 binário do CSV, pois
delimitadores/aspas do contêiner podem mudar na restituição.

`insumos_sha256.json` identifica código e dados efetivos; `produtos_sha256.json`
identifica os derivados locais ignorados pelo Git. `paridade_r.csv` compara os dois
produtos integralmente, e `contrato_r.csv` contém 115 verificações. `duckdb.json`
compara oito medidas com a referência R. `dbc_sintetico.json` e `pysus_parse.json`
usam dados sintéticos; não certificam arquivos oficiais ou indicadores.

Os schemas das duas matrizes são seus cabeçalhos CSV. Na matriz de decisão,
`cobertura_sistema_familia_periodo` distingue capacidade descrita de observação;
`decisao` é orientação de engenharia sob `integracao_e_condicao`, não homologação.
Na matriz por família, `estado_download`, `estado_conversao` e
`estado_equivalencia_metodologica` são dimensões independentes. “Não testado”,
“bloqueado” e “não demonstrada” não significam zero registros ou inexistência da
família. `fallback` deve preservar arquivo e proveniência oficial.

Não há microdados pessoais neste conjunto de evidências. Arquivos grandes e dados
restituídos permanecem na área ignorada `.cache/avaliacao_ferramentas/`; RAW, fontes,
snapshots anteriores e relatório 2025–2026 não foram alterados.
