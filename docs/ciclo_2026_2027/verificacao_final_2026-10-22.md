# Verificação final da primeira rodada — 22/10/2026

## Execução técnica

Ambiente local: R 4.5.0, Debian 13. O projeto mantém CI em R 4.3; execução remota não realizada. Nenhuma dependência R adicional foi introduzida.

| Comando/conjunto | Resultado comprovado |
|---|---|
| Nove scripts R já presentes no workflow, executados individualmente da raiz | Todos concluídos com código 0 nesta rodada |
| `Rscript tests/test_conferir_contrato_snapshot_cnes.R` | 14 cenários concluídos; código 0 |
| `Rscript scripts/conferir_snapshot_cnes.R metadata/ciclo_2026_2027/execucoes/rodada_01_20261022_v2 'Codex (agente automatizado), solicitado pelo usuário nesta tarefa'` | Código 1; 61 verificações passaram, 7 falharam, 4 não executadas; dado reprovado conforme diagnóstico |
| SHA-256 dos insumos, código, teste e produtos registrados | Todos conferem com os manifestos da execução canônica |
| CSVs novos, IDs matriz/avaliação, cronograma e dependências das tarefas | Estrutura e correspondências conferidas; sem atribuição automática de validade científica |
| Links Markdown locais das entregas | Conferidos contra arquivos existentes |
| `git diff --check` | Sem erro de whitespace |

Os nove scripts existentes foram: `test_estrutura_repositorio.R`, `test_metadata_cnes.R`, `test_classificacao_habilitacoes_cnes.R`, `test_ler_arquivos_cnes.R`, `test_padronizar_cnes_interim.R`, `test_validar_pipeline_cnes.R`, `test_executar_pipeline_piloto_cnes.R`, `teste_pipeline_piloto_cnes.R` e `test_indicadores_cnes_oferta.R`, todos em `tests/`.

Log da execução atual: [testes_2026-10-22.txt](../../metadata/ciclo_2026_2027/testes_2026-10-22.txt). Os testes existentes não fornecem contagem padronizada de asserções; por isso o resultado é registrado como nove scripts, e não como nove casos. O teste novo informa seus 14 cenários explicitamente.

Uma tentativa preliminar de reutilizar a fixture do ciclo 2 no preparador atual falhou por ausência de `CO_CNES`; isso foi diagnosticado e permanece em R05. A suíte final usa a fixture histórica do piloto como caso incompatível e casos sintéticos válidos explícitos. Não houve alteração na fixture antiga nem no preparador para mascarar essa falha. Os testes completos `test_base_estabelecimentos_cnes.R` e `test_base_habilitacoes_cnes.R`, fora do CI vigente, não foram executados nesta rodada; a tabela mãe bruta ainda é ponteiro LFS. Os testes Python não foram repetidos porque a trilha experimental não foi alterada.

## Preservação e escopo do diff

Foram comparados hashes obtidos antes e depois do trabalho para **173 arquivos versionados preexistentes e dois anexos originais**. Resultado: 174 arquivos preservados e uma alteração intencional no workflow. As duas cópias dos anexos em `referencias/` também coincidem byte a byte com os originais.

[Manifesto de preservação](../../metadata/ciclo_2026_2027/preservacao_sha256.csv): inclui caminho, categoria, SHA-256 anterior/posterior e estado. O relatório remoto não integra esse manifesto porque não foi obtido; sua preservação nesta tarefa decorre da ausência de qualquer operação de escrita. As consultas de leitura foram recusadas, sem revisão editorial ou recriação do relatório.

O diff preexistente limita-se a `.github/workflows/validar_pipeline_cnes_r.yml`: inclusão do novo teste e dos gatilhos para seu executor. Todas as outras entregas são arquivos novos em `docs/ciclo_2026_2027/`, `metadata/ciclo_2026_2027/` e os três caminhos R descritos no [incremento](primeiro_incremento.md).

Os arquivos de evidência pequenos são versionáveis por sua função de rastreabilidade (convenções de versionamento de metadados); não constituem nova base analítica e não substituem os dados históricos. Os CSVs têm campos documentados no [dicionário das evidências](../../metadata/ciclo_2026_2027/schema_dicionario_evidencias.csv).

## Conclusão técnica delimitada

O incremento foi implementado e verificado. O snapshot **não** foi aprovado, os candidatos substantivos **não** foram validados e a revisão metodológica **não** foi presumida. O próximo passo concreto e suas dependências estão no [registro de continuidade](continuidade_2026-10-22.md).
