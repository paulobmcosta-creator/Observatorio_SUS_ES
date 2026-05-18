# Classificação de Habilitações e Serviços Especializados do CNES

## 1. Finalidade

Esta classificação organiza habilitações e serviços especializados do CNES por linha de cuidado para apoiar a análise da oferta especializada no Observatório SUS-ES. A tabela de referência tem função metodológica: criar uma primeira ponte entre descrições de habilitações ou serviços e categorias analíticas usadas pelo Observatório, como oncologia, cardiologia, Rede de Urgência e Emergência, UTI e cuidado crítico, diagnóstico e apoio terapêutico, terapia renal substitutiva e reabilitação.

A classificação ainda não aplica regras aos dados CNES e não calcula indicadores. Ela prepara uma base de referência que poderá ser utilizada em ciclos futuros para gerar bases tabulares de habilitações e serviços especializados, produzir indicadores de oferta especializada e apoiar análises de vazios assistenciais e concentração territorial.

## 2. Relação com a visão analítica do CNES

A classificação deriva da visão do CNES como base da oferta instalada, habilitada e potencialmente disponível ao SUS. Nesse sentido, ela deve ser lida como instrumento para qualificar a estrutura formal da rede, e não como prova de funcionamento real, acesso efetivo, produção assistencial ou qualidade do cuidado.

Esta classificação se relaciona conceitualmente com:

- `docs/cnes/visao_analitica_cnes_observatorio.md`;
- `docs/cnes/produtos_tabulares_cnes.md`;
- `docs/cnes/familias_indicadores_cnes.md`;
- `docs/cnes/roadmap_tecnico_cnes.md`.

A visão analítica define o papel do CNES como camada estrutural. O documento de produtos tabulares define a base de habilitações e serviços especializados como produto futuro. O documento de famílias de indicadores organiza os usos analíticos esperados. O roadmap técnico recomenda esta classificação como próximo ciclo, antes da implementação da função R que aplicará a classificação às bases CNES.

## 3. Escopo da classificação

Esta primeira versão contempla as seguintes linhas de cuidado:

- oncologia;
- cardiologia;
- Rede de Urgência e Emergência;
- UTI e cuidado crítico;
- diagnóstico e apoio terapêutico;
- terapia renal substitutiva;
- reabilitação.

O escopo inicial foi definido por sua relevância para a atenção especializada, capacidade hospitalar, resposta à urgência e emergência, apoio diagnóstico e continuidade do cuidado. Outras linhas poderão ser incluídas em versões futuras, desde que sejam acompanhadas de documentação metodológica e validação dos códigos oficiais.

## 4. Estrutura da tabela de classificação

A tabela de referência está no arquivo `metadata/cnes/classificacao_habilitacoes_cnes.csv`. Ela possui as seguintes colunas:

- `codigo_habilitacao`: código da habilitação ou serviço especializado quando conhecido. Quando o código oficial ainda não foi confirmado, utiliza-se `codigo_a_confirmar`.
- `descricao_habilitacao`: descrição textual da habilitação ou serviço.
- `linha_cuidado`: linha de cuidado principal associada ao registro.
- `grupo_tematico`: agrupamento analítico mais amplo, como atenção especializada, urgência e emergência, capacidade hospitalar, apoio diagnóstico e terapêutico ou cuidado continuado e reabilitação.
- `subgrupo`: detalhamento interno da linha de cuidado.
- `tipo_componente`: tipo de componente da rede ou da oferta, como habilitação, serviço especializado, componente de rede, equipamento/serviço ou leito de cuidado crítico.
- `prioridade_observatorio`: prioridade analítica inicial para o Observatório SUS-ES, com valores `alta`, `media` ou `baixa`.
- `fonte_referencia`: referência normativa ou metodológica utilizada ou a ser validada.
- `observacao_metodologica`: ressalvas sobre uso, confirmação de códigos e interpretação.

A coluna `codigo_habilitacao` usa `codigo_a_confirmar` nesta primeira versão quando não há segurança suficiente sobre o código oficial. Essa escolha evita inventar códigos e explicita a necessidade de refinamento futuro com documentação oficial do CNES, SIGTAP e portarias ministeriais.

## 5. Uso previsto

A tabela será usada futuramente para:

- classificar habilitações CNES por linha de cuidado;
- gerar base tabular de habilitações e serviços especializados;
- calcular indicadores de oferta especializada;
- identificar vazios assistenciais;
- analisar concentração territorial;
- cruzar oferta habilitada com produção SIH/SUS e SIA/SUS.

O uso operacional dependerá de uma função R futura, que deverá aplicar a classificação de forma reprodutível, preservar códigos e descrições originais, registrar a versão da tabela de referência utilizada e produzir testes automatizados.

## 6. Limitações

Esta tabela possui limitações importantes:

- é uma primeira versão metodológica;
- alguns códigos oficiais estão marcados como `codigo_a_confirmar`;
- habilitação formal não garante funcionamento real;
- habilitação formal não garante produção;
- habilitação formal não garante acesso;
- a classificação não substitui validação normativa posterior;
- a tabela deve ser refinada com fontes oficiais do CNES, SIGTAP e portarias ministeriais.

A presença de uma habilitação ou serviço em determinada linha de cuidado não deve ser interpretada como evidência isolada de suficiência da oferta, disponibilidade operacional, qualidade assistencial ou acesso oportuno. Essas conclusões exigem cruzamento com outras bases, parâmetros assistenciais e validação metodológica adicional.

## 7. Próximos passos

Os próximos passos recomendados são:

- validar códigos oficiais;
- ampliar linhas de cuidado;
- criar função R para aplicar a classificação;
- gerar base tabular de habilitações;
- criar indicadores de habilitações e serviços especializados;
- cruzar com produção ambulatorial e hospitalar.

A evolução desta classificação deve manter rastreabilidade das alterações, controle de versão da tabela de referência e documentação dos critérios de inclusão, exclusão e agrupamento de códigos.
