# Classificação de Habilitações e Serviços Especializados do CNES

## 1. Finalidade

Esta classificação organiza referências CNES e correlatas relevantes para a análise da oferta especializada no Observatório SUS-ES. A tabela deixou de ser apenas uma lista de “habilitações” e passou a explicitar a natureza de cada referência, distinguindo habilitação, serviço especializado, equipamento, leito, tipo de estabelecimento, componente de rede, procedimento SIGTAP, ocupação CBO, conceito metodológico ou outro item ainda a confirmar.

O objetivo é reduzir ambiguidade antes da automação. A classificação ainda não aplica regras aos dados CNES, não calcula indicadores e não deve ser usada como mapeamento operacional definitivo sem validação normativa posterior.

## 2. Por que distinguir `tipo_referencia_cnes`

Nem todo item relevante para o Observatório é uma habilitação CNES estrita. Alguns elementos necessários para analisar a oferta especializada pertencem a outras dimensões do CNES ou a bases relacionadas. Por exemplo, UTI adulto é melhor tratada como referência de leito/capacidade hospitalar; tomografia computadorizada e mamografia são equipamentos; UPA pode ser tipo de estabelecimento ou componente da rede de urgência; procedimentos endovasculares podem depender de regras SIGTAP; e “componentes habilitados da RUE” é uma categoria metodológica que ainda precisa ser traduzida em códigos e regras específicas.

A coluna `tipo_referencia_cnes` evita que esses itens sejam tratados indevidamente como se todos fossem habilitações. Ela também ajuda a planejar futuras bases tabulares específicas por entidade: habilitações, serviços, equipamentos, leitos, estabelecimentos e componentes de rede.

## 3. Estrutura da tabela

A tabela de referência está no arquivo `metadata/cnes/classificacao_habilitacoes_cnes.csv`. Ela possui as seguintes colunas:

- `id_classificacao`: identificador textual único e estável da linha de classificação, em snake_case.
- `tipo_referencia_cnes`: natureza da referência no CNES ou em base relacionada, com valores controlados.
- `codigo_referencia`: código oficial quando confirmado. Quando não houver confirmação segura, usa `codigo_a_confirmar`; quando o item for conceitual e não tiver código aplicável, usa `nao_aplicavel`.
- `status_codigo`: situação do código informado.
- `descricao_referencia`: descrição textual do item classificado.
- `linha_cuidado`: linha de cuidado principal associada ao item.
- `grupo_tematico`: agrupamento analítico mais amplo.
- `subgrupo`: detalhamento interno da linha de cuidado.
- `tipo_componente`: tipo de componente da rede ou da oferta.
- `prioridade_observatorio`: prioridade analítica inicial para o Observatório SUS-ES, com valores `alta`, `media` ou `baixa`.
- `fonte_referencia`: fonte normativa, técnica ou metodológica usada ou ainda pendente de validação.
- `observacao_metodologica`: ressalvas de interpretação, natureza da referência e limites para uso operacional.

Os valores permitidos para `tipo_referencia_cnes` são: `habilitacao`, `servico_especializado`, `equipamento`, `leito`, `tipo_estabelecimento`, `componente_rede`, `procedimento_sigtap`, `ocupacao_cbo`, `conceito_metodologico` e `outro_a_confirmar`.

## 4. Status do código

A coluna `status_codigo` diferencia a situação do código usado na linha:

- `confirmado`: código oficial validado em fonte normativa ou técnica confiável.
- `a_confirmar`: código ainda não validado; nesses casos, `codigo_referencia` deve permanecer como `codigo_a_confirmar`.
- `nao_aplicavel`: usado quando o item não possui código aplicável na tabela de referência proposta.
- `conceitual`: usado quando a linha representa uma categoria metodológica, como um agrupamento analítico, e não um código CNES estrito.

Nesta versão, os códigos oficiais ainda não foram confirmados. Por isso, referências operacionais permanecem com `codigo_a_confirmar` e itens conceituais usam `nao_aplicavel` quando apropriado.

## 5. Uso previsto

A tabela será usada futuramente para orientar:

- separação entre habilitações, serviços especializados, equipamentos, leitos, tipos de estabelecimento e componentes de rede;
- validação normativa de códigos oficiais;
- criação de função R para aplicar a classificação apenas após validação suficiente;
- geração de bases tabulares específicas por entidade;
- cálculo futuro de indicadores especializados;
- identificação de vazios assistenciais e concentração territorial.

A tabela ainda não deve ser aplicada automaticamente a bases reais sem validação normativa posterior, especialmente nas linhas com `codigo_a_confirmar`, `conceito_metodologico` ou `outro_a_confirmar`.

## 6. Limitações

Esta classificação possui limitações importantes:

- códigos oficiais ainda precisam ser validados;
- itens conceituais não devem ser confundidos com códigos CNES;
- equipamentos, leitos e serviços podem exigir bases CNES diferentes;
- componentes de rede podem depender de portarias, regras assistenciais e tabelas auxiliares;
- a classificação não substitui documentação oficial;
- a classificação serve como primeira camada metodológica de organização da oferta especializada.

A presença de uma referência em determinada linha de cuidado não demonstra funcionamento real, produção, acesso, suficiência ou qualidade. A classificação organiza a leitura estrutural da oferta e deverá ser refinada com documentação oficial do CNES, SIGTAP, manuais técnicos e portarias ministeriais.

## 7. Próximos passos

Os próximos passos recomendados são:

- validar códigos oficiais;
- ampliar linhas de cuidado;
- criar função R para aplicar a classificação;
- gerar base tabular de habilitações;
- criar indicadores de habilitações e serviços especializados;
- cruzar com produção ambulatorial e hospitalar.

A evolução desta classificação deve manter rastreabilidade das alterações, controle de versão da tabela de referência e documentação dos critérios de inclusão, exclusão e agrupamento de códigos.
