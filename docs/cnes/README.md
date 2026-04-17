# Módulo CNES — Pipeline Piloto Técnico (R)

## Objetivo

Implementar a primeira rotina técnica controlada para dados CNES no Observatório SUS-ES, com foco em infraestrutura reprodutível (extração, padronização mínima, exportação intermédia, validação inicial e log).

## Entradas

- Diretório padrão: `data_raw/cnes/`
- Formato esperado nesta versão: arquivos `.csv`
- Pré-requisito mínimo: coluna de competência temporal (`competencia`) no arquivo de entrada

## Processamento

1. **Leitura (`src/extract/ler_arquivos_cnes.R`)**
   - Lista arquivos por padrão regex.
   - Lê arquivos CSV e adiciona `arquivo_origem` para rastreabilidade.
2. **Transformação (`src/transform/padronizar_cnes_interim.R`)**
   - Padroniza nomes para minúsculas com underscore.
   - Deriva `competencia_aaaamm` (formato `AAAA-MM`) e `competencia_data_referencia` (primeiro dia do mês).
   - Mantém os identificadores existentes e adiciona `versao_pipeline`.
3. **Validação (`src/validation/validar_pipeline_cnes.R`)**
   - Confere presença de arquivos de entrada.
   - Confere colunas mínimas esperadas no output transformado.
   - Verifica existência do arquivo final exportado.
4. **Orquestração (`src/transform/executar_pipeline_piloto_cnes.R`)**
   - Executa extração → transformação → exportação → validação.
   - Registra log técnico em CSV.

## Saídas

- Saída intermédia principal: `data_interim/cnes/cnes_piloto_interim.csv`
- Log de execução: `data_interim/logs/pipeline_cnes_log.csv`

## Limitações atuais

- Piloto técnico para CSV; não cobre ainda múltiplos formatos CNES (DBC/DBF etc.).
- Não implementa integração completa de múltiplos blocos temáticos CNES.
- Não realiza modelagem analítica final ou indicadores epidemiológicos.
- Não aplica regras avançadas de consistência temporal entre competências.

## Próximos passos recomendados

- Expandir leitor para formatos oficiais adicionais e múltiplas competências.
- Evoluir validações para regras de negócio específicas do CNES.
- Incluir testes automatizados ampliados com cenários reais e casos de borda.
- Definir contrato de dados de entrada (schema versionado em `metadata/`).

## Validação em ambiente com R

- Dependências declaradas em `config/dependencias_r.csv`.
- Script de instalação/preparo: `scripts/instalar_dependencias_r.R`.
- Guia de setup local: `docs/cnes/setup_execucao_local_r.md`.
- Workflow de CI: `.github/workflows/validar_pipeline_cnes_r.yml`.
