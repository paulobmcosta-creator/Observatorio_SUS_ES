# Metadados do Pipeline Piloto CNES

## 1. Finalidade

Os metadados do pipeline piloto CNES documentam a estrutura mínima esperada da camada `data_interim`, produzida após a leitura dos arquivos brutos em CSV e a padronização técnica inicial. Essa camada serve como base auditável para rastrear campos de entrada preservados, campos derivados pelo pipeline e controles mínimos de versão do processamento.

Esta documentação tem caráter técnico e piloto. Ela não define um modelo final do CNES, não cria uma camada analítica definitiva e não representa indicadores de saúde pública prontos para uso em painéis ou análises epidemiológicas.

## 2. Relação com o contrato de dados

O contrato de dados do piloto CNES define as regras gerais de entrada, transformação, validação e saída do pipeline. Ele descreve premissas como formato dos arquivos, campos mínimos, regras de padronização e limitações conhecidas.

O schema YAML e o dicionário CSV complementam esse contrato ao descrever formalmente os campos esperados na saída intermediária. Enquanto o contrato explica o comportamento geral do pipeline, os metadados especificam, campo a campo, tipo esperado, obrigatoriedade, origem, descrição, regra de preenchimento e observações.

## 3. Arquivos de metadados

- `metadata/cnes/schema_cnes_piloto.yml`: schema técnico em YAML com a estrutura mínima da saída intermediária `cnes_piloto_interim`, incluindo versão, camada e descrição dos campos documentados.
- `metadata/cnes/dicionario_cnes_piloto.csv`: dicionário tabular dos mesmos campos, em formato CSV, para leitura simples por pessoas e por rotinas automatizadas de validação.

## 4. Campos documentados

Os campos mínimos documentados são:

- `competencia`: competência original informada no arquivo bruto, usada como referência temporal de entrada.
- `co_municipio_gestor`: identificador administrativo do município gestor, quando disponível no arquivo bruto.
- `co_cnes`: identificador CNES do estabelecimento de saúde, quando disponível no arquivo bruto.
- `arquivo_origem`: nome do arquivo bruto usado como origem do registro, criado pelo pipeline para rastreabilidade.
- `competencia_aaaamm`: competência padronizada no formato `AAAA-MM`, derivada da coluna `competencia`.
- `competencia_data_referencia`: data de referência correspondente ao primeiro dia do mês da competência padronizada.
- `versao_pipeline`: versão técnica fixa do processamento responsável pela transformação.

## 5. Limitações

Este conjunto de metadados ainda não é um schema definitivo do CNES. Ele descreve apenas a estrutura mínima da saída intermediária do piloto técnico em R e não cobre todos os blocos, layouts oficiais, regras de negócio, validações sanitárias ou modelos analíticos possíveis do CNES.

Também não se trata de camada final de indicadores. Os campos documentados apoiam rastreabilidade, auditoria e validação técnica da camada `data_interim`, sem substituir etapas futuras de curadoria, enriquecimento, validação epidemiológica e construção de `data_processed`.

## 6. Próximos passos

- Estabelecer versionamento explícito de schema para mudanças compatíveis e incompatíveis.
- Implementar validação automática da saída intermediária contra o schema documentado.
- Expandir a documentação para outros blocos e layouts CNES.
- Integrar os metadados futuros à camada `data_processed` quando houver produtos analíticos consolidados.
- Utilizar os metadados como referência posterior para indicadores e painéis, sem antecipar essas camadas no piloto técnico atual.
