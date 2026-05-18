# Módulo CNES — Pipeline Piloto Técnico (R)

## Objetivo

Implementar a primeira rotina técnica controlada para dados CNES no Observatório SUS-ES, com foco em infraestrutura reprodutível: extração, padronização mínima, exportação intermediária, validação inicial e log.

Este módulo ainda é um piloto técnico. Ele não cria dashboards, não calcula indicadores finais e não substitui validação epidemiológica ou sanitária especializada.

## Contrato de dados

O contrato mínimo de entrada, transformação e saída do piloto está documentado em [`docs/cnes/contrato_dados_cnes_piloto.md`](contrato_dados_cnes_piloto.md). Esse documento explicita o formato esperado dos arquivos CSV, os campos mínimos, os campos derivados, as regras de validação e as limitações conhecidas.

## Entradas

- Diretório padrão: `data_raw/cnes/`
- Formato esperado nesta versão: arquivos `.csv`
- Pré-requisito mínimo: coluna de competência temporal (`competencia`) no arquivo de entrada
- Identificadores administrativos esperados, mas não obrigatórios: `CO_MUNICIPIO_GESTOR` e `CO_CNES`

## Scripts existentes

1. **Leitura — `src/extract/ler_arquivos_cnes.R`**
   - Lista arquivos por padrão regex.
   - Lê arquivos CSV.
   - Consolida um ou mais arquivos compatíveis.
   - Adiciona `arquivo_origem` para rastreabilidade.

2. **Transformação — `src/transform/padronizar_cnes_interim.R`**
   - Padroniza nomes para minúsculas com underscore.
   - Deriva `competencia_aaaamm` no formato `AAAA-MM`, usando `NA` para competências malformadas.
   - Deriva `competencia_data_referencia` como o primeiro dia do mês de referência, usando `NA` para competências malformadas.
   - Preserva identificadores existentes, como `co_municipio_gestor` e `co_cnes`.
   - Adiciona `versao_pipeline`.
   - Emite aviso quando nenhum identificador administrativo esperado está presente.

3. **Validação — `src/validation/validar_pipeline_cnes.R`**
   - Confere presença de arquivos de entrada.
   - Confere se os dados transformados são um `data.frame` não vazio.
   - Confere colunas mínimas esperadas no output transformado.
   - Verifica existência do arquivo final exportado.

4. **Orquestração — `src/transform/executar_pipeline_piloto_cnes.R`**
   - Executa extração → transformação → exportação → validação.
   - Registra log técnico em CSV.
   - Retorna lista com `arquivo_saida`, `arquivo_log` e `linhas_exportadas`.

## Saídas

- Saída intermediária principal: `data_interim/cnes/cnes_piloto_interim.csv`
- Log de execução: `data_interim/logs/pipeline_cnes_log.csv`

Em testes, os caminhos de saída e log devem apontar para diretórios temporários para evitar versionamento de artefatos gerados.


## Metadados

A camada inicial de metadados do piloto CNES formaliza a estrutura mínima esperada para a saída intermediária `data_interim` e apoia auditoria, rastreabilidade e testes automatizados. Os arquivos principais são:

- `metadata/cnes/schema_cnes_piloto.yml`: schema YAML versionado do piloto técnico, com tipo esperado, obrigatoriedade, origem, descrição, regra de preenchimento e observações de cada campo mínimo.
- `metadata/cnes/dicionario_cnes_piloto.csv`: dicionário CSV coerente com o schema, adequado para leitura tabular e verificações simples.
- `docs/cnes/metadados_cnes_piloto.md`: documentação técnica dos metadados, sua relação com o contrato de dados, limitações e próximos passos.
- `tests/test_metadata_cnes.R`: teste em R base que valida existência dos arquivos, colunas do dicionário, campos mínimos documentados, duplicidades e presença dos campos no schema YAML.

## Fixtures sintéticas

As fixtures do módulo ficam em `tests/fixtures/cnes/` e não contêm dados pessoais ou sensíveis.

- `cnes_piloto_exemplo.csv`: fixture básica do teste de integração do pipeline piloto.
- `cnes_multiplos_registros.csv`: fixture válida com três registros e identificadores administrativos.
- `cnes_sem_competencia.csv`: fixture inválida sem a coluna temporal mínima.
- `cnes_competencia_malformada.csv`: fixture com competências sintéticas malformadas.
- `cnes_sem_identificadores.csv`: fixture válida quanto à competência, mas sem identificadores administrativos esperados.

## Testes existentes

Os testes são scripts R simples executáveis via `Rscript`, sem dependências externas de frameworks de teste.

- `tests/test_estrutura_repositorio.R`: valida a estrutura mínima do repositório.
- `tests/test_ler_arquivos_cnes.R`: testa leitura de CSV, coluna `arquivo_origem`, consolidação de múltiplos arquivos e falhas esperadas de entrada.
- `tests/test_padronizar_cnes_interim.R`: testa padronização de colunas, campos derivados, preservação de identificadores, versão do pipeline, erro sem competência, competência malformada e aviso sem identificadores.
- `tests/test_validar_pipeline_cnes.R`: testa validação bem-sucedida e falhas para ausência de entrada, objeto transformado inválido, dados vazios, colunas ausentes e saída inexistente.
- `tests/test_executar_pipeline_piloto_cnes.R`: testa a execução completa em diretório temporário, criação de saída e log, retorno esperado e reexecução com append de log.
- `tests/teste_pipeline_piloto_cnes.R`: teste de integração do pipeline completo usando fixture sintética.

## Execução local

Antes de executar os testes, confirme que o runtime R está instalado e que `Rscript` está disponível no `PATH`:

```bash
which R
which Rscript
R --version
Rscript --version
Rscript -e 'sessionInfo()'
```

Se o terminal retornar `Rscript: command not found`, instale o R ou ajuste o `PATH`. Orientações mais detalhadas estão em [`docs/cnes/setup_execucao_local_r.md`](setup_execucao_local_r.md).

A partir da raiz do repositório, execute:

```bash
Rscript scripts/instalar_dependencias_r.R
Rscript tests/test_estrutura_repositorio.R
Rscript tests/test_metadata_cnes.R
Rscript tests/test_ler_arquivos_cnes.R
Rscript tests/test_padronizar_cnes_interim.R
Rscript tests/test_validar_pipeline_cnes.R
Rscript tests/test_executar_pipeline_piloto_cnes.R
Rscript tests/teste_pipeline_piloto_cnes.R
```

Também é possível executar o pipeline piloto diretamente, desde que existam arquivos CSV válidos no diretório de entrada configurado:

```bash
Rscript src/transform/executar_pipeline_piloto_cnes.R
```

## Validação em CI

O workflow `.github/workflows/validar_pipeline_cnes_r.yml` configura explicitamente o R com `r-lib/actions/setup-r@v2` antes de qualquer comando `Rscript`. O job também verifica `R`, `Rscript`, suas versões e `sessionInfo()` antes de instalar/preparar as dependências declaradas em `config/dependencias_r.csv` e executar os testes de estrutura, unitários e de integração do módulo CNES.

## Limitações atuais

- Piloto técnico para CSV; não cobre ainda múltiplos formatos CNES, como DBC ou DBF.
- Não implementa integração completa de múltiplos blocos temáticos CNES.
- Não realiza modelagem analítica final ou indicadores epidemiológicos.
- Não gera camada `data_processed`.
- Não produz dashboards.
- Não aplica regras completas de consistência temporal, territorial ou sanitária entre competências.

## Próximos passos recomendados

- Expandir leitor para formatos oficiais adicionais e múltiplas competências.
- Evoluir validações para regras de negócio específicas do CNES.
- Definir schema versionado em `metadata/`.
- Implementar indicadores derivados em etapa futura, após validação metodológica.
- Integrar futuramente resultados validados a painéis, sem antecipar dashboards neste piloto técnico.
