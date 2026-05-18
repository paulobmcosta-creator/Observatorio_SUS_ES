# Contrato de Dados — Pipeline Piloto CNES

## 1. Finalidade

Este contrato define os requisitos mínimos de entrada, transformação e saída do pipeline piloto CNES. Seu objetivo é tornar explícitas as premissas técnicas usadas na leitura, padronização, validação e exportação da camada intermediária do módulo CNES no Observatório SUS-ES.

## 2. Escopo do contrato

O contrato se aplica ao piloto técnico baseado em arquivos CSV. Ele ainda não cobre leitura de arquivos DBC, DBF ou integração completa com múltiplos blocos temáticos do CNES. Também não estabelece regras epidemiológicas finais nem substitui validações sanitárias especializadas.

## 3. Entrada esperada

A entrada mínima esperada pelo piloto CNES é:

- diretório padrão: `data_raw/cnes/`;
- formato esperado: `.csv`;
- coluna temporal mínima: `competencia`;
- identificadores administrativos esperados, mas não obrigatórios: `CO_MUNICIPIO_GESTOR` e `CO_CNES`.

A função de leitura adiciona o campo `arquivo_origem` para rastrear o arquivo bruto do qual cada registro foi obtido.

## 4. Padronização de colunas

Os nomes das colunas são convertidos para minúsculas e caracteres não alfanuméricos são substituídos por underscore. Underscores no início ou no fim do nome também são removidos.

Exemplo:

`CO_MUNICIPIO_GESTOR` → `co_municipio_gestor`

## 5. Campos derivados

O pipeline piloto cria ou preserva os seguintes campos técnicos mínimos:

- `competencia_aaaamm`: competência no formato `AAAA-MM`, ou `NA` quando a competência estiver malformada;
- `competencia_data_referencia`: primeiro dia do mês de referência, ou `NA` quando a competência estiver malformada;
- `versao_pipeline`: identificação da versão técnica do pipeline;
- `arquivo_origem`: arquivo bruto de origem.

## 6. Saída esperada

As saídas padrão do pipeline piloto são:

- saída intermediária padrão: `data_interim/cnes/cnes_piloto_interim.csv`;
- log padrão: `data_interim/logs/pipeline_cnes_log.csv`.

Esses caminhos são os padrões da função de orquestração, mas podem ser sobrescritos em testes ou execuções controladas para evitar gravação de artefatos reais no repositório.

## 7. Regras de validação

As validações atualmente implementadas verificam:

- existência de arquivos de entrada compatíveis com o padrão informado;
- existência de dados transformados em objeto `data.frame` não vazio;
- presença de colunas mínimas esperadas após transformação;
- existência do arquivo de saída intermediária.

## 8. Limitações conhecidas

O piloto ainda:

- não lê DBC/DBF;
- não valida regras completas de negócio do CNES;
- não calcula indicadores finais;
- não gera camada `data_processed`;
- não produz dashboards;
- não substitui validação epidemiológica ou sanitária.

## 9. Próximos passos

Os próximos passos técnicos recomendados são:

- expansão para formatos oficiais;
- validações de negócio;
- schema versionado em `metadata/`;
- indicadores derivados;
- integração futura com painéis.
