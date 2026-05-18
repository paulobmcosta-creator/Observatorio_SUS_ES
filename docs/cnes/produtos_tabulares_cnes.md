# Produtos Tabulares Derivados do CNES no Observatório SUS-ES

## 1. Finalidade do documento

Este documento define os produtos tabulares derivados do Cadastro Nacional de Estabelecimentos de Saúde (CNES) que deverão sustentar a análise da oferta instalada, habilitada e potencialmente disponível ao Sistema Único de Saúde (SUS) no Espírito Santo. A proposta é transformar a visão metodológica do CNES em uma arquitetura tabular clara, auditável e útil para o desenvolvimento posterior do Observatório SUS-ES.

O documento se relaciona diretamente com:

- `docs/cnes/visao_analitica_cnes_observatorio.md`;
- `docs/cnes/contrato_dados_cnes_piloto.md`;
- `metadata/cnes/schema_cnes_piloto.yml`;
- `metadata/cnes/dicionario_cnes_piloto.csv`.

A finalidade é orientar:

- a organização das bases intermediárias;
- o trabalho de bolsistas;
- o desenvolvimento de scripts futuros;
- a criação de indicadores;
- o cruzamento posterior com SIH/SUS, SIA/SUS, SIM, IBGE e ANS;
- a produção futura de painéis e mapas.

Este documento não implementa produtos tabulares reais. Ele estabelece a lógica metodológica e operacional que deverá orientar futuras implementações, mantendo a distinção entre estrutura cadastrada, capacidade potencialmente disponível ao SUS, produção assistencial e desfechos em saúde.

## 2. Princípio geral de organização tabular

O CNES não deve ser reduzido a uma única tabela ampla, com muitos campos heterogêneos e difícil auditoria. Uma tabela única tende a misturar unidades de observação diferentes, como estabelecimento, leito, equipamento, habilitação, serviço especializado e vínculo profissional. Essa mistura dificulta a validação, aumenta o risco de dupla contagem e reduz a transparência metodológica.

A organização tabular do módulo CNES deve seguir duas camadas complementares: uma camada relacional e auditável, voltada à preservação das entidades originais ou intermediárias, e uma camada analítica em formato longo, voltada à agregação, visualização e produção de indicadores.

### 2.1. Camada relacional e auditável

A camada relacional e auditável deve ser composta por bases por entidade, preservando a granularidade original ou intermediária de cada dimensão do CNES. No mínimo, essa camada deve contemplar bases de:

- estabelecimentos;
- leitos;
- habilitações e serviços especializados;
- equipamentos;
- profissionais.

Essa camada deve preservar:

- competência;
- código CNES;
- código IBGE do município;
- município;
- região de saúde;
- macrorregião de saúde, quando aplicável;
- chaves de relacionamento;
- campos originais relevantes;
- critérios de padronização;
- rastreabilidade.

A principal função dessa camada é permitir conferência, reprocessamento, controle de qualidade e auditoria por estabelecimento, município e competência antes de qualquer agregação. Sempre que possível, os produtos relacionais devem permitir retornar ao arquivo de origem e à regra de padronização utilizada.

### 2.2. Camada analítica para indicadores e painéis

A camada analítica deve ser derivada das bases relacionais e organizada preferencialmente em formato longo. Essa estrutura facilita comparações temporais, agregações territoriais, leitura por painéis e integração com futuras camadas de visualização.

Uma tabela analítica em formato longo pode conter campos como:

- fonte;
- competência;
- ano;
- mês;
- uf;
- código IBGE município;
- município;
- região de saúde;
- macrorregião de saúde;
- código CNES, quando aplicável;
- grupo_indicador;
- indicador_nome;
- indicador_valor;
- unidade;
- estratificador_1;
- estratificador_2;
- observacao_metodologica.

A camada analítica não substitui a camada relacional. Ela serve para agregações, painéis e visualização. Qualquer indicador agregado deve poder ser rastreado até uma base relacional auditável, com regra explícita de seleção, contagem, agregação, recorte territorial e tratamento de ausências.

## 3. Produto tabular 1 — Base de estabelecimentos

A base de estabelecimentos deve ser tratada como a base-mãe do módulo CNES. Ela organiza a identificação da rede de serviços, preserva a unidade institucional de referência e fornece a principal chave de relacionamento para outras dimensões, como leitos, habilitações, serviços, equipamentos, profissionais e produção assistencial.

### 3.1. Unidade de observação

A unidade de observação da base de estabelecimentos deve ser:

**Uma linha por competência + estabelecimento CNES.**

Essa definição significa que um mesmo estabelecimento deve aparecer novamente a cada competência em que estiver presente, permitindo análise temporal de mudanças cadastrais, institucionais e territoriais.

### 3.2. Finalidade

A base de estabelecimentos deve responder:

- qual rede existe;
- onde está localizada;
- qual é o perfil institucional dos estabelecimentos;
- qual parte da rede atende ao SUS;
- quais estabelecimentos podem ser relacionados com produção do SIH/SUS e SIA/SUS.

Essa base também deve permitir distinguir a rede total cadastrada da rede potencialmente disponível ao SUS, quando houver informação suficiente para essa separação.

### 3.3. Campos mínimos esperados

Os campos mínimos esperados para a base de estabelecimentos são:

- competencia;
- ano;
- mes;
- codigo_cnes;
- nome_estabelecimento;
- codigo_ibge_municipio;
- municipio;
- uf;
- regiao_saude;
- macrorregiao_saude;
- tipo_estabelecimento;
- natureza_juridica;
- esfera_administrativa;
- tipo_gestao;
- atende_sus;
- vinculo_sus, quando disponível;
- situacao_cadastral, quando disponível;
- arquivo_origem;
- data_processamento;
- versao_pipeline.

### 3.4. Chaves

As chaves conceituais e operacionais da base de estabelecimentos devem ser:

- chave primária conceitual: competencia + codigo_cnes;
- chaves territoriais: codigo_ibge_municipio, regiao_saude, macrorregiao_saude;
- chave de relacionamento com produção: codigo_cnes.

O nome do estabelecimento não deve ser usado como chave, pois pode variar no tempo, conter abreviações, apresentar grafias distintas ou ser alterado por mudanças administrativas.

### 3.5. Indicadores futuros derivados

Exemplos de indicadores futuros que podem ser derivados da base de estabelecimentos incluem:

- total de estabelecimentos;
- estabelecimentos SUS;
- estabelecimentos não SUS;
- estabelecimentos por tipo;
- estabelecimentos por natureza jurídica;
- estabelecimentos por região de saúde;
- proporção de estabelecimentos que atendem SUS;
- concentração de estabelecimentos no município-polo.

Esses indicadores deverão ser interpretados como medidas de estrutura cadastrada, e não como medidas diretas de acesso, produção ou qualidade.

### 3.6. Limitações

Estabelecimento cadastrado não significa funcionamento efetivo, acesso real ou produção assistencial. A presença de um estabelecimento no CNES indica existência cadastral em determinada competência, mas não comprova que o serviço estava operando plenamente, com equipe disponível, agenda aberta, produção suficiente ou capacidade de resposta compatível com a necessidade regional.

## 4. Produto tabular 2 — Base de leitos

A base de leitos deve organizar a capacidade hospitalar cadastrada no CNES, distinguindo, sempre que possível, leitos totais, leitos disponíveis ao SUS e leitos não disponíveis ao SUS. Essa base é central para análises de capacidade instalada hospitalar, mas deve ser interpretada com cautela, pois cadastro de leito não equivale automaticamente à disponibilidade operacional.

### 4.1. Unidade de observação

A unidade de observação da base de leitos deve ser:

**Uma linha por competência + estabelecimento CNES + tipo de leito + vínculo SUS, quando aplicável.**

Quando a fonte permitir detalhamento adicional, a especialidade do leito e o tipo de UTI ou cuidado crítico também devem compor a granularidade analítica.

### 4.2. Finalidade

A base de leitos mede a capacidade hospitalar instalada e permite distinguir oferta total e oferta disponível ao SUS. Ela deve apoiar análises sobre distribuição territorial de leitos, concentração regional, vazios assistenciais e compatibilidade entre capacidade cadastrada e internações registradas em bases de produção hospitalar.

### 4.3. Campos mínimos esperados

Os campos mínimos esperados para a base de leitos são:

- competencia;
- ano;
- mes;
- codigo_cnes;
- codigo_ibge_municipio;
- municipio;
- regiao_saude;
- macrorregiao_saude;
- tipo_leito;
- especialidade_leito, quando disponível;
- leitos_existentes;
- leitos_sus;
- leitos_nao_sus, quando derivável;
- leitos_complementares, quando aplicável;
- tipo_uti, quando aplicável;
- atende_sus;
- arquivo_origem;
- data_processamento;
- versao_pipeline.

### 4.4. Chaves

As chaves mínimas da base de leitos devem incluir:

- competencia;
- codigo_cnes;
- tipo_leito;
- especialidade_leito;
- indicador de vínculo SUS, quando aplicável.

A relação com a base de estabelecimentos deve ocorrer por competencia + codigo_cnes quando a análise exigir consistência temporal, e por codigo_cnes quando a finalidade for apenas identificar o estabelecimento em bases externas que usem essa chave.

### 4.5. Indicadores futuros derivados

Exemplos de indicadores futuros que podem ser derivados da base de leitos incluem:

- leitos totais por 1.000 habitantes;
- leitos SUS por 1.000 habitantes;
- proporção de leitos SUS;
- leitos UTI SUS por 100.000 habitantes;
- leitos de retaguarda por 100.000 habitantes;
- municípios sem leitos hospitalares;
- concentração regional de leitos.

Esses indicadores exigirão denominadores populacionais, preferencialmente provenientes do IBGE, e poderão exigir recortes adicionais para distinguir leitos gerais, especializados e críticos.

### 4.6. Limitações

Leito cadastrado não garante disponibilidade operacional, ocupação, equipe ou acesso real. A existência cadastral de leitos não informa, isoladamente, se o leito estava bloqueado, ocupado, sem equipe, em manutenção, sem insumos ou inacessível para determinados usuários. Conclusões sobre suficiência e acesso exigem cruzamento com SIH/SUS, parâmetros populacionais e informações complementares.

## 5. Produto tabular 3 — Base de habilitações e serviços especializados

A base de habilitações e serviços especializados deve organizar os registros que qualificam a capacidade formal da rede para ofertar determinadas linhas de cuidado, serviços estratégicos e componentes de atenção especializada. Esta é uma das bases mais relevantes para identificar oferta especializada, concentração territorial e vazios assistenciais.

### 5.1. Unidade de observação

A unidade de observação da base de habilitações e serviços especializados deve ser:

**Uma linha por competência + estabelecimento CNES + código de habilitação ou serviço especializado.**

Quando habilitações e serviços especializados estiverem em tabelas de origem distintas, a modelagem deve preservar a origem e documentar as regras usadas para integrá-los ou compará-los.

### 5.2. Finalidade

Esta é uma das bases mais estratégicas para a atenção especializada, pois permite identificar serviços formalmente habilitados e vazios assistenciais por linha de cuidado. Ela deve apoiar análises sobre disponibilidade territorial de serviços, dependência de polos assistenciais, concentração de alta complexidade e coerência entre habilitação formal e produção observada.

### 5.3. Campos mínimos esperados

Os campos mínimos esperados para a base de habilitações e serviços especializados são:

- competencia;
- ano;
- mes;
- codigo_cnes;
- nome_estabelecimento;
- codigo_ibge_municipio;
- municipio;
- regiao_saude;
- macrorregiao_saude;
- codigo_habilitacao;
- descricao_habilitacao;
- codigo_servico_especializado, quando aplicável;
- descricao_servico_especializado, quando aplicável;
- grupo_tematico;
- linha_cuidado;
- tipo_servico;
- atende_sus;
- status_habilitacao, quando disponível;
- data_inicio_habilitacao, quando disponível;
- arquivo_origem;
- data_processamento;
- versao_pipeline.

### 5.4. Classificação temática mínima

Em ciclos futuros, as habilitações e serviços deverão ser classificados, no mínimo, em:

- oncologia;
- cardiologia;
- Rede de Urgência e Emergência;
- UTI e cuidado crítico;
- diagnóstico e apoio terapêutico;
- terapia renal substitutiva;
- reabilitação;
- outras linhas estratégicas.

Essa classificação deverá ser documentada em schema, dicionário ou documento metodológico próprio, com critérios explícitos para inclusão, exclusão, agrupamento e revisão de códigos.

### 5.5. Exemplos de habilitações e serviços por linha de cuidado

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

### 5.6. Indicadores futuros derivados

Exemplos de indicadores futuros que podem ser derivados da base de habilitações e serviços especializados incluem:

- estabelecimentos habilitados por linha de cuidado;
- regiões sem habilitação estratégica;
- serviços habilitados por 100.000 habitantes;
- estabelecimentos com múltiplas habilitações;
- diversidade de habilitações por região;
- concentração de habilitações em município-polo.

Esses indicadores deverão preservar a distinção entre habilitação formal, serviço cadastrado, produção realizada e acesso efetivo.

### 5.7. Limitações

Habilitação formal não garante produção, acesso, qualidade, suficiência ou funcionamento regular do serviço. Um estabelecimento pode possuir habilitação registrada sem produzir volume correspondente em determinada competência, ou pode apresentar produção influenciada por fluxos regionais, pactuações, regulação, disponibilidade de equipe e condições operacionais não observáveis apenas no CNES.

## 6. Produto tabular 4 — Base de equipamentos

A base de equipamentos deve organizar os recursos tecnológicos cadastrados no CNES, especialmente aqueles relevantes para diagnóstico, apoio terapêutico e atenção especializada. Essa base deve permitir identificar a distribuição territorial de equipamentos e sua disponibilidade informada, incluindo disponibilidade ao SUS quando a fonte permitir.

### 6.1. Unidade de observação

A unidade de observação da base de equipamentos deve ser:

**Uma linha por competência + estabelecimento CNES + tipo de equipamento.**

Quando houver campos de quantidade existente, quantidade em uso e quantidade disponível ao SUS, esses campos devem ser preservados separadamente para evitar interpretações indevidas.

### 6.2. Finalidade

A base de equipamentos caracteriza a disponibilidade territorial de recursos tecnológicos relevantes para diagnóstico e tratamento. Ela deve apoiar análises sobre concentração de equipamentos estratégicos, vazios tecnológicos, dependência de municípios-polo e coerência entre equipamentos cadastrados e exames ou procedimentos realizados.

### 6.3. Campos mínimos esperados

Os campos mínimos esperados para a base de equipamentos são:

- competencia;
- ano;
- mes;
- codigo_cnes;
- codigo_ibge_municipio;
- municipio;
- regiao_saude;
- macrorregiao_saude;
- codigo_equipamento, quando disponível;
- tipo_equipamento;
- descricao_equipamento;
- quantidade_existente;
- quantidade_em_uso, quando disponível;
- quantidade_disponivel_sus, quando disponível;
- disponibilidade;
- grupo_tematico;
- atende_sus;
- arquivo_origem;
- data_processamento;
- versao_pipeline.

### 6.4. Indicadores futuros derivados

Exemplos de indicadores futuros que podem ser derivados da base de equipamentos incluem:

- equipamentos por 100.000 habitantes;
- equipamentos disponíveis ao SUS por 100.000 habitantes;
- proporção de equipamentos disponíveis ao SUS;
- regiões sem equipamento estratégico;
- concentração de equipamentos no município-polo.

Esses indicadores exigirão denominadores populacionais e critérios explícitos para selecionar equipamentos estratégicos, distinguir disponibilidade total e SUS, e tratar equipamentos fora de uso ou sem informação completa.

### 6.5. Limitações

Equipamento cadastrado não garante funcionamento, manutenção, equipe habilitada, disponibilidade de agenda ou acesso pelo SUS. A existência cadastral também não informa, sozinha, capacidade operacional, produtividade, tempo de espera, contratualização, escala de profissionais ou barreiras regulatórias.

## 7. Produto tabular 5 — Base de profissionais

A base de profissionais deve organizar a força de trabalho em saúde cadastrada no CNES. Essa é uma das dimensões mais sensíveis do ponto de vista metodológico, pois registros de profissionais podem representar vínculos, ocupações, cargas horárias e estabelecimentos, e não necessariamente profissionais únicos disponíveis em tempo integral.

### 7.1. Unidade de observação

A unidade de observação da base de profissionais deve ser definida com cautela:

**Uma linha por competência + estabelecimento CNES + ocupação CBO + vínculo/carga horária, conforme granularidade disponível.**

Será necessário distinguir, quando tecnicamente possível:

- vínculo profissional;
- profissional único;
- carga horária;
- ocupação CBO;
- disponibilidade ao SUS.

A definição do tipo de contagem deve ser explícita em qualquer base ou indicador derivado, para evitar misturar vínculos, pessoas e carga horária como se fossem a mesma medida.

### 7.2. Finalidade

Essa base caracteriza a força de trabalho em saúde cadastrada no CNES, com especial atenção às ocupações estratégicas para a atenção especializada. Ela deve apoiar análises sobre distribuição territorial de profissionais, presença de ocupações críticas, disponibilidade potencial ao SUS e compatibilidade entre equipe cadastrada, serviços habilitados e produção assistencial.

### 7.3. Campos mínimos esperados

Os campos mínimos esperados para a base de profissionais são:

- competencia;
- ano;
- mes;
- codigo_cnes;
- codigo_ibge_municipio;
- municipio;
- regiao_saude;
- macrorregiao_saude;
- cbo;
- descricao_cbo;
- categoria_profissional;
- ocupacao_especifica;
- grupo_ocupacional;
- vinculo_sus, quando disponível;
- carga_horaria_ambulatorial, quando disponível;
- carga_horaria_hospitalar, quando disponível;
- carga_horaria_total, quando disponível;
- identificador_profissional_pseudonimizado, apenas se houver base e regra segura;
- tipo_contagem;
- arquivo_origem;
- data_processamento;
- versao_pipeline.

### 7.4. Cautela metodológica obrigatória

O CNES trabalha com ocupações registradas, vínculos e cargas horárias informadas. A CBO não deve ser interpretada automaticamente como título formal de especialista. Portanto, “médico cardiologista”, “médico oncologista” ou outras ocupações especializadas devem ser tratadas como ocupação registrada no cadastro, não como certificação definitiva de especialidade profissional.

Essa cautela é especialmente importante em análises de suficiência profissional. A ocupação cadastrada pode ser útil para mapear a distribuição de perfis assistenciais, mas não comprova, isoladamente, titulação formal, disponibilidade real, escala presencial, produtividade ou acesso da população ao profissional.

### 7.5. Indicadores futuros derivados

Exemplos de indicadores futuros que podem ser derivados da base de profissionais incluem:

- médicos por 1.000 habitantes;
- médicos SUS por 1.000 habitantes;
- profissionais por categoria;
- profissionais por CBO;
- especialistas por 100.000 habitantes;
- carga horária SUS por 1.000 habitantes;
- regiões sem ocupações estratégicas;
- razão profissionais SUS/total.

A interpretação desses indicadores deve deixar claro se a medida representa vínculos, profissionais únicos, ocupações, carga horária ou outra unidade de contagem.

### 7.6. Limitações

As principais limitações da base de profissionais incluem:

- risco de dupla contagem;
- múltiplos vínculos;
- divergência entre ocupação e especialização formal;
- carga horária informada não necessariamente equivale a disponibilidade efetiva;
- presença profissional não garante escala, cobertura ou acesso.

Essas limitações exigem documentação rigorosa dos critérios de contagem e cautela na comparação entre municípios, regiões e competências.

## 8. Relação entre produtos tabulares e futuros indicadores

Os produtos tabulares relacionais alimentam indicadores ao organizar unidades de observação consistentes, chaves preservadas e campos mínimos auditáveis. Indicadores agregados devem ser entendidos como produtos derivados, e não como substitutos das bases relacionais.

| Produto tabular | Exemplos de indicadores | Bases complementares necessárias |
| --- | --- | --- |
| Base de estabelecimentos | total de estabelecimentos; estabelecimentos SUS; estabelecimentos por tipo; proporção que atende SUS; concentração no município-polo | IBGE; ANS; SIH/SUS; SIA/SUS |
| Base de leitos | leitos totais por 1.000 habitantes; leitos SUS por 1.000 habitantes; leitos UTI SUS por 100.000 habitantes; municípios sem leitos hospitalares | IBGE; SIH/SUS; ANS |
| Base de habilitações e serviços | estabelecimentos habilitados por linha de cuidado; regiões sem habilitação estratégica; serviços habilitados por 100.000 habitantes; diversidade de habilitações por região | IBGE; SIH/SUS; SIA/SUS; SIM |
| Base de equipamentos | equipamentos por 100.000 habitantes; equipamentos disponíveis ao SUS por 100.000 habitantes; regiões sem equipamento estratégico | IBGE; SIA/SUS; ANS |
| Base de profissionais | médicos por 1.000 habitantes; profissionais por CBO; carga horária SUS por 1.000 habitantes; regiões sem ocupações estratégicas | IBGE; ANS; SIH/SUS; SIA/SUS |

A escolha das bases complementares dependerá da pergunta analítica. Indicadores per capita exigem denominadores populacionais. Indicadores de compatibilidade entre oferta e produção exigem SIH/SUS ou SIA/SUS. Indicadores de desfecho ou necessidade devem ser analisados com cautela e podem exigir SIM, IBGE, ANS e parâmetros epidemiológicos adicionais.

## 9. Chaves mínimas e regras transversais

As seguintes regras valem para todos os produtos tabulares derivados do CNES:

1. Preservar competência.
2. Preservar código CNES.
3. Preservar código IBGE do município.
4. Padronizar nomes de municípios.
5. Incluir região de saúde e macrorregião quando possível.
6. Distinguir oferta total e oferta SUS sempre que tecnicamente possível.
7. Preservar `arquivo_origem`.
8. Preservar `versao_pipeline`.
9. Não usar nome do estabelecimento como chave.
10. Não agregar antes de preservar base auditável por estabelecimento.
11. Documentar critérios de classificação temática.
12. Registrar limitações de interpretação.
13. Evitar misturar vínculo, estabelecimento e profissional único sem regra explícita.
14. Manter compatibilidade com futuras tabelas em formato longo.

Essas regras transversais buscam garantir que os produtos tabulares sejam reprodutíveis, auditáveis e compatíveis com análises futuras. A prioridade metodológica deve ser preservar a unidade de observação adequada antes de construir indicadores agregados.

## 10. O que este documento ainda não implementa

Este documento:

- não cria bases tabulares reais;
- não implementa scripts de extração;
- não implementa scripts de transformação;
- não cria indicadores novos;
- não cria dashboards;
- não cria mapas;
- não cruza CNES com SIH/SUS, SIA/SUS ou SIM;
- não define ainda todos os códigos oficiais de habilitação;
- não substitui documentação futura de schema e dicionário de cada produto.

Sua função é orientar a arquitetura metodológica e operacional dos produtos tabulares derivados do CNES. A implementação técnica deverá ocorrer em ciclos posteriores, com scripts, schemas, dicionários, testes e validações próprios.

## 11. Roadmap sugerido para implementação futura

A ordem recomendada para implementação técnica futura é:

1. Base de estabelecimentos.
2. Base de habilitações e serviços especializados.
3. Base de leitos.
4. Base de equipamentos.
5. Base de profissionais.
6. Indicadores de vazios assistenciais.
7. Cruzamento com produção ambulatorial e hospitalar.
8. Cruzamento com mortalidade e desfechos.
9. Painéis e mapas.

Essa ordem prioriza primeiro a base-mãe de estabelecimentos e, em seguida, a dimensão de habilitações e serviços especializados, que é estratégica para compreender a atenção especializada e os vazios assistenciais. Leitos, equipamentos e profissionais devem ser estruturados posteriormente com atenção às suas unidades de observação específicas e às limitações de disponibilidade real.

O próximo ciclo técnico mais racional, após este documento, será implementar ou documentar em maior detalhe:

`feat(cnes): classificar habilitações especializadas por linha de cuidado`
