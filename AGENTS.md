# AGENTES E RESPONSABILIDADES

Este documento descreve os papéis assumidos por distintos "agentes" (humanos e automatizados) dentro deste repositório e as responsabilidades associadas a cada um. A observância de uma governança clara é essencial para a manutenção de um repositório científico robusto e reprodutível.

## Pesquisador Principal (PI)

* **Definição e Prioridade dos Objetivos**: estabelece as questões de pesquisa, define as métricas e indicadores de interesse em saúde coletiva e orienta a priorização das tarefas. 
* **Supervisão Metodológica**: supervisiona as decisões metodológicas, revisa scripts críticos e valida o rigor científico.
* **Revisão de Contribuições**: aprova pull requests de grande impacto, sobretudo aqueles que alteram significativamente a estrutura de dados, o pipeline analítico ou a interpretação dos resultados.
* **Garantia de Ética e Conformidade**: assegura que as análises sigam princípios éticos e legais, incluindo anonimização de dados sensíveis conforme a LGPD.

## Desenvolvedor de Dados

* **Implementação de Scripts de Extração (src/extract)**: cria funções robustas para coletar dados de fontes primárias ou APIs, documentando parâmetros, formatos de saída e estratégias de atualização.
* **Transformação e Limpeza (src/transform)**: desenvolve rotinas para limpeza de dados, tratamento de valores faltantes, normalização e integração de bases heterogêneas.
* **Geração de Indicadores (src/indicators)**: constrói métricas e indicadores de saúde pública alinhados às melhores práticas epidemiológicas, descrevendo claramente as fórmulas utilizadas.
* **Validação (src/validation)**: escreve testes automatizados e scripts de verificação que checam consistência, completude e plausibilidade dos dados transformados.
* **Documentação**: mantém docstrings completas (vide [docs/convensoes_metodologicas.md](docs/convensoes_metodologicas.md)) e atualiza este manual quando cria componentes novos.

## Analista de Visualização

* **Dashboards**: cria painéis interativos no diretório `dashboards/` utilizando ferramentas como Dash, Shiny ou Plotly, garantindo acessibilidade e clareza.
* **Mapas**: desenvolve mapas no diretório `maps/` que georreferenciem os indicadores, respeitando escalas cartográficas adequadas.
* **Interface com Usuários Finais**: recolhe feedback de utilizadores do SUS, gestores e pesquisadores para aperfeiçoar a representação visual dos dados.

## Curador de Metadados

* **Gerenciamento de `metadata/`**: mantém arquivos com descrições de campos, dicionários de dados e esquemas de bases externas.
* **Padronização de Metadados**: garante que todos os datasets incluam campos obrigatórios (ex.: data de coleta, nível de agregação, unidade de medida).
* **Versionamento**: registra alterações nos dados e nos metadados, comunicando mudanças significativas ao time.

## Testador e Integrador

* **Automatização de Testes**: escreve scripts em `tests/` para verificar funções de extração, transformação e cálculos de indicadores.
* **Integração Contínua**: configura workflows de CI que executem testes a cada commit, integrando com ferramentas como GitHub Actions.
* **Relatórios de Cobertura**: monitora a cobertura de testes e incentiva melhoria contínua.

## Contribuidores Externos

* **Engajamento e Transparência**: devem abrir issues para discutir novas ideias ou problemas detectados antes de submeter pull requests.
* **Conformidade com o Guia**: precisam aderir às convenções de codificação, nomenclatura e documentação descritas neste repositório.
* **Direitos Autorais e Licenças**: garantem que qualquer código ou dado submetido possa ser redistribuído de acordo com a licença do projeto.

## Diretrizes para Mensagens de Commit

Para promover clareza e rastreabilidade, utilize o padrão [Conventional Commits](https://www.conventionalcommits.org/pt-br/v1.0.0/) adaptado ao contexto de saúde pública:

* **Tipos Principais**:
  * `feat`: introdução de nova funcionalidade ou script.
  * `fix`: correções de erros que alteram comportamento.
  * `chore`: tarefas de manutenção (ex.: inclusão de arquivos de configuração, `.gitkeep`).
  * `docs`: mudanças na documentação sem impacto no código executável.
  * `refactor`: reestruturação interna que não altera funcionalidades externas.
  * `test`: adição ou alteração de testes automatizados.
  * `ci`: alterações em pipelines de integração contínua.

* **Formato**: `tipo(escopo opcional): descrição concisa em português no imperativo`

* **Exemplos**:
  * `feat(indicators): implementar cálculo da taxa de mortalidade infantil`
  * `fix(transform): corrigir tratamento de valores ausentes nas idades`
  * `docs: atualizar README com instruções de uso`

Evite mensagens genéricas como “update” ou “final changes” e inclua contexto suficiente para futuras referências.
