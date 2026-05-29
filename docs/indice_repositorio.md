# Índice do repositório — Observatório SUS-ES

Este documento é o índice geral do repositório após a limpeza documental. Ele orienta a navegação inicial, separando entrada pedagógica, núcleo metodológico, histórico arquivado, áreas experimentais e áreas restritas.

## 1. Entrada para aluno

- `docs/guias_aluno/README.md`: ponto de partida pedagógico.
- `docs/guias_aluno/guia_inicio_observatorio_sus.md`: introdução ao projeto e às regras de segurança.
- `docs/guias_aluno/mapa_repositorio_observatorio_sus.md`: mapa dos diretórios e permissões de alteração.
- `docs/guias_aluno/glossario_minimo_cnes_observatorio.md`: termos essenciais para leitura inicial.
- `docs/guias_aluno/plano_trabalho_aluno_cnes.md`: plano de quatro semanas para ambientação.

## 2. Documentação metodológica

- `docs/convensoes_metodologicas.md`: convenções de documentação e método.
- `docs/convensoes_versionamento_dados.md`: diretrizes de versionamento de dados.
- `docs/fluxo_trabalho.md`: fluxo de trabalho do projeto.
- `docs/governanca_codigo.md`: governança de código.
- `docs/matriz_manutencao.md`: matriz de manutenção.
- `docs/revisao_geral_entrega_aluno.md`: auditoria da Revisão Geral 01 e nota da limpeza documental posterior.

## 3. Documentação CNES

- `docs/cnes/README.md`: entrada para a documentação CNES.
- `docs/cnes/`: documentação consolidada sobre bases, indicadores, metadados, decisões e produtos tabulares CNES.

A leitura de documentos CNES deve ser orientada pelo pesquisador, especialmente quando envolver contratos, chaves e campos sensíveis.

## 4. Metadados

- `metadata/`: dicionários, schemas, contratos e matrizes de revisão.
- `metadata/cnes/`: metadados específicos do CNES.

Metadados existentes não devem ser alterados por aluno sem autorização, porque sustentam rastreabilidade e validação.

## 5. Legado R/oráculo

- `src/`: código-fonte do pipeline, com destaque para componentes R do piloto CNES.
- `scripts/`: scripts auxiliares e técnicos.

R permanece oráculo metodológico. Scripts não devem ser executados ou modificados sem orientação.

## 6. Python/PySUS experimental

- `python/`: componentes Python/PySUS experimentais.
- `docs/migracao_python/README.md`: status consolidado da migração.

Python/PySUS permanece experimental/prototípico e não substitui o pipeline R. A geração de base por essa trilha não está autorizada.

## 7. Arquivo histórico

- `docs/arquivo_historico/README.md`: regra geral de uso do arquivo histórico.
- `docs/arquivo_historico/migracao_python/`: histórico completo da migração R–Python/PySUS.

O arquivo histórico preserva rastreabilidade, mas não é material inicial de orientação do aluno.

## 8. Áreas restritas

- `data_raw/`: dados brutos.
- `data_interim/`: dados intermediários.
- `data_processed/`: dados processados.
- `tests/`: testes automatizados e fixtures.
- `config/`: configurações e dependências.
- `.github/workflows/`: integração contínua.

Essas áreas não são livres para escrita ou alteração pelo aluno.

## 9. O que não executar sem autorização

- Scripts R.
- Scripts Python/PySUS.
- Testes automatizados.
- Pipelines de extração, transformação ou indicadores.
- Downloads de dados.
- Geração de bases em `data_raw/`, `data_interim/` ou `data_processed/`.
- Rotinas que tentem resolver ou modificar `CO_UNIDADE`.
- Qualquer tentativa de substituir R por Python sem validação de paridade e decisão metodológica.
