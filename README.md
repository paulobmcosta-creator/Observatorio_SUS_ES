# Observatório SUS ES

O **Observatório SUS ES** é uma iniciativa científica e educacional cujo objetivo é monitorar, analisar e divulgar informações sobre a saúde pública no estado do Espírito Santo. A partir de fontes oficiais (SUS, IBGE, ANVISA e outras), desenvolvemos indicadores epidemiológicos, dashboards interativos e mapas temáticos para subsidiar gestores, profissionais de saúde, pesquisadores e a sociedade civil.

Este repositório implementa um _pipeline_ completo de ciência de dados em saúde, desde a coleta de dados brutos até a geração de produtos de visualização. Todas as etapas são documentadas para garantir reprodutibilidade, transparência e aderência às melhores práticas de ciência aberta.

## Estrutura do Projeto
Observatorio_SUS_ES/
├── data_raw/ # Dados brutos coletados de fontes primárias
├── data_interim/ # Dados parcialmente tratados durante a limpeza
├── data_processed/ # Dados finalizados prontos para análise
├── metadata/ # Descrições de campos, dicionários e esquemas de dados
├── src/
│ ├── extract/ # Scripts de extração de dados
│ ├── transform/ # Rotinas de limpeza e padronização
│ ├── indicators/ # Cálculo de métricas epidemiológicas
│ └── validation/ # Scripts de validação e testes de consistência
├── dashboards/ # Códigos e assets de dashboards interativos
├── maps/ # Scripts e arquivos para mapas geoespaciais
├── tests/ # Testes automatizados do pipeline
├── docs/ # Documentação detalhada (governança, metodologia, fluxo)
│ ├── governanca_codigo.md
│ ├── convensoes_metodologicas.md
│ └── fluxo_trabalho.md
├── AGENTS.md # Papéis e responsabilidades dos colaboradores
├── .gitignore # Arquivos e pastas ignorados pelo Git
└── README.md # Este documento

### Principais Componentes

1. **Coleta de Dados (`src/extract`)** – Scripts para baixar ou consultar dados em APIs, portais governamentais e bases institucionais. Os dados são armazenados em `data_raw/` com preservação da estrutura original.
2. **Transformação (`src/transform`)** – Funções para limpeza, normalização e integração de diferentes bases. Resultados intermediários são salvos em `data_interim/`.
3. **Indicadores (`src/indicators`)** – Implementações de indicadores de saúde (incidência, prevalência, letalidade, cobertura vacinal, entre outros) com fórmulas explícitas e referências metodológicas.
4. **Validação (`src/validation`)** – Scripts que verificam a consistência dos dados (checagem de valores extremos, comparações temporais/geográficas) e testes unitários automatizados em `tests/`.
5. **Visualizações (`dashboards/` e `maps/`)** – Códigos para construir painéis interativos e mapas georreferenciados, possibilitando a interpretação dos indicadores por diversos públicos.
6. **Documentação (`docs/`)** – Textos descritivos sobre governaça de código, convenções metodológicas e fluxo de trabalho para que novos colaboradores possam se orientar.

## Linguagem principal e ecossistema

Os pipelines reprodutíveis do Observatório SUS‑ES serão desenvolvidos prioritariamente em **R**. Scripts e funções devem aproveitar o ecossistema tidyverse e demais bibliotecas da linguagem, garantindo transparência, legibilidade e reprodutibilidade. O uso de **Python** é admitido apenas em situações específicas em que exista justificativa técnica (ausência de recurso equivalente em R), devendo ser claramente documentado.

Ferramentas como Power BI e QGIS permanecem no ecossistema do projeto para visualização e georreferenciamento, mas a espinha dorsal analítica reprodutível será elaborada em R. Independente da linguagem, todos os códigos devem seguir as convenções metodológicas e de governança descritas em `docs/`.

## Execução de pipelines em R

Para o piloto CNES em R, consulte:

- guia de setup local: `docs/cnes/setup_execucao_local_r.md`;
- dependências declaradas: `config/dependencias_r.csv`;
- workflow de validação contínua: `.github/workflows/validar_pipeline_cnes_r.yml`.

## Como Contribuir

Contribuições são bem-vindas! Para participar:

1. Consulte o arquivo [AGENTS.md](AGENTS.md) para compreender os papéis e responsabilidades e verifique as [convenções metodológicas](docs/convensoes_metodologicas.md).
2. Abra uma _issue_ descrevendo sua proposta ou relatando um problema. Aguarde a triagem e discussão.
3. Crie um _branch_ a partir de `main` com nome descritivo (ver [governança de código](docs/governanca_codigo.md)).
4. Desenvolva sua funcionalidade seguindo o [fluxo de trabalho](docs/fluxo_trabalho.md), garantindo que seus scripts estejam bem documentados e que novos testes sejam incluídos.
5. Submeta um _pull request_ para revisão. Explique as alterações, referencie a issue relacionada e siga o checklist de revisão.

## Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE). Ao reutilizar ou adaptar conteúdos deste repositório, cite os autores e o repositório conforme normas acadêmicas.

## Contato

Para dúvidas ou sugestões gerais, utilize a área de _Issues_ do GitHub. Para assuntos específicos, entre em contato com o Pesquisador Principal através da instituição responsável.
