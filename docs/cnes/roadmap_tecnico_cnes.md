# Roadmap Técnico do Módulo CNES no Observatório SUS-ES

## 1. Finalidade do roadmap

Este roadmap técnico organiza a evolução do módulo CNES no repositório do Observatório SUS-ES. Ele traduz a visão analítica, os produtos tabulares e as famílias de indicadores do CNES em uma sequência racional de ciclos futuros de desenvolvimento, distinguindo o que deve ser documentado, implementado, testado, versionado em metadados e integrado a outras bases.

O documento se relaciona diretamente com:

- `docs/cnes/visao_analitica_cnes_observatorio.md`;
- `docs/cnes/produtos_tabulares_cnes.md`;
- `docs/cnes/familias_indicadores_cnes.md`;
- `docs/cnes/contrato_dados_cnes_piloto.md`;
- `docs/cnes/metadados_cnes_piloto.md`;
- `metadata/cnes/schema_cnes_piloto.yml`;
- `metadata/cnes/dicionario_cnes_piloto.csv`.

O objetivo do roadmap não é implementar funcionalidades diretamente. Sua finalidade é orientar a sequência de implementação futura, indicando prioridades, dependências, tipos de PR, arquivos prováveis, critérios de aceite e cautelas metodológicas. Este documento, portanto, não cria bases, indicadores, cruzamentos, dashboards ou mapas; ele organiza a tomada de decisão técnica para os próximos ciclos.

## 2. Princípios de organização do desenvolvimento

O desenvolvimento do módulo CNES deve seguir princípios que preservem rastreabilidade, reprodutibilidade e coerência metodológica:

1. Não avançar para dashboards antes de consolidar bases, metadados e indicadores.
2. Não criar indicadores sem antes definir claramente o produto tabular de origem.
3. Não agregar dados antes de preservar bases auditáveis por estabelecimento.
4. Preservar competência, código CNES, código IBGE e região de saúde sempre que possível.
5. Distinguir oferta total e oferta SUS sempre que tecnicamente possível.
6. Documentar critérios de classificação temática antes de automatizá-los.
7. Criar testes junto com cada nova função R.
8. Atualizar metadados e dicionários sempre que novas saídas forem criadas.
9. Evitar dependências externas desnecessárias.
10. Tratar CNES como cadastro administrativo de oferta, não como base de produção, acesso, qualidade ou desfecho.

Esses princípios devem orientar tanto PRs documentais quanto PRs de implementação. A prioridade inicial deve ser consolidar produtos tabulares e regras metodológicas antes de gerar visualizações ou análises integradas de maior complexidade.

## 3. Situação atual do módulo CNES

O módulo CNES já possui uma base técnica inicial e documentação metodológica em expansão. Atualmente, já existem:

- pipeline piloto CNES em R;
- função de leitura;
- função de padronização da camada interim;
- função de validação;
- função de orquestração;
- testes unitários;
- teste de integração;
- fixtures sintéticas;
- contrato de dados;
- schema YAML;
- dicionário CSV da camada piloto;
- documentação metodológica;
- primeiros indicadores técnicos de oferta;
- CI configurado para executar testes R.

Também existem documentos que definem o papel analítico do CNES, a arquitetura tabular desejada e as famílias de indicadores a serem consideradas em ciclos futuros.

Ainda não existem, ou ainda não estão consolidados:

- produtos tabulares completos por entidade;
- base de estabelecimentos formalizada além do piloto;
- base de leitos;
- base de habilitações e serviços especializados;
- base de equipamentos;
- base de profissionais;
- classificação temática de habilitações;
- indicadores de vazios assistenciais;
- cruzamentos com SIH/SUS, SIA/SUS, SIM, IBGE e ANS;
- dashboards;
- mapas;
- camada final `data_processed` consolidada.

Essa situação indica que o próximo passo racional não é visualização, mas sim consolidação metodológica, tabular e programática das dimensões estruturais do CNES.

## 4. Visão geral dos ciclos de desenvolvimento

A sequência recomendada de ciclos de desenvolvimento é:

1. Ciclo 1 — Classificação de habilitações especializadas por linha de cuidado.
2. Ciclo 2 — Base tabular de estabelecimentos.
3. Ciclo 3 — Base tabular de habilitações e serviços especializados.
4. Ciclo 4 — Indicadores de habilitações e serviços especializados.
5. Ciclo 5 — Base de leitos e indicadores de capacidade hospitalar.
6. Ciclo 6 — Base de equipamentos e indicadores de recursos tecnológicos.
7. Ciclo 7 — Base de profissionais e indicadores de força de trabalho.
8. Ciclo 8 — Indicadores de vazios assistenciais e concentração regional.
9. Ciclo 9 — Integração com população IBGE e cobertura ANS.
10. Ciclo 10 — Cruzamento com produção SIH/SUS e SIA/SUS.
11. Ciclo 11 — Cruzamento com mortalidade SIM.
12. Ciclo 12 — Preparação de camada analítica para painéis e mapas.

Essa ordem pode ser ajustada conforme disponibilidade de dados, prioridades institucionais e capacidade de desenvolvimento. Ainda assim, a sequência proposta evita começar por painéis e mapas antes de consolidar bases, metadados, dicionários, testes e indicadores. Também separa ciclos que dependem apenas do CNES daqueles que exigem integração com bases externas.

## 5. Ciclo 1 — Classificação de habilitações especializadas por linha de cuidado

### 5.1. Objetivo

Definir e implementar uma classificação temática inicial das habilitações e serviços especializados do CNES, priorizando linhas de cuidado estratégicas. Esse ciclo deve transformar listas de códigos e descrições em uma tabela de referência auditável, capaz de apoiar bases tabulares, indicadores e análises futuras.

### 5.2. Linhas de cuidado prioritárias

As linhas de cuidado prioritárias são:

- oncologia;
- cardiologia;
- Rede de Urgência e Emergência;
- UTI e cuidado crítico;
- diagnóstico e apoio terapêutico;
- terapia renal substitutiva;
- reabilitação;
- outras linhas estratégicas futuras.

### 5.3. Arquivos prováveis

Arquivos prováveis para esse ciclo incluem:

- `metadata/cnes/classificacao_habilitacoes_cnes.csv`;
- `docs/cnes/classificacao_habilitacoes_cnes.md`;
- `tests/test_classificacao_habilitacoes_cnes.R`.

Se houver código R futuro, um arquivo provável é:

- `src/transform/classificar_habilitacoes_cnes.R`.

### 5.4. Tipo de PR

Esse ciclo pode ser iniciado como PR documental/metadados, com tabela de referência e documentação metodológica. Em seguida, pode evoluir para PR com código R para aplicar a classificação a bases de habilitações ou serviços especializados.

### 5.5. Critérios de aceite

Critérios mínimos de aceite:

- tabela de classificação criada;
- linhas de cuidado documentadas;
- códigos e descrições rastreáveis;
- teste verificando campos mínimos da classificação;
- README atualizado.

## 6. Ciclo 2 — Base tabular de estabelecimentos

### 6.1. Objetivo

Formalizar a base de estabelecimentos como base-mãe do módulo CNES. Essa base deve preservar uma linha por competência e estabelecimento, servindo como referência para leitos, habilitações, serviços, equipamentos, profissionais e cruzamentos futuros com produção assistencial.

### 6.2. Arquivos prováveis

Arquivos prováveis:

- `src/transform/gerar_base_estabelecimentos_cnes.R`;
- `tests/test_base_estabelecimentos_cnes.R`;
- `metadata/cnes/schema_estabelecimentos_cnes.yml`;
- `metadata/cnes/dicionario_estabelecimentos_cnes.csv`;
- `docs/cnes/base_estabelecimentos_cnes.md`.

### 6.3. Produto esperado

O produto esperado é uma base intermediária auditável, com uma linha por competência + código CNES. Essa base deve preservar chaves de relacionamento, campos territoriais e variáveis institucionais suficientes para interpretar a posição do estabelecimento na rede.

### 6.4. Campos mínimos

Campos mínimos esperados:

- competência;
- código CNES;
- nome do estabelecimento;
- código IBGE;
- município;
- região de saúde;
- macrorregião;
- tipo de estabelecimento;
- natureza jurídica;
- esfera administrativa;
- gestão;
- atende SUS;
- arquivo de origem;
- versão do pipeline.

### 6.5. Critérios de aceite

Critérios de aceite:

- função implementada;
- teste criado;
- schema e dicionário atualizados;
- documentação criada;
- CI executando o teste.

## 7. Ciclo 3 — Base tabular de habilitações e serviços especializados

### 7.1. Objetivo

Criar base de habilitações e serviços especializados por estabelecimento, competência e linha de cuidado. Essa base deve preservar códigos originais, descrições, estabelecimento, território e classificação temática quando disponível.

### 7.2. Arquivos prováveis

Arquivos prováveis:

- `src/transform/gerar_base_habilitacoes_cnes.R`;
- `tests/test_base_habilitacoes_cnes.R`;
- `metadata/cnes/schema_habilitacoes_cnes.yml`;
- `metadata/cnes/dicionario_habilitacoes_cnes.csv`;
- `docs/cnes/base_habilitacoes_cnes.md`.

### 7.3. Produto esperado

O produto esperado é uma base com uma linha por competência + CNES + código de habilitação ou serviço especializado. Quando houver classificação temática disponível, a linha de cuidado deve ser atribuída de forma rastreável.

### 7.4. Critérios de aceite

Critérios de aceite:

- habilitações preservadas;
- linha de cuidado atribuída quando houver classificação;
- código CNES preservado;
- território preservado;
- teste implementado;
- documentação e metadados atualizados.

## 8. Ciclo 4 — Indicadores de habilitações e serviços especializados

### 8.1. Objetivo

Criar indicadores derivados da base de habilitações e serviços especializados. Esses indicadores devem apoiar a análise de oferta especializada, vazios regionais, concentração territorial e presença de serviços estratégicos.

### 8.2. Arquivos prováveis

Arquivos prováveis:

- `src/indicators/calcular_indicadores_cnes_habilitacoes.R`;
- `tests/test_indicadores_cnes_habilitacoes.R`;
- `metadata/cnes/dicionario_indicadores_cnes_habilitacoes.csv`;
- `docs/cnes/indicadores_cnes_habilitacoes.md`.

### 8.3. Indicadores possíveis

Indicadores possíveis:

- estabelecimentos habilitados por linha de cuidado;
- regiões sem habilitação estratégica;
- estabelecimentos com múltiplas habilitações;
- diversidade de habilitações por região;
- concentração de habilitações no município-polo;
- proporção de habilitações em estabelecimentos SUS.

### 8.4. Critérios de aceite

Critérios de aceite:

- função retorna formato longo;
- indicadores têm unidade e observação metodológica;
- testes cobrem cenários de sucesso e erro;
- dicionário de indicadores criado;
- documentação criada.

## 9. Ciclo 5 — Base de leitos e indicadores de capacidade hospitalar

### 9.1. Objetivo

Criar base de leitos e indicadores de capacidade instalada hospitalar. Esse ciclo deve distinguir leitos existentes, leitos SUS, leitos não SUS quando deriváveis e recortes de maior complexidade, como UTI e leitos complementares.

### 9.2. Arquivos prováveis

Arquivos prováveis:

- `src/transform/gerar_base_leitos_cnes.R`;
- `src/indicators/calcular_indicadores_cnes_leitos.R`;
- `tests/test_base_leitos_cnes.R`;
- `tests/test_indicadores_cnes_leitos.R`;
- `metadata/cnes/schema_leitos_cnes.yml`;
- `metadata/cnes/dicionario_leitos_cnes.csv`;
- `metadata/cnes/dicionario_indicadores_cnes_leitos.csv`;
- `docs/cnes/base_leitos_cnes.md`;
- `docs/cnes/indicadores_cnes_leitos.md`.

### 9.3. Indicadores possíveis

Indicadores possíveis:

- leitos existentes;
- leitos SUS;
- proporção de leitos SUS;
- leitos por 1.000 habitantes;
- leitos SUS por 1.000 habitantes;
- leitos UTI SUS por 100.000 habitantes;
- regiões sem leito UTI SUS;
- concentração de leitos no município-polo.

### 9.4. Dependências

Taxas por habitante exigem população IBGE. Indicadores de disponibilidade SUS dependem de campos confiáveis para distinguir oferta total e oferta SUS. Conclusões sobre suficiência exigem parâmetros assistenciais e, idealmente, cruzamentos com produção hospitalar.

## 10. Ciclo 6 — Base de equipamentos e indicadores de recursos tecnológicos

### 10.1. Objetivo

Criar base de equipamentos e indicadores de disponibilidade tecnológica. Esse ciclo deve caracterizar a distribuição territorial de equipamentos estratégicos, distinguindo quantidade existente, em uso e disponível ao SUS quando a fonte permitir.

### 10.2. Arquivos prováveis

Arquivos prováveis:

- `src/transform/gerar_base_equipamentos_cnes.R`;
- `src/indicators/calcular_indicadores_cnes_equipamentos.R`;
- `tests/test_base_equipamentos_cnes.R`;
- `tests/test_indicadores_cnes_equipamentos.R`;
- `metadata/cnes/schema_equipamentos_cnes.yml`;
- `metadata/cnes/dicionario_equipamentos_cnes.csv`;
- `metadata/cnes/dicionario_indicadores_cnes_equipamentos.csv`;
- `docs/cnes/base_equipamentos_cnes.md`;
- `docs/cnes/indicadores_cnes_equipamentos.md`.

### 10.3. Indicadores possíveis

Indicadores possíveis:

- equipamentos existentes;
- equipamentos disponíveis ao SUS;
- proporção de equipamentos SUS;
- equipamentos estratégicos por 100.000 habitantes;
- regiões sem equipamento estratégico;
- concentração de equipamentos no município-polo.

## 11. Ciclo 7 — Base de profissionais e indicadores de força de trabalho

### 11.1. Objetivo

Criar base de profissionais por CBO, vínculo e carga horária, com cautela sobre dupla contagem. Esse ciclo deve explicitar se as contagens representam vínculos, ocupações, profissionais únicos, carga horária ou outra unidade de observação.

### 11.2. Arquivos prováveis

Arquivos prováveis:

- `src/transform/gerar_base_profissionais_cnes.R`;
- `src/indicators/calcular_indicadores_cnes_profissionais.R`;
- `tests/test_base_profissionais_cnes.R`;
- `tests/test_indicadores_cnes_profissionais.R`;
- `metadata/cnes/schema_profissionais_cnes.yml`;
- `metadata/cnes/dicionario_profissionais_cnes.csv`;
- `metadata/cnes/dicionario_indicadores_cnes_profissionais.csv`;
- `docs/cnes/base_profissionais_cnes.md`;
- `docs/cnes/indicadores_cnes_profissionais.md`.

### 11.3. Indicadores possíveis

Indicadores possíveis:

- profissionais por CBO;
- médicos por 1.000 habitantes;
- médicos SUS por 1.000 habitantes;
- especialistas por 100.000 habitantes;
- carga horária SUS por 1.000 habitantes;
- regiões sem ocupações estratégicas;
- concentração de profissionais no município-polo.

### 11.4. Cautela metodológica

Cautelas obrigatórias:

- CBO não equivale automaticamente a título formal de especialista;
- múltiplos vínculos podem gerar dupla contagem;
- carga horária informada não garante disponibilidade efetiva.

## 12. Ciclo 8 — Indicadores de vazios assistenciais e concentração regional

### 12.1. Objetivo

Criar indicadores sintéticos para identificar ausência, concentração e dependência territorial da oferta instalada. Esse ciclo deve combinar estabelecimentos, habilitações, leitos, equipamentos e profissionais para apoiar análise regional.

### 12.2. Arquivos prováveis

Arquivos prováveis:

- `src/indicators/calcular_indicadores_cnes_vazios.R`;
- `tests/test_indicadores_cnes_vazios.R`;
- `metadata/cnes/dicionario_indicadores_cnes_vazios.csv`;
- `docs/cnes/indicadores_cnes_vazios.md`.

### 12.3. Indicadores possíveis

Indicadores possíveis:

- municípios sem hospital;
- regiões sem serviço oncológico habilitado;
- regiões sem serviço cardiovascular habilitado;
- regiões sem UTI SUS;
- regiões sem equipamento estratégico;
- regiões sem ocupação profissional estratégica;
- concentração de leitos no município-polo;
- concentração de equipamentos no município-polo;
- concentração de profissionais no município-polo;
- índice de dependência de polo assistencial.

### 12.4. Dependências

Esses indicadores dependem de classificação territorial, população, parâmetros assistenciais e interpretação regional. A ausência cadastral deve ser interpretada considerando desenho regional, fluxos assistenciais, pactuações e porte populacional.

## 13. Ciclo 9 — Integração com população IBGE e cobertura ANS

### 13.1. Objetivo

Adicionar denominadores populacionais e aproximação da população potencialmente dependente do SUS. Esse ciclo deve permitir cálculo de taxas e razões por habitante, além de análises que distinguem oferta total, oferta SUS e população de referência.

### 13.2. Arquivos prováveis

Arquivos prováveis:

- `src/transform/integrar_populacao_ibge_cnes.R`;
- `src/transform/integrar_cobertura_ans_cnes.R`;
- `tests/test_integracao_populacao_ans_cnes.R`;
- `docs/cnes/integracao_populacao_ans.md`;
- `metadata/cnes/dicionario_integracao_populacao_ans.csv`.

### 13.3. Produtos esperados

Produtos esperados:

- população municipal;
- população regional;
- cobertura de saúde suplementar;
- população estimada dependente do SUS;
- denominadores para taxas.

### 13.4. Cautela metodológica

População dependente do SUS é aproximação e precisa de regra explícita. A cobertura de saúde suplementar não equivale automaticamente à utilização efetiva do setor privado, e a ausência de plano não descreve sozinha necessidade, acesso ou demanda.

## 14. Ciclo 10 — Cruzamento com produção SIH/SUS e SIA/SUS

### 14.1. Objetivo

Relacionar oferta instalada e habilitada do CNES com produção hospitalar e ambulatorial. Esse ciclo deve permitir avaliar se procedimentos e internações ocorrem em estabelecimentos compatíveis com a estrutura e habilitação cadastradas, sempre com cautela metodológica.

### 14.2. Arquivos prováveis

Arquivos prováveis:

- `src/transform/integrar_cnes_sih.R`;
- `src/transform/integrar_cnes_sia.R`;
- `tests/test_integracao_cnes_sih.R`;
- `tests/test_integracao_cnes_sia.R`;
- `docs/cnes/integracao_cnes_sih_sia.md`.

### 14.3. Indicadores possíveis

Indicadores possíveis:

- procedimentos realizados em estabelecimentos habilitados;
- procedimentos realizados em estabelecimentos não habilitados;
- produção por estabelecimento habilitado;
- produção por região de atendimento;
- fluxos residência-atendimento;
- produção versus capacidade instalada.

### 14.4. Cautela metodológica

Município de residência e município de atendimento devem ser tratados separadamente. A análise também deve considerar competência, estabelecimento executor, perfil dos procedimentos, complexidade assistencial e diferenças entre produção registrada e acesso efetivo.

## 15. Ciclo 11 — Cruzamento com mortalidade SIM

### 15.1. Objetivo

Relacionar oferta instalada com desfechos e mortalidade, de forma cautelosa. Esse ciclo deve usar o CNES como camada estrutural, e não como explicação isolada para mortalidade ou qualidade do cuidado.

### 15.2. Arquivos prováveis

Arquivos prováveis:

- `src/transform/integrar_cnes_sim.R`;
- `tests/test_integracao_cnes_sim.R`;
- `docs/cnes/integracao_cnes_sim.md`.

### 15.3. Indicadores possíveis

Indicadores possíveis:

- mortalidade por região versus oferta especializada;
- mortalidade hospitalar em estabelecimentos habilitados;
- mortalidade hospitalar em estabelecimentos não habilitados;
- regiões com alta mortalidade e baixa oferta instalada.

### 15.4. Cautela metodológica

Esses indicadores não devem ser interpretados como avaliação direta de qualidade sem ajuste por risco, perfil dos pacientes, volume e complexidade. Relações entre oferta e mortalidade exigem desenho analítico explícito, controle de confundidores e cuidado com causalidade indevida.

## 16. Ciclo 12 — Preparação para painéis e mapas

### 16.1. Objetivo

Preparar dados para visualização, sem substituir as bases auditáveis. Esse ciclo deve gerar camadas derivadas para painéis e mapas apenas depois de consolidados produtos tabulares, indicadores, metadados e testes.

### 16.2. Arquivos prováveis

Arquivos prováveis:

- `src/transform/gerar_camada_painel_cnes.R`;
- `tests/test_camada_painel_cnes.R`;
- `docs/cnes/camada_painel_cnes.md`.

### 16.3. Produtos esperados

Produtos esperados:

- tabela longa de indicadores;
- agregações por município;
- agregações por região de saúde;
- agregações por linha de cuidado;
- campos compatíveis com mapas e painéis.

### 16.4. Cautela metodológica

Painéis e mapas devem vir depois da consolidação das bases e indicadores. Visualizações não devem substituir documentação metodológica, schemas, dicionários, testes ou bases relacionais auditáveis.

## 17. Tabela sintética do roadmap

| Ciclo | Foco | Tipo de entrega | Arquivos esperados | Dependências | Prioridade |
| --- | --- | --- | --- | --- | --- |
| 1 | Classificação de habilitações por linha de cuidado | Documental/metadados; depois código | `metadata/cnes/classificacao_habilitacoes_cnes.csv`; `docs/cnes/classificacao_habilitacoes_cnes.md`; `tests/test_classificacao_habilitacoes_cnes.R`; possível `src/transform/classificar_habilitacoes_cnes.R` | CNES; códigos e descrições de habilitação/serviço | Alta |
| 2 | Base tabular de estabelecimentos | Código R, testes, schema, dicionário e documentação | `src/transform/gerar_base_estabelecimentos_cnes.R`; `tests/test_base_estabelecimentos_cnes.R`; `metadata/cnes/schema_estabelecimentos_cnes.yml`; `metadata/cnes/dicionario_estabelecimentos_cnes.csv`; `docs/cnes/base_estabelecimentos_cnes.md` | CNES piloto e regras territoriais | Alta |
| 3 | Base de habilitações e serviços especializados | Código R, testes, schema, dicionário e documentação | `src/transform/gerar_base_habilitacoes_cnes.R`; `tests/test_base_habilitacoes_cnes.R`; `metadata/cnes/schema_habilitacoes_cnes.yml`; `metadata/cnes/dicionario_habilitacoes_cnes.csv`; `docs/cnes/base_habilitacoes_cnes.md` | CNES; ciclo 1; ciclo 2 | Alta |
| 4 | Indicadores de habilitações e serviços | Código R, testes, dicionário e documentação | `src/indicators/calcular_indicadores_cnes_habilitacoes.R`; `tests/test_indicadores_cnes_habilitacoes.R`; `metadata/cnes/dicionario_indicadores_cnes_habilitacoes.csv`; `docs/cnes/indicadores_cnes_habilitacoes.md` | Ciclos 1, 2 e 3 | Alta |
| 5 | Leitos e capacidade hospitalar | Código R, testes, schemas, dicionários e documentação | `src/transform/gerar_base_leitos_cnes.R`; `src/indicators/calcular_indicadores_cnes_leitos.R`; `tests/test_base_leitos_cnes.R`; `tests/test_indicadores_cnes_leitos.R`; metadados e docs de leitos | CNES; IBGE para taxas | Média-alta |
| 6 | Equipamentos e recursos tecnológicos | Código R, testes, schemas, dicionários e documentação | `src/transform/gerar_base_equipamentos_cnes.R`; `src/indicators/calcular_indicadores_cnes_equipamentos.R`; testes, metadados e docs de equipamentos | CNES; IBGE para taxas | Média |
| 7 | Profissionais e força de trabalho | Código R, testes, schemas, dicionários e documentação | `src/transform/gerar_base_profissionais_cnes.R`; `src/indicators/calcular_indicadores_cnes_profissionais.R`; testes, metadados e docs de profissionais | CNES; IBGE para taxas; regras de contagem | Média |
| 8 | Vazios assistenciais e concentração regional | Código R, testes, dicionário e documentação | `src/indicators/calcular_indicadores_cnes_vazios.R`; `tests/test_indicadores_cnes_vazios.R`; `metadata/cnes/dicionario_indicadores_cnes_vazios.csv`; `docs/cnes/indicadores_cnes_vazios.md` | Ciclos 2 a 7; população; parâmetros regionais | Média |
| 9 | População IBGE e cobertura ANS | Integração, testes, dicionário e documentação | `src/transform/integrar_populacao_ibge_cnes.R`; `src/transform/integrar_cobertura_ans_cnes.R`; `tests/test_integracao_populacao_ans_cnes.R`; docs e dicionário | IBGE; ANS; regras de denominador | Média |
| 10 | Produção SIH/SUS e SIA/SUS | Integração, testes e documentação | `src/transform/integrar_cnes_sih.R`; `src/transform/integrar_cnes_sia.R`; `tests/test_integracao_cnes_sih.R`; `tests/test_integracao_cnes_sia.R`; `docs/cnes/integracao_cnes_sih_sia.md` | CNES consolidado; SIH/SUS; SIA/SUS | Posterior |
| 11 | Mortalidade SIM | Integração, testes e documentação | `src/transform/integrar_cnes_sim.R`; `tests/test_integracao_cnes_sim.R`; `docs/cnes/integracao_cnes_sim.md` | CNES consolidado; SIM; desenho analítico | Posterior |
| 12 | Camada analítica para painéis e mapas | Transformação, testes e documentação | `src/transform/gerar_camada_painel_cnes.R`; `tests/test_camada_painel_cnes.R`; `docs/cnes/camada_painel_cnes.md` | Indicadores consolidados; territórios validados | Posterior |

## 18. Critérios gerais de aceite para futuros PRs

Critérios gerais para futuros PRs do módulo CNES:

1. Toda nova função R deve ter teste correspondente.
2. Todo novo produto tabular deve ter schema e dicionário.
3. Toda nova família de indicadores deve ter documentação e dicionário.
4. Todo novo cruzamento entre bases deve explicitar chaves e limitações.
5. Nenhum output gerado deve ser versionado sem justificativa.
6. Nenhuma agregação deve eliminar a base auditável por estabelecimento.
7. Toda taxa deve documentar denominador.
8. Toda classificação temática deve possuir tabela de referência ou regra documentada.
9. Todo PR deve atualizar o README do módulo quando alterar a arquitetura.
10. O CI deve continuar passando antes do merge.

Esses critérios não substituem revisões metodológicas específicas, mas fornecem um padrão mínimo para manter consistência, rastreabilidade e qualidade técnica.

## 19. O que não deve ser feito prematuramente

Ainda não se deve:

- criar dashboards antes de consolidar as bases;
- criar mapas antes de validar os territórios;
- cruzar bases sem chave documentada;
- criar indicadores compostos sem metodologia;
- comparar estabelecimentos sem ajuste adequado;
- tratar habilitação como sinônimo de funcionamento;
- tratar produção como sinônimo de acesso;
- tratar CBO como título formal de especialista;
- substituir bases auditáveis por tabelas agregadas.

Essas restrições são importantes para evitar que produtos visuais ou indicadores sintéticos ocultem limitações das fontes, problemas de unidade de observação ou escolhas metodológicas ainda não documentadas.

## 20. Próximo ciclo técnico recomendado

Após este roadmap, o próximo ciclo técnico recomendado é:

`feat(cnes): classificar habilitações especializadas por linha de cuidado`

Esse ciclo é prioritário porque conecta diretamente:

- a visão analítica do CNES;
- os produtos tabulares;
- as famílias de indicadores;
- as linhas de cuidado prioritárias do Observatório;
- os boletins-espelho de oncologia, cardiologia e RUE.

A classificação de habilitações especializadas cria uma ponte concreta entre o cadastro administrativo do CNES e a leitura temática da rede de atenção especializada. Ela deve ser implementada com tabela de referência, documentação, testes e regras explícitas antes da produção de indicadores mais complexos ou visualizações.
