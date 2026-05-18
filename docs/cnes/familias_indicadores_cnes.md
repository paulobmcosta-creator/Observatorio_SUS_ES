# Famílias de Indicadores Derivados do CNES no Observatório SUS-ES

## 1. Finalidade do documento

Este documento define as famílias de indicadores derivadas do Cadastro Nacional de Estabelecimentos de Saúde (CNES) no Observatório SUS-ES. Ele organiza, em nível técnico-metodológico, os grupos de indicadores que deverão orientar a análise da oferta instalada, das habilitações, da capacidade física, da força de trabalho, dos vazios assistenciais e da compatibilidade entre oferta, produção e desfechos.

O documento funciona como ponte entre a visão analítica do CNES, os produtos tabulares derivados, os indicadores técnicos de oferta já existentes e os ciclos futuros de desenvolvimento técnico. Ele se relaciona diretamente com:

- `docs/cnes/visao_analitica_cnes_observatorio.md`;
- `docs/cnes/produtos_tabulares_cnes.md`;
- `docs/cnes/contrato_dados_cnes_piloto.md`;
- `docs/cnes/metadados_cnes_piloto.md`;
- `metadata/cnes/schema_cnes_piloto.yml`;
- `metadata/cnes/dicionario_cnes_piloto.csv`.

O objetivo não é implementar todos os indicadores neste momento, mas organizar uma arquitetura analítica para orientar futuros scripts, testes, metadados, dicionários e painéis. Assim, as famílias descritas aqui devem ser entendidas como especificação metodológica, e não como produtos executáveis já disponíveis no repositório.

Os indicadores derivados do CNES devem ser tratados como indicadores de oferta, estrutura, capacidade instalada e disponibilidade potencial. Eles não devem ser interpretados, isoladamente, como indicadores diretos de acesso, qualidade, produção assistencial ou resultado em saúde. Para análises de produção, acesso efetivo e desfechos, será necessário articular o CNES com outras fontes, como SIH/SUS, SIA/SUS, SIM, IBGE e ANS.

## 2. Princípio geral das famílias de indicadores

As famílias de indicadores devem derivar dos produtos tabulares definidos no Bloco 2 da documentação metodológica do CNES. Esses produtos organizam as dimensões estruturais da rede e funcionam como bases relacionais auditáveis para a construção posterior de indicadores.

As principais bases de origem são:

- base de estabelecimentos;
- base de leitos;
- base de habilitações e serviços especializados;
- base de equipamentos;
- base de profissionais;
- camada analítica em formato longo.

Cada indicador deve preservar, sempre que possível:

- competência;
- município;
- código IBGE;
- região de saúde;
- macrorregião de saúde;
- código CNES, quando o nível de agregação permitir;
- grupo do indicador;
- nome padronizado do indicador;
- valor;
- unidade;
- estratificadores;
- observação metodológica.

Os indicadores podem ter diferentes níveis de agregação, conforme a pergunta analítica e a disponibilidade dos dados:

- estabelecimento;
- município;
- região de saúde;
- macrorregião;
- estado.

Indicadores de contagem simples podem derivar diretamente das bases CNES, desde que a unidade de observação esteja corretamente definida. Indicadores de taxa, razão ou cobertura relativa exigem denominadores populacionais externos, especialmente IBGE e, quando for o caso, ANS para aproximação da população potencialmente dependente do SUS.

A implementação futura deve evitar agregações prematuras. Sempre que possível, os indicadores devem ser rastreáveis até os produtos tabulares por estabelecimento, competência e município, permitindo auditoria, revisão de regras de classificação e reprodução dos resultados.

## 3. Família 1 — Oferta geral de estabelecimentos

### 3.1. Finalidade

Esta família mede a presença, a distribuição e o perfil institucional dos estabelecimentos de saúde cadastrados no CNES. Ela descreve a rede enquanto conjunto de unidades cadastradas, permitindo distinguir estabelecimentos por território, tipo, natureza jurídica, esfera administrativa e vínculo com o SUS.

Essa família deve responder:

- quantos estabelecimentos existem;
- onde estão localizados;
- que tipos de estabelecimentos existem;
- que parte da rede atende ao SUS;
- qual é a composição pública, privada, filantrópica ou conveniada da rede;
- quais municípios e regiões concentram estabelecimentos.

### 3.2. Produto tabular de origem

A origem principal desta família é:

- base de estabelecimentos.

### 3.3. Indicadores prioritários

Os indicadores prioritários desta família incluem:

- total_estabelecimentos;
- total_estabelecimentos_sus;
- total_estabelecimentos_nao_sus;
- proporcao_estabelecimentos_sus;
- estabelecimentos_por_tipo;
- estabelecimentos_por_natureza_juridica;
- estabelecimentos_por_esfera_administrativa;
- estabelecimentos_por_regiao_saude;
- estabelecimentos_por_municipio;
- taxa_estabelecimentos_por_100_mil_habitantes;
- concentracao_estabelecimentos_municipio_polo.

### 3.4. Interpretação

Esses indicadores são úteis para caracterizar a rede e sua distribuição territorial, mas ainda são insuficientes para avaliar capacidade assistencial efetiva. Um território pode ter muitos estabelecimentos pequenos e baixa capacidade instalada, enquanto outro pode ter menos unidades, porém com maior complexidade, mais leitos, equipamentos, serviços habilitados e profissionais.

A leitura desta família deve, portanto, ser combinada com as famílias de habilitações, leitos, equipamentos e força de trabalho. Quando houver taxas por habitante, também será necessário explicitar o denominador populacional utilizado.

### 3.5. Limitações

O número de estabelecimentos não mede, sozinho:

- porte;
- complexidade;
- capacidade instalada;
- produção;
- qualidade;
- funcionamento efetivo;
- acesso da população.

A presença cadastral de um estabelecimento indica existência registrada em uma competência, mas não comprova funcionamento pleno, escala assistencial, acesso oportuno, produção compatível ou qualidade do cuidado.

## 4. Família 2 — Habilitações e serviços especializados

### 4.1. Finalidade

Esta família é estratégica para a atenção especializada, pois identifica a presença territorial de serviços formalmente habilitados ou cadastrados em linhas de cuidado prioritárias. Ela ajuda a transformar a leitura da rede em análise de especialização, regionalização e potenciais vazios assistenciais.

Essa família deve responder:

- quais serviços especializados existem;
- onde estão localizados;
- quais regiões têm ou não habilitações estratégicas;
- quais estabelecimentos concentram múltiplas habilitações;
- quais linhas de cuidado apresentam maior concentração ou vazio assistencial.

### 4.2. Produto tabular de origem

A origem principal desta família é:

- base de habilitações e serviços especializados.

### 4.3. Linhas de cuidado prioritárias

As linhas de cuidado prioritárias devem incluir, no mínimo:

- oncologia;
- cardiologia;
- Rede de Urgência e Emergência;
- UTI e cuidado crítico;
- diagnóstico e apoio terapêutico;
- terapia renal substitutiva;
- reabilitação;
- outras linhas estratégicas futuras.

A classificação por linha de cuidado deverá ser documentada em ciclos futuros, com códigos oficiais, critérios de inclusão, critérios de exclusão e regras para lidar com mudanças temporais nas habilitações e serviços.

### 4.4. Indicadores prioritários

Os indicadores prioritários desta família incluem:

- estabelecimentos_habilitados_total;
- estabelecimentos_habilitados_por_linha_cuidado;
- estabelecimentos_habilitados_por_regiao_saude;
- servicos_habilitados_por_100_mil_habitantes;
- regioes_sem_habilitacao_estrategica;
- municipios_sem_servico_habilitado;
- diversidade_habilitacoes_por_regiao;
- estabelecimentos_com_multiplas_habilitacoes;
- concentracao_habilitacoes_municipio_polo;
- proporcao_habilitacoes_em_estabelecimentos_sus.

### 4.5. Exemplos por linha de cuidado

Os exemplos abaixo são referências conceituais para orientar classificações futuras. Eles não substituem uma tabela oficial de códigos e não devem ser interpretados como lista fechada.

#### Oncologia

- CACON;
- UNACON;
- UNACON com radioterapia;
- UNACON com hematologia;
- UNACON pediátrica;
- hospital geral com cirurgia oncológica;
- serviço isolado de radioterapia;
- serviço de oncologia clínica.

#### Cardiologia

- centro de referência em alta complexidade cardiovascular;
- unidade de assistência em alta complexidade cardiovascular;
- cirurgia cardiovascular adulta;
- cirurgia cardiovascular pediátrica;
- cirurgia vascular;
- cardiologia intervencionista;
- procedimentos endovasculares extracardíacos;
- laboratório de eletrofisiologia.

#### Rede de Urgência e Emergência

- porta hospitalar de urgência;
- UPA;
- SAMU;
- sala de estabilização;
- leitos de retaguarda;
- leitos de UTI;
- pronto-socorro;
- componentes habilitados da RUE.

### 4.6. Interpretação

Essa família ajuda a identificar a existência formal de oferta especializada e a presença de vazios regionais. Ela permite observar se determinadas linhas de cuidado estão concentradas em poucos estabelecimentos ou municípios, se há regiões sem serviços estratégicos e se a organização territorial da rede é compatível com a regionalização pretendida.

A interpretação deve distinguir habilitação formal de capacidade operacional real. A existência de habilitação é uma informação estrutural relevante, mas precisa ser confrontada com produção, leitos, equipamentos, profissionais e fluxos assistenciais.

### 4.7. Limitações

Habilitação formal não garante:

- produção efetiva;
- acesso oportuno;
- qualidade do cuidado;
- suficiência da oferta;
- funcionamento regular;
- disponibilidade de equipe, leito ou equipamento.

Essa família deve ser usada como camada de oferta formal e não como prova isolada de funcionamento ou resolutividade assistencial.

## 5. Família 3 — Capacidade instalada física

### 5.1. Finalidade

Esta família mede a capacidade física instalada da rede, especialmente leitos e equipamentos. Ela aproxima a dimensão material da oferta cadastrada e permite avaliar a distribuição territorial de recursos hospitalares, tecnológicos e de apoio diagnóstico ou terapêutico.

Essa família deve responder:

- quantos leitos existem;
- quantos leitos estão disponíveis ao SUS;
- onde estão os leitos de maior complexidade;
- onde estão os equipamentos estratégicos;
- quais regiões apresentam insuficiência ou concentração de capacidade instalada.

### 5.2. Produtos tabulares de origem

As origens principais desta família são:

- base de leitos;
- base de equipamentos;
- base de estabelecimentos, como apoio.

### 5.3. Indicadores prioritários de leitos

Os indicadores prioritários de leitos incluem:

- leitos_existentes_total;
- leitos_sus_total;
- leitos_nao_sus_total;
- proporcao_leitos_sus;
- leitos_totais_por_1000_habitantes;
- leitos_sus_por_1000_habitantes;
- leitos_uti_sus_por_100_mil_habitantes;
- leitos_complementares_por_regiao_saude;
- leitos_retaguarda_rue_por_100_mil_habitantes;
- municipios_sem_leitos_hospitalares;
- regioes_sem_leitos_uti_sus;
- concentracao_leitos_municipio_polo.

### 5.4. Indicadores prioritários de equipamentos

Os indicadores prioritários de equipamentos incluem:

- equipamentos_existentes_total;
- equipamentos_disponiveis_sus_total;
- proporcao_equipamentos_sus;
- equipamentos_estrategicos_por_100_mil_habitantes;
- equipamentos_por_tipo;
- equipamentos_por_regiao_saude;
- regioes_sem_equipamento_estrategico;
- concentracao_equipamentos_municipio_polo.

### 5.5. Interpretação

Esses indicadores aproximam a capacidade material da rede, mas precisam ser interpretados com cautela. Eles permitem identificar disponibilidade cadastrada de leitos e equipamentos, concentração de recursos em municípios-polo, desigualdades regionais e potenciais vazios estruturais.

Taxas por habitante exigem denominadores populacionais consistentes. Comparações entre regiões devem considerar o papel regional dos serviços, fluxos de referência, porte populacional, capacidade privada não SUS e disponibilidade potencial ao SUS.

### 5.6. Limitações

Leitos e equipamentos cadastrados não garantem:

- disponibilidade operacional;
- equipe vinculada;
- manutenção;
- escala de funcionamento;
- agenda disponível;
- acesso pelo SUS;
- produção efetiva.

A disponibilidade cadastral deve ser confrontada, quando possível, com produção assistencial, registros de internação, exames ou procedimentos e informações de contexto regional.

## 6. Família 4 — Força de trabalho em saúde

### 6.1. Finalidade

Esta família caracteriza a disponibilidade e distribuição de profissionais de saúde registrados no CNES. Ela descreve a força de trabalho cadastrada por categoria, ocupação CBO, vínculo, carga horária e território, com atenção especial às ocupações estratégicas para a atenção especializada.

Essa família deve responder:

- quais profissionais estão cadastrados;
- onde estão distribuídos;
- quais ocupações estratégicas existem;
- qual parte da força de trabalho está vinculada ao SUS;
- como a força de trabalho se distribui entre municípios, regiões e estabelecimentos;
- onde há ausência ou concentração de profissionais especializados.

### 6.2. Produto tabular de origem

A origem principal desta família é:

- base de profissionais.

### 6.3. Cautela metodológica obrigatória

O CNES trabalha com ocupações registradas, vínculos e cargas horárias informadas. A CBO não deve ser interpretada automaticamente como título formal de especialista. Portanto, ocupações como “médico cardiologista”, “médico oncologista” ou outras ocupações especializadas devem ser tratadas como ocupação registrada no cadastro, não como certificação definitiva de especialidade profissional.

Também pode haver risco de dupla contagem de profissionais em razão de múltiplos vínculos. Um mesmo profissional pode aparecer em mais de um estabelecimento, ocupação, vínculo ou carga horária. Por isso, qualquer indicador deve explicitar se representa vínculos, profissionais únicos, ocupações, carga horária cadastrada ou outra unidade de contagem.

### 6.4. Indicadores prioritários

Os indicadores prioritários desta família incluem:

- profissionais_total_por_categoria;
- profissionais_sus_por_categoria;
- proporcao_profissionais_sus;
- profissionais_por_cbo;
- medicos_total;
- medicos_sus;
- medicos_por_1000_habitantes;
- medicos_sus_por_1000_habitantes;
- especialistas_por_100_mil_habitantes;
- profissionais_estrategicos_por_linha_cuidado;
- carga_horaria_total_por_categoria;
- carga_horaria_sus_por_categoria;
- carga_horaria_sus_por_1000_habitantes;
- regioes_sem_ocupacoes_estrategicas;
- concentracao_profissionais_municipio_polo.

### 6.5. Linhas de análise prioritárias

Exemplos de linhas de análise prioritárias incluem:

- especialidades básicas;
- especialidades cirúrgicas;
- especialidades cardiológicas;
- especialidades oncológicas;
- profissionais de enfermagem;
- fisioterapeutas;
- farmacêuticos;
- psicólogos;
- fonoaudiólogos;
- profissionais de apoio diagnóstico.

### 6.6. Interpretação

Essa família é importante para avaliar coerência entre serviços habilitados e força de trabalho cadastrada. Por exemplo, a análise pode investigar se regiões com habilitações estratégicas também apresentam profissionais compatíveis, ou se determinados serviços aparecem formalmente habilitados sem força de trabalho cadastrada em ocupações relacionadas.

A interpretação deve permanecer cautelosa. A presença de profissionais cadastrados não comprova escala real, presença física, disponibilidade de agenda, produtividade ou acesso efetivo da população.

### 6.7. Limitações

As principais limitações desta família incluem:

- risco de dupla contagem;
- múltiplos vínculos;
- divergência entre ocupação CBO e título profissional;
- carga horária informada não necessariamente equivale à disponibilidade real;
- presença profissional não garante escala, acesso ou continuidade do cuidado.

## 7. Família 5 — Vazios assistenciais e concentração regional

### 7.1. Finalidade

Esta família transforma a leitura estrutural do CNES em diagnóstico territorial para gestão. Ela combina diferentes dimensões da oferta cadastrada para identificar ausências, concentrações, dependência de polos e desigualdades regionais na distribuição da capacidade instalada.

Essa família deve responder:

- onde não há serviços;
- onde não há leitos;
- onde não há equipamentos;
- onde não há profissionais estratégicos;
- quais regiões dependem de um único município-polo;
- quais linhas de cuidado apresentam maior concentração territorial;
- onde a regionalização formal não encontra suporte na capacidade instalada.

### 7.2. Produtos tabulares de origem

As origens desta família são:

- base de estabelecimentos;
- base de habilitações e serviços especializados;
- base de leitos;
- base de equipamentos;
- base de profissionais.

### 7.3. Indicadores prioritários

Os indicadores prioritários desta família incluem:

- municipios_sem_estabelecimento_sus;
- municipios_sem_hospital;
- municipios_sem_pronto_atendimento;
- municipios_sem_leitos_sus;
- regioes_sem_upa;
- regioes_sem_samu;
- regioes_sem_leitos_uti_sus;
- regioes_sem_servico_oncologico_habilitado;
- regioes_sem_servico_cardiovascular_habilitado;
- regioes_sem_equipamento_estrategico;
- regioes_sem_ocupacao_profissional_estrategica;
- concentracao_estabelecimentos_municipio_polo;
- concentracao_leitos_municipio_polo;
- concentracao_equipamentos_municipio_polo;
- concentracao_profissionais_municipio_polo;
- indice_dependencia_polo_assistencial.

### 7.4. Interpretação

Essa família é central para planejamento regional e identificação de desigualdades territoriais. Ela permite observar se a distribuição da oferta cadastrada sustenta a organização regional da rede ou se determinados municípios e regiões dependem excessivamente de poucos polos assistenciais.

A interpretação deve sempre diferenciar ausência cadastral, insuficiência relativa e inadequação ao perfil de necessidade. Um município sem determinado serviço pode estar coberto por desenho regional pactuado, enquanto uma região inteira sem oferta estratégica pode indicar vazio assistencial relevante.

### 7.5. Limitações

Vazio assistencial não deve ser interpretado apenas pela ausência cadastral. É necessário considerar:

- porte populacional;
- desenho regional;
- fluxos assistenciais;
- pactuações intermunicipais;
- produção registrada;
- distância e acessibilidade;
- parâmetros assistenciais;
- cobertura de saúde suplementar.

Essa família exige critérios explícitos para definir o que será considerado vazio, concentração, dependência de polo ou insuficiência relativa.

## 8. Família 6 — Compatibilidade entre oferta, produção e desfechos

### 8.1. Finalidade

Esta família não deriva exclusivamente do CNES, mas depende dele como base estrutural para cruzamentos com produção assistencial e desfechos. Ela busca comparar a oferta cadastrada com internações, procedimentos, fluxos territoriais, mortalidade e denominadores populacionais.

Essa família deve responder:

- a produção ocorre em estabelecimentos habilitados?
- regiões com alta demanda têm oferta instalada compatível?
- há produção especializada em locais sem habilitação correspondente?
- há serviços habilitados com baixa ou nenhuma produção?
- a mortalidade ou internação se distribui de forma coerente com a oferta instalada?
- os fluxos de residência e atendimento revelam dependência regional?

### 8.2. Bases necessárias

As bases necessárias para esta família incluem:

- CNES;
- SIH/SUS;
- SIA/SUS;
- SIM;
- IBGE;
- ANS.

### 8.3. Indicadores prioritários

Os indicadores prioritários desta família incluem:

- procedimentos_realizados_em_estabelecimentos_habilitados;
- procedimentos_realizados_em_estabelecimentos_nao_habilitados;
- producao_por_estabelecimento_habilitado;
- producao_por_regiao_de_atendimento;
- internacoes_por_regiao_residencia;
- internacoes_por_regiao_atendimento;
- fluxos_residencia_atendimento;
- producao_vs_capacidade_instalada;
- internacoes_por_leito_sus;
- procedimentos_por_equipamento;
- procedimentos_por_profissional;
- mortalidade_hospitalar_em_estabelecimentos_habilitados;
- mortalidade_hospitalar_em_estabelecimentos_nao_habilitados;
- regioes_com_demanda_elevada_e_baixa_oferta_instalada.

### 8.4. Interpretação

Essa família é a mais analiticamente potente, mas também a mais complexa, porque exige cruzamentos metodologicamente controlados. Ela permite avaliar coerência entre capacidade instalada, produção registrada, fluxos de atendimento e desfechos, desde que sejam respeitadas as diferenças de unidade de observação, competência, território, estabelecimento executor e município de residência.

Indicadores desta família devem ser tratados como análises integradas, não como indicadores exclusivamente CNES. O CNES fornece a camada estrutural; SIH/SUS e SIA/SUS informam produção; SIM informa mortalidade; IBGE e ANS apoiam denominadores e contexto populacional.

### 8.5. Limitações

Esses indicadores exigem cautela por causa de:

- diferenças entre município de residência e município de atendimento;
- qualidade dos registros;
- risco de comparação inadequada entre estabelecimentos;
- necessidade de ajuste por complexidade, perfil dos pacientes e volume de produção;
- limites dos dados administrativos para medir qualidade.

Sem regras explícitas de cruzamento, temporalidade e classificação, esses indicadores podem produzir interpretações equivocadas sobre desempenho, suficiência, acesso ou qualidade.

## 9. Hierarquia de prioridade para desenvolvimento

A implementação das famílias de indicadores deve seguir uma hierarquia de prioridade. Essa hierarquia busca iniciar por indicadores estruturais mais diretamente derivados do CNES, avançar para diagnósticos territoriais de vazios e concentração, e somente depois construir indicadores integrados com produção e desfechos.

### 9.1. Prioridade 1 — Indicadores estruturais básicos

A primeira prioridade deve incluir:

- oferta geral de estabelecimentos;
- habilitações e serviços especializados;
- leitos SUS e totais;
- equipamentos estratégicos;
- profissionais por CBO.

Esses indicadores dependem prioritariamente do CNES e de denominadores populacionais. Eles são a base para descrever a rede cadastrada e construir uma leitura mínima da oferta instalada por território.

### 9.2. Prioridade 2 — Indicadores de vazios e concentração

A segunda prioridade deve incluir:

- regiões sem serviços estratégicos;
- municípios sem capacidade mínima;
- concentração no município-polo;
- dependência regional;
- desigualdade entre regiões de saúde.

Esses indicadores já exigem classificação territorial e parâmetros de interpretação. Também demandam regras explícitas para definir o que será considerado serviço estratégico, capacidade mínima, polo assistencial, vazio regional ou concentração relevante.

### 9.3. Prioridade 3 — Indicadores integrados oferta-produção-desfecho

A terceira prioridade deve incluir:

- produção em estabelecimentos habilitados;
- fluxos residência-atendimento;
- produção versus capacidade instalada;
- mortalidade versus oferta especializada;
- demanda elevada com baixa oferta.

Esses indicadores exigem cruzamento com SIH/SUS, SIA/SUS, SIM, IBGE e ANS. Por envolverem produção, fluxos e desfechos, devem ser implementados apenas depois que as bases CNES estiverem suficientemente padronizadas, documentadas e auditáveis.

## 10. Estrutura mínima sugerida para indicadores em formato longo

Quando implementados, os indicadores devem preferencialmente seguir uma estrutura padronizada em formato longo. Essa estrutura favorece auditoria, comparabilidade temporal, agregação territorial e integração futura com tabelas, painéis e mapas.

Os campos mínimos sugeridos são:

- fonte;
- competencia;
- ano;
- mes;
- uf;
- codigo_ibge_municipio;
- municipio;
- regiao_saude;
- macrorregiao_saude;
- codigo_cnes, quando aplicável;
- grupo_indicador;
- familia_indicador;
- indicador_nome;
- indicador_valor;
- unidade;
- recorte;
- categoria;
- estratificador_1;
- estratificador_2;
- observacao_metodologica;
- data_processamento;
- versao_pipeline.

Essa estrutura deve ser compatível com painéis, mapas, tabelas e auditoria posterior, mas não substitui as bases relacionais por entidade. Os indicadores agregados devem permanecer rastreáveis aos produtos tabulares de origem e às regras de transformação utilizadas.

## 11. Relação com os produtos tabulares

A tabela abaixo resume a relação entre famílias de indicadores, produtos tabulares principais e bases complementares necessárias.

| Família de indicadores | Produto tabular principal | Bases complementares |
| --- | --- | --- |
| Oferta geral de estabelecimentos | Base de estabelecimentos | IBGE; ANS; SIH/SUS; SIA/SUS |
| Habilitações e serviços especializados | Base de habilitações e serviços especializados | IBGE; SIH/SUS; SIA/SUS; SIM |
| Capacidade instalada física | Base de leitos; base de equipamentos | Base de estabelecimentos; IBGE; ANS; SIH/SUS; SIA/SUS |
| Força de trabalho em saúde | Base de profissionais | IBGE; ANS; SIH/SUS; SIA/SUS |
| Vazios assistenciais e concentração regional | Bases de estabelecimentos, habilitações/serviços, leitos, equipamentos e profissionais | IBGE; ANS; SIH/SUS; SIA/SUS; parâmetros regionais |
| Compatibilidade entre oferta, produção e desfechos | Camada CNES integrada por estabelecimento, competência e território | SIH/SUS; SIA/SUS; SIM; IBGE; ANS |

A tabela não define obrigatoriedade de cruzamento para todos os indicadores. Ela indica que algumas famílias podem começar com contagens CNES, enquanto outras dependem de denominadores, produção assistencial, desfechos ou parâmetros regionais.

## 12. O que este documento ainda não implementa

Este documento:

- não cria novos indicadores executáveis;
- não altera código R;
- não cria testes;
- não gera tabelas;
- não cria dashboards;
- não cria mapas;
- não realiza cruzamentos reais entre bases;
- não define todos os códigos oficiais de habilitação;
- não substitui dicionários futuros específicos de cada família de indicadores.

Sua função é estabelecer a arquitetura analítica para ciclos futuros de desenvolvimento do módulo CNES. A implementação deverá ser acompanhada de scripts, testes, schemas, dicionários, validações e documentação específica de cada indicador ou família.

## 13. Roadmap sugerido para implementação futura

A ordem recomendada para implementação técnica futura é:

1. Revisar e expandir indicadores gerais de oferta já existentes.
2. Classificar habilitações especializadas por linha de cuidado.
3. Implementar indicadores de habilitações e serviços especializados.
4. Implementar indicadores de leitos e capacidade instalada.
5. Implementar indicadores de equipamentos estratégicos.
6. Implementar indicadores de força de trabalho por CBO.
7. Implementar indicadores de vazios assistenciais e concentração regional.
8. Cruzar CNES com SIH/SUS e SIA/SUS.
9. Cruzar oferta especializada com SIM e indicadores de mortalidade.
10. Preparar camadas para painéis e mapas.

O próximo ciclo técnico mais racional, após este documento, é:

`feat(cnes): classificar habilitações especializadas por linha de cuidado`
