# Baseline R pré-migração para Python/PySUS

## 1. Objetivo do baseline
Este documento registra o estado técnico-metodológico atual do repositório **antes** de qualquer migração, substituição, refatoração ou descarte da camada operacional em R para Python/PySUS. O foco desta etapa é exclusivamente de **congelamento de referência** (inventário, validação observacional e mapeamento de riscos), sem alterar lógica, dados, metadados ou scripts existentes.

## 2. Identificação do repositório e commit de referência
- **Repositório:** `Observatorio_SUS_ES`
- **Branch atual:** `work`
- **HEAD atual (`git rev-parse HEAD`):** `8e759b17449de9b2d27d6fb48b2a12df6152dfb0`
- **Último commit (`git log -1 --oneline`):** `8e759b1 Merge pull request #42 from paulobmcosta-creator/codex/refactor-cnes-module-pr-without-versioning-intermediate-prod`
- **Data/hora da inspeção (UTC):** 2026-05-24 (execução local nesta sessão; baseline atualizado após instalação efêmera de R para validação)
- **Estado de `git status --short` no início da inspeção:** sem alterações rastreadas no momento do levantamento.
- **Havia arquivos modificados antes da tarefa?** Não foram identificadas modificações rastreadas no snapshot inicial.
- **Observação de escopo:** esta tarefa **não deve alterar** código, dados (`data_raw`, `data_interim`, `data_processed`), metadados (`metadata`) nem configurações existentes.

## 3. Visão geral da arquitetura atual
Estrutura observada (nível macro):

- `data_raw/`
  - `data_raw/cnes/202601/` (insumo CNES por competência)
- `data_interim/`
  - `data_interim/cnes/estabelecimentos/`
  - `data_interim/cnes/habilitacoes/`
- `data_processed/`
- `metadata/`
  - `metadata/cnes/`
- `src/`
  - `src/extract/`
  - `src/transform/`
  - `src/indicators/`
  - `src/validation/`
- `tests/`
  - `tests/fixtures/cnes/`
- `docs/`
  - `docs/cnes/`
- `config/`
- `scripts/`
- `.github/workflows/`

Conclusão arquitetural desta etapa: o repositório mantém uma base **operacional em R** para o módulo CNES, com extração/transformação/validação/indicadores e documentação metodológica associada.

## 4. Scripts R identificados
### 4.1 Scripts-alvo mínimos solicitados

1. **`src/extract/ler_arquivos_cnes.R`**
   - Função aparente: leitura consolidada de CSVs CNES com preservação textual de códigos e rastreabilidade (`arquivo_origem`).
   - Tipo: **extração**.
   - Classificação preliminar: componente operacional substituível (futuro Python), com regra sensível de preservação de identificadores em texto.
   - Regras a preservar: leitura como `character`, união de colunas heterogêneas, erro explícito para diretório/arquivo ausente.

2. **`src/transform/padronizar_cnes_interim.R`**
   - Função aparente: padronização estrutural (nomes de colunas, competência `AAAA-MM`, data de referência, versão do pipeline).
   - Tipo: **transformação**.
   - Classificação preliminar: componente metodológico sensível.
   - Regras a preservar: normalização de nomes, construção de `competencia_aaaamm` e `competencia_data_referencia`, aviso para IDs ausentes.

3. **`src/transform/executar_pipeline_piloto_cnes.R`**
   - Função aparente: orquestração E2E do piloto (extração + transformação + validação + escrita de saída + log).
   - Tipo: **orquestração**.
   - Classificação preliminar: componente piloto e operacional substituível.
   - Regras a preservar: sequência de etapas, logging de execução, validação obrigatória antes de concluir.

4. **`src/transform/preparar_estabelecimentos_cnes.R`**
   - Função aparente: consolida estabelecimentos CNES por UF/competência, com enriquecimentos e classificação conservadora de atendimento SUS.
   - Tipo: **transformação**.
   - Classificação preliminar: componente metodológico sensível.
   - Regras a preservar: uso de `co_unidade` e `cnes`, filtragem territorial ES, tratamento de encoding/sep, detecção de ponteiro LFS, domínios de `atende_sus`.

5. **`src/transform/preparar_habilitacoes_cnes.R`**
   - Função aparente: integra habilitações CNES (RL + domínio + classificação + estabelecimentos), com chave composta de habilitação.
   - Tipo: **transformação/classificação**.
   - Classificação preliminar: componente metodológico sensível.
   - Regras a preservar: join por `co_unidade`; join de classificação por `codigo_habilitacao + tipo_habilitacao`; defaults controlados (`linha_cuidado`, `usar_observatorio`, `status_validacao`).

6. **`src/transform/classificar_habilitacoes_cnes.R`**
   - Função aparente: enriquecimento/classificação por chave composta de habilitação e validações de colunas obrigatórias.
   - Tipo: **classificação**.
   - Classificação preliminar: patrimônio metodológico sensível.
   - Regras a preservar: chave composta obrigatória; consistência dos campos classificatórios.

7. **`src/indicators/calcular_indicadores_cnes_oferta.R`**
   - Função aparente: cálculo de indicadores iniciais de oferta CNES (totais, recortes territoriais e temporais).
   - Tipo: **indicador**.
   - Classificação preliminar: componente metodológico com potencial substituição operacional futura.
   - Regras a preservar: contrato mínimo de colunas de entrada e semântica dos indicadores.

8. **`src/validation/validar_pipeline_cnes.R`**
   - Função aparente: validações estruturais da execução do pipeline (entrada, schema mínimo transformado e saída).
   - Tipo: **validação**.
   - Classificação preliminar: oráculo metodológico temporário.
   - Regras a preservar: falha explícita em ausência de insumo/saída ou colunas mínimas.

### 4.2 Outros scripts R relevantes observados
- `src/transform/auditar_fora_escopo_habilitacoes_cnes.R`
- `src/transform/corrigir_falsos_negativos_habilitacoes_cnes.R`

Foram apenas mapeados no baseline, sem execução de alterações.

## 5. Produtos CNES atualmente documentados ou gerados
### 5.1 Produtos de dados intermediários
1. `data_interim/cnes/estabelecimentos/cnes_estabelecimentos_es_202601.csv`
   - Tipo: dado intermediário gerado.
   - Finalidade: base de estabelecimentos CNES ES (competência 202601).
2. `data_interim/cnes/habilitacoes/cnes_habilitacoes_es_202601.csv`
   - Tipo: dado intermediário gerado.
   - Finalidade: base de habilitações CNES ES enriquecida e classificada.

### 5.2 Metadados CNES
Arquivos observados em `metadata/cnes/` incluem classificação, dicionários, schemas e matrizes de revisão (ex.: `classificacao_habilitacoes_cnes.csv`, `dicionario_*.csv`, `schema_*.csv|yml`, auditorias).

### 5.3 Documentação CNES
Arquivos observados em `docs/cnes/` incluem contrato de dados, decisões metodológicas, produtos tabulares, base de estabelecimentos/habilitações, indicadores, roadmap e setup local.

### 5.4 Estatísticas dos CSVs de estabelecimentos/habilitações

#### a) `cnes_estabelecimentos_es_202601.csv`
- Linhas: **12.548**
- Colunas: **17**
- Colunas: `cnes, competencia, nome_estabelecimento, razao_social, cod_municipio, municipio, uf, tipo_estabelecimento, natureza_juridica, gestao, subtipo_estabelecimento, atendimento_prestado, convenio, atende_sus, fonte, arquivo_origem, data_processamento`
- Municípios distintos (`municipio`): **78**
- `co_unidade` distintos: **não aplicável (coluna ausente nesse produto)**
- `cnes` distintos: **12.548**
- Domínio `atende_sus`: `Não`, `Revisar`, `Sim`
- Domínio `linha_cuidado`: não aplicável
- Domínio `usar_observatorio`: não aplicável
- Vazios em chaves essenciais:
  - `cnes`: **0**

#### b) `cnes_habilitacoes_es_202601.csv`
- Linhas: **1.963**
- Colunas: **31**
- Municípios distintos (`municipio`): **78**
- `co_unidade` distintos: **não aferível neste baseline (coluna não presente no arquivo exportado atual)**
- `cnes` distintos: **1.283**
- `codigo_habilitacao` distintos: **172**
- `tipo_habilitacao` distintos: **7**
- Domínio `atende_sus`: `Não`, `Revisar`, `Sim`
- Domínio `linha_cuidado`: `Cardiovascular`, `Fora do escopo inicial`, `Nefrologia`, `Oncologia`, `Outras habilitações estratégicas`, `RUE`, `Saúde mental`, `UTI / cuidado crítico`
- Domínio `usar_observatorio`: `Não`, `Sim`
- Vazios em chaves essenciais:
  - `cnes`: **0**
  - `codigo_habilitacao`: **0**
  - `tipo_habilitacao`: **0**

## 6. Regras metodológicas já consolidadas
Regras identificadas no código/documentação e que devem ser preservadas durante migração:

- `co_unidade` deve ser tratado como **chave operacional** do estabelecimento CNES.
- `cnes` deve ser tratado como **código público**.
- Joins relacionais CNES devem usar `co_unidade` quando aplicável.
- Habilitações devem usar chave composta `codigo_habilitacao + tipo_habilitacao`.
- Habilitações devem integrar com estabelecimentos por `co_unidade`.
- `atende_sus` é classificação conservadora, **não** indicador final.
- `data_interim` é produto gerável/reconstruível, não fonte permanente de verdade.
- `metadata/cnes/classificacao_habilitacoes_cnes.csv` é patrimônio metodológico e deve ser preservado.

## 7. Testes existentes
Testes R mapeados em `tests/`:

1. `tests/test_estrutura_repositorio.R`
   - Objetivo aparente: sanidade de estrutura de pastas/artefatos esperados.
   - Dependência: estrutura local do repo.
   - Oráculo R vs Python: **sim** (baseline estrutural).

2. `tests/test_metadata_cnes.R`
   - Objetivo aparente: validações de metadados/classificação CNES.
   - Dependência: arquivos em `metadata/cnes`.
   - Oráculo R vs Python: **sim**.

3. `tests/test_classificacao_habilitacoes_cnes.R`
   - Objetivo aparente: consistência da classificação e função classificadora.
   - Dependência: metadata real + função R.
   - Oráculo R vs Python: **sim (alto valor)**.

4. `tests/test_ler_arquivos_cnes.R`
   - Objetivo aparente: unitário de leitura e robustez de extração.
   - Dependência: fixtures (`tests/fixtures/cnes`) e temporários.
   - Oráculo R vs Python: **sim**.

5. `tests/test_padronizar_cnes_interim.R`
   - Objetivo aparente: padronização de colunas/competência/IDs e warnings.
   - Dependência: fixtures e função R.
   - Oráculo R vs Python: **sim**.

6. `tests/test_validar_pipeline_cnes.R`
   - Objetivo aparente: validações contratuais do pipeline.
   - Dependência: fixtures + temporários.
   - Oráculo R vs Python: **sim**.

7. `tests/test_executar_pipeline_piloto_cnes.R`
   - Objetivo aparente: orquestração do pipeline piloto e logging.
   - Dependência: fixture + escrita em `tempdir()`.
   - Oráculo R vs Python: **sim**.

8. `tests/teste_pipeline_piloto_cnes.R`
   - Objetivo aparente: teste mínimo de integração pipeline piloto.
   - Dependência: fixture + temporários.
   - Oráculo R vs Python: **sim**.

9. `tests/test_indicadores_cnes_oferta.R`
   - Objetivo aparente: indicadores de oferta com dados sintéticos.
   - Dependência: apenas base R e função de indicadores.
   - Oráculo R vs Python: **sim (determinístico)**.

10. `tests/test_base_estabelecimentos_cnes.R`
    - Objetivo aparente: valida base real de estabelecimentos ES 202601.
    - Dependência: `data_raw/cnes/202601` real + escrita temporária.
    - Oráculo R vs Python: **sim (comparação funcional)**.

11. `tests/test_base_habilitacoes_cnes.R`
    - Objetivo aparente: valida preparação real de habilitações integrada com estabelecimentos.
    - Dependência: `data_raw/cnes/202601` + `metadata/cnes` + escrita temporária.
    - Oráculo R vs Python: **sim (comparação funcional)**.

## 8. Execução de testes nesta etapa
### 8.1 Verificação de runtime R (antes da instalação)
Comandos executados:
- `which R || true`
- `which Rscript || true`
- `R --version || true`
- `Rscript --version || true`

Resultado inicial:
- `R` **não encontrado**.
- `Rscript` **não encontrado**.

### 8.2 Instalação efêmera de R no ambiente da sessão
Conforme instrução operacional desta etapa, foi tentada instalação no ambiente temporário (sem alterar arquivos do repositório):

- `apt-get update`
- `apt-get install -y r-base r-base-dev`

Após a instalação:
- `which R` -> `/usr/bin/R`
- `which Rscript` -> `/usr/bin/Rscript`
- `R --version` -> `R version 4.3.3 (2024-02-29)`
- `Rscript --version` -> `Rscript (R) version 4.3.3 (2024-02-29)`
- `Rscript -e 'sessionInfo()'` executado com sucesso.

### 8.3 Execução dos testes R solicitados
Testes executados com `Rscript`:

- ✅ `tests/test_estrutura_repositorio.R` (passou)
- ✅ `tests/test_metadata_cnes.R` (passou)
- ✅ `tests/test_classificacao_habilitacoes_cnes.R` (passou)
- ✅ `tests/test_ler_arquivos_cnes.R` (passou)
- ✅ `tests/test_padronizar_cnes_interim.R` (passou)
- ✅ `tests/test_validar_pipeline_cnes.R` (passou)
- ✅ `tests/test_executar_pipeline_piloto_cnes.R` (passou)
- ✅ `tests/teste_pipeline_piloto_cnes.R` (passou)
- ✅ `tests/test_indicadores_cnes_oferta.R` (passou)
- ❌ `tests/test_base_estabelecimentos_cnes.R` (falhou)
- ❌ `tests/test_base_habilitacoes_cnes.R` (falhou)

Resumo das falhas:
- Ambos os testes de base real falharam com erro: `Arquivo tbEstabelecimento202601.csv é ponteiro Git LFS sem conteúdo tabular real.`
- Classificação da causa provável: **dados/Git LFS** (conteúdo bruto necessário não materializado localmente), não evidência direta de regressão lógica dos scripts.


### 8.4 Complementação da Etapa 0: tentativa de materialização Git LFS (após falha nos testes de base real)

Ações executadas no ambiente efêmero:

- `git lfs version || true`
- `apt-get update`
- `apt-get install -y git-lfs`
- `git lfs install`
- `git lfs pull --include="data_raw/cnes/202601/tbEstabelecimento202601.csv"`
- `head -n 5 data_raw/cnes/202601/tbEstabelecimento202601.csv`
- `wc -c data_raw/cnes/202601/tbEstabelecimento202601.csv`
- `Rscript tests/test_base_estabelecimentos_cnes.R`
- `Rscript tests/test_base_habilitacoes_cnes.R`

Resultados observados:

- `git-lfs` já estava disponível (`git-lfs/3.4.1`).
- Não foi necessária instalação adicional de `git-lfs` (pacote já na versão mais recente).
- `git lfs install` executou com sucesso.
- `git lfs pull` **não materializou** o arquivo e retornou erro: `batch request: missing protocol: ""` e `Failed to fetch some objects from ''`.
- Verificação do arquivo bruto após pull:
  - `head -n 5` continuou exibindo conteúdo de ponteiro LFS (`version https://git-lfs.github.com/spec/v1`, `oid sha256:...`, `size 284224999`).
  - `wc -c` retornou **134 bytes**, confirmando que o arquivo permaneceu como ponteiro, sem conteúdo tabular real local.

Reexecução dos dois testes que haviam falhado:

- ❌ `tests/test_base_estabelecimentos_cnes.R`
  - Erro resumido: `Arquivo tbEstabelecimento202601.csv é ponteiro Git LFS sem conteúdo tabular real.`
- ❌ `tests/test_base_habilitacoes_cnes.R`
  - Erro resumido: `Arquivo tbEstabelecimento202601.csv é ponteiro Git LFS sem conteúdo tabular real.`

Conclusão da complementação:

- A limitação de Git LFS **persistiu** nesta sessão.
- Os dois testes de base real foram reexecutados, mas continuam bloqueados por indisponibilidade do conteúdo LFS do arquivo bruto necessário.

## 9. Estado de versionamento de dados
### 9.1 `.gitignore`
Política observada:
- Ignora majoritariamente `data_interim/*` e `data_processed/*`.
- Exceções explícitas para:
  - `data_interim/.gitkeep`
  - `data_interim/cnes/`
  - `data_interim/cnes/estabelecimentos/`
  - `data_interim/cnes/estabelecimentos/cnes_estabelecimentos_es_202601.csv`

Leitura preliminar:
- Há versionamento seletivo de produto interim específico (estabelecimentos 202601), com potencial fragilidade para expansão de competências/coberturas.

### 9.2 `.gitattributes` e Git LFS
Entrada observada:
- `data_raw/cnes/202601/tbEstabelecimento202601.csv filter=lfs diff=lfs merge=lfs -text`

Leitura preliminar:
- Pelo menos um insumo crítico está em **Git LFS**.
- Risco operacional: ambiente sem fetch completo de LFS pode impedir reprodução de transformações.

### 9.3 Suficiência para futura camada Python/PySUS
- A política atual é funcional para o estado piloto, porém **potencialmente frágil** para escalabilidade multi-competência e dupla operação R/Python (risco de inconsistência entre dados geráveis e dados versionados seletivamente).

## 10. Baseline de cardinalidades e integridade

| produto | caminho | linhas | colunas | chaves principais | cardinalidade de chaves | domínios relevantes | observações | status do baseline |
|---|---|---:|---:|---|---|---|---|---|
| Estabelecimentos ES 202601 | `data_interim/cnes/estabelecimentos/cnes_estabelecimentos_es_202601.csv` | 12.548 | 17 | `cnes` (pública) | `cnes` distintos: 12.548 | `atende_sus` = {Sim, Não, Revisar} | sem vazios em `cnes`; `co_unidade` não presente no export atual | capturado |
| Habilitações ES 202601 | `data_interim/cnes/habilitacoes/cnes_habilitacoes_es_202601.csv` | 1.963 | 31 | `cnes` + (`codigo_habilitacao`,`tipo_habilitacao`) | `cnes`: 1.283; `codigo_habilitacao`: 172; `tipo_habilitacao`: 7 | `atende_sus` = {Sim, Não, Revisar}; `usar_observatorio` = {Sim, Não}; 8 valores em `linha_cuidado` | sem vazios em `cnes`, `codigo_habilitacao`, `tipo_habilitacao`; `co_unidade` não presente no export atual | capturado |
| Classificação de habilitações | `metadata/cnes/classificacao_habilitacoes_cnes.csv` | não aferido nesta etapa | não aferido nesta etapa | `codigo_habilitacao` + `tipo_habilitacao` | não aferido nesta etapa | campos metodológicos de classificação | patrimônio metodológico explícito | mapeado |
| Documentação metodológica CNES | `docs/cnes/` | n/a | n/a | n/a | n/a | n/a | múltiplos documentos de contrato/decisão/produto | mapeado |

Produtos esperados não encontrados: **não identificado** no escopo inspecionado (pastas alvo existem e possuem artefatos).

## 11. Componentes candidatos a descarte futuro
Classificação preliminar (sem mover/alterar):

- **Preservar como patrimônio metodológico**
  - `metadata/cnes/classificacao_habilitacoes_cnes.csv`
  - documentação metodológica em `docs/cnes/*`
  - regras de chave/joins embutidas em transformações CNES

- **Preservar como oráculo temporário**
  - suíte `tests/*.R` relevante para CNES
  - `src/validation/validar_pipeline_cnes.R`
  - funções de classificação/indicadores para comparação de paridade

- **Substituir futuramente por Python/PySUS**
  - camada de extração e leitura em `src/extract/*`
  - orquestração piloto `src/transform/executar_pipeline_piloto_cnes.R`

- **Avaliar caso a caso**
  - transformações com forte regra de negócio (`preparar_estabelecimentos_*`, `preparar_habilitacoes_*`)
  - indicadores (manter semântica, permitir nova implementação)

- **Arquivar/deprecar futuramente**
  - scripts estritamente transitórios de piloto, após validação de paridade R vs Python e aceite formal.

## 12. Riscos identificados antes da migração
1. Dependência de `Rscript` para execução local e CI de testes legados.
2. Dependência de dados reais em `data_raw/cnes/202601` para testes de base real.
3. Risco de Git LFS incompleto (insumos críticos como `tbEstabelecimento202601.csv`).
4. Potencial duplicação de utilitários (ex.: normalização de nomes) em múltiplos scripts.
5. Hardcoding de competência `202601` em scripts/testes/produtos.
6. Acoplamento entre transformação e escrita de arquivos em parte dos scripts.
7. Fragilidade de encoding e delimitador (UTF-8/Latin1, `;`/`,`), mitigada parcialmente no legado R.
8. Risco de divergência entre documentação e código efetivamente executado.
9. Risco de cobertura incompleta em PySUS para todas as tabelas CNES atualmente usadas.

## 13. Critérios de aceite para avançar à Etapa 1
Checklist objetivo da Etapa 0:

- [x] Documento de baseline criado em `docs/migracao_python/00_baseline_r_pre_migracao.md`.
- [x] Branch e commit de referência registrados.
- [x] Scripts R mapeados e classificados preliminarmente.
- [x] Produtos CNES mapeados (dados, metadados e documentação).
- [x] Testes existentes mapeados.
- [x] Execução de testes registrada **ou** limitação de ambiente documentada (nesta inspeção: limitação documentada).
- [x] Regras metodológicas centrais registradas.
- [x] Componentes candidatos a descarte classificados preliminarmente.
- [x] Nenhum código, dado ou metadado existente alterado nesta etapa.

## 14. Conclusão
Este baseline deve ser tratado como referência obrigatória antes de:

1. classificar formalmente o legado R;
2. criar ambiente Python;
3. testar integração PySUS;
4. comparar saídas R versus Python;
5. deprecar qualquer script R.

A Etapa 0 encerra-se com foco em rastreabilidade e proteção metodológica do estado atual, sem iniciar Etapa 1 e sem alterar ativos existentes fora deste documento.
