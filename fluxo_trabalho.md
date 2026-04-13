# Fluxo de Trabalho no Observatório SUS ES

Este documento descreve o fluxo de trabalho recomendável para o desenvolvimento de análises e produtos dentro deste repositório. O objetivo é assegurar que todas as etapas – da coleta de dados à divulgação – sejam rastreáveis, reprodutíveis e alinhadas com princípios científicos.

## 1. Planejamento e Definição do Problema

1. **Identificação da Questão de Pesquisa**: o Pesquisador Principal e demais envolvidos definem a pergunta de interesse e os indicadores necessários.
2. **Mapeamento de Fontes de Dados**: listar bases disponíveis (SUS, IBGE, etc.), identificando níveis geográficos, periodicidade e restrições de acesso.
3. **Criação de Issue**: abrir uma issue no GitHub detalhando o problema, fontes e abordagem inicial. Todas as discussões subsequentes devem ocorrer nesta issue.

## 2. Coleta e Extração de Dados

1. **Criação de Branch de Funcionalidade**: criar um branch com nome descritivo (ex.: `feature/extrair-casos-dengue`).
2. **Implementação de Scripts**: escrever scripts em `src/extract/` para baixar ou acessar APIs. Salvar resultados em `data_raw/` e documentar formatos obtidos.
3. **Documentação**: atualizar metadados em `metadata/` indicando origem, data de coleta e estrutura dos arquivos.

## 3. Transformação e Limpeza

1. **Criação de Scripts**: em `src/transform/`, desenvolver rotinas para limpeza de dados, padronização de nomes, unidades e codificação de variáveis.
2. **Dados Intermediários**: armazenar resultados temporários em `data_interim/` para permitir rastreabilidade das etapas.
3. **Validação Inicial**: utilizar scripts em `src/validation/` para conferir se há inconsistências, outliers ou erros de digitização.

## 4. Construção de Indicadores

1. **Definição de Fórmulas**: documentar claramente a fórmula e a justificativa epidemiológica de cada indicador.
2. **Implementação**: codificar funções em `src/indicators/` que recebam dados processados e retornem indicadores. Garantir modularidade para facilitar reuso.
3. **Armazenamento**: salvar datasets de indicadores em `data_processed/` com nomenclatura informativa.
4. **Testes**: criar casos de teste em `tests/` para garantir que o cálculo esteja correto em diferentes cenários.

## 5. Validação Avançada

1. **Consistência Temporal e Geográfica**: verificar se tendências observadas são plausíveis e se não existem valores abruptos que indiquem erro.
2. **Comparação com Referências**: confrontar resultados com relatórios oficiais ou literatura científica.
3. **Revisão por Pares**: solicitar revisão metodológica a outros especialistas para detectar possíveis falhas.

## 6. Visualização e Divulgação

1. **Dashboards**: desenvolver painéis interativos em `dashboards/` que apresentem indicadores de forma intuitiva.
2. **Mapas**: criar mapas em `maps/` para ilustrar a distribuição espacial de indicadores.
3. **Relatórios**: publicar relatórios em Markdown ou HTML com narrativa interpretativa, discussões e implicações para políticas públicas.

## 7. Integração e Publicação

1. **Revisão Final**: abrir um Pull Request para integrar o branch de trabalho à `main`. Acompanhar o checklist de governança de código.
2. **Merge**: após aprovação, realizar merge via *squash*, etiquetar a issue correspondente como fechada e atualizar o changelog se houver.
3. **Divulgação Externa**: disponibilizar dashboards e mapas em portais apropriados (ex.: site da instituição) e comunicar os resultados aos stakeholders.

## 8. Manutenção e Atualizações

1. **Monitoramento**: verificar periodicamente se as bases de dados foram atualizadas; agendar reexecução dos scripts conforme a periodicidade (mensal, trimestral, anual).
2. **Refatoração**: otimizar código legados e adaptar o pipeline quando surgirem novas fontes ou mudanças nos formatos existentes.
3. **Feedback Continuado**: coletar sugestões de usuários finais para melhorar usabilidade das visualizações e pertinência dos indicadores.

Seguindo este fluxo estruturado, o Observatório SUS ES mantém a integridade científica e a eficiência operacional em suas análises e produtos.

