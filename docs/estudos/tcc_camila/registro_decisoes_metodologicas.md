# Registro de decisões e alterações metodológicas — TCC da Camila / Observatório SUS-ES

**Versão:** 3.0
**Data de referência:** 18/11/2026 (mandato integrado v3)
**Finalidade:** preservar decisões aprovadas, pendências e alterações que deverão ser incorporadas ao texto do TCC em momento posterior, com rastreabilidade entre decisão, execução empírica, produto analítico e revisão da redação.
**Restrição:** este registro **não modifica** o TCC original nem homologa automaticamente resultados ainda não verificados.

## 1. Decisões homologadas e referência demográfica vigente

| ID | Decisão | Aplicação operacional | Efeito previsto no TCC | Situação |
|---|---|---|---|---|
| MET-001 | Manter mortalidade prematura (30–69 anos). | Preservar as 55 taxas padronizadas já calculadas para G0/I00–I99 e os métodos originalmente executados; manter distinção entre taxa padronizada e indicador ODS de probabilidade de morrer. | Explicitar definição, universo 30–69, oito grupos quinquenais, pesos e finalidade; não apresentá-la como única medida de mortalidade. | **Homologado — preservar** |
| MET-002 | Acrescentar taxas brutas gerais, específicas por faixa etária e padronizadas para todas as idades, **com análises por sexo e idade como diretriz geral obrigatória**. | Cobrir 2014–2024, ES e quatro Regiões de Saúde; aplicar a G0–G5; validar numeradores e denominadores por ano, município, sexo e faixa etária. Onde cobertura falhar, declarar lacuna sem inventar valores. | Revisar objetivos, métodos, resultados, tabelas, figuras, discussão e limitações, incluindo sexo e idade. | **Homologado — implementar** |
| MET-003 | Padronizar todas as idades com faixa terminal **80 anos ou mais (80+)**. | Usar grupos 0–4, 5–9, …, 75–79, 80+ (17 estratos), harmonizando óbitos, população anual e pesos de um **único padrão fixo escolhido**; agregar 80–84 e 85+ no numerador quando necessário. | Explicitar escolha de 80+, limites do grupo terminal e faixas comuns às taxas. | **Homologado — implementar** |
| MET-004 | Brasil/Censo 2022 HOMOLOGADO como padrão principal. | Fixar os pesos nacionais em 2014–2024 para todos os territórios e sexos. Preservar 2010 como sensibilidade sobre os mesmos denominadores anuais. | Reescrever métodos, figuras e resultados com referência à tabela SIDRA 9514. | Homologado, implementado e validado nos dados. |
| MET-005 | Fixar **quatro Regiões de Saúde do PDR/ES 2024 como referencial comum do Observatório SUS-ES para análises regionais do estado**; no TCC, a Região Norte recebe aprofundamento adicional. | Cobrir os 78 municípios: Norte (14), Central (15), Metropolitana (23), Sul (26), com regionalização aplicada retrospectivamente a 2014–2024. Observatório: quatro regiões com igual tratamento. TCC: quatro regiões + destaque analítico da Norte. | Revisar mapas, área de estudo, comparações e legendas; não declarar a divisão de 2024 historicamente vigente; não reintroduzir Noroeste 1 como recorte focal. | **Homologado — revisão textual obrigatória** |
| MET-006 | Institucionalizar comparação `CAUSABAS_O` × `CAUSABAS` **para todas as causas, grupos, estudos e territórios elegíveis**, e menções quando válidas; não restringir à cardiologia. | Comparar individualmente todos os registros válidos do SIM, produzir matrizes, saldos e alertas, investigar anomalias relevantes; manter I50 como caso de teste, sem misturar original, final e menção. | Incorporar no TCC o caso I50 e as limitações; criar especificação transversal do Observatório para todas as linhas de pesquisa. | **Homologado — executar na etapa transversal** |
| MET-008 | Usar taxas específicas por sexo e idade, além de totais, como regra geral; padronizar separadamente homens e mulheres **com os mesmos pesos etários** quando a comparação entre sexos for pretendida. | Conferir soma por sexo, grupos etários e valores ignorados nos arquivos SIM e denominadores oficiais; apresentar análise conjunta e por sexo com fórmula explícita. | Incorporar estratos e interpretação de desigualdades; publicar somente quando validado. | **Homologado — verificar cobertura e implementar** |
| MET-007 | Não modificar o TCC original durante a execução computacional. | Registrar toda mudança proposta em backlog revisável antes de alterar o manuscrito. | Revisões do texto somente em etapa autorizada, com correspondência entre tabelas, métodos e manuscrito. | **Homologado — preservar** |

## 2. Especificação mínima dos indicadores de mortalidade

- **Contagem de óbitos:** por ano, região, grupo de causa, sexo, idade e fonte/edição, respeitando elegibilidade da análise.
- **Taxa bruta para todas as idades:** óbitos elegíveis residentes do território / população do mesmo território e ano × 100.000. Óbitos de idade ignorada permanecem no total quando atenderem aos demais critérios; documentar sua quantidade.
- **Taxa específica:** óbitos da faixa / população da mesma faixa × 100.000; os intervalos finais usam **80+**, não 80–84 e 85+ separados.
- **Taxa padronizada para todas as idades (método direto):** 100.000 × soma, para os 17 estratos etários, de [(óbitos da faixa/população da faixa) × peso da faixa na população-padrão nacional fixada para a série (2022 principal e 2010 complementar)]. **Peso 80+ = soma dos pesos correspondentes a todas as idades ≥80** no padrão selecionado; o mesmo padrão é aplicado a todos os anos e regiões. Não extrapolar taxas ausentes e não calcular se faltarem grupos necessários.
- **Mortalidade prematura padronizada (30–69 anos):** manter os oito estratos quinquenais e normalizar pesos do padrão dentro de 30–69 anos, sem incorporar a faixa de 80+.
- **Sexo:** produzir análise por sexo e idade como diretriz geral aprovada. Para comparar taxas padronizadas de homens e mulheres, empregar pesos etários comuns do padrão escolhido, com numeradores e denominadores específicos de cada sexo, depois de validação integral. Informar lacunas em vez de omitir silenciosamente as estratificações.
- **Idade ignorada e universos incompletos:** contabilizar separadamente; nunca redistribuir automaticamente óbitos entre estratos. A taxa bruta e a taxa padronizada podem ter universos etários analíticos distintos; explicitar os quantitativos.
- **Controle comparativo:** validar totals da tabela etária contra os grupos G0–G5; conferir pesos ∑w=1, denominadores positivos, integridade territorial dos 78 municípios e séries temporais, com comparação aos checkpoints anteriores.
- **Interpretação:** manter lado a lado taxas brutas e padronizadas, esclarecendo seus diferentes significados; usar taxas específicas para idosos para não apagar a concentração de óbitos em 70+, 80+.

## 3. Questões pendentes ou que devem ser auditadas antes de declarar o módulo encerrado

| ID | Questão | Teste ou evidência necessária | Status |
|---|---|---|---|
| PEN-001 | Completude do denominador por sexo × idade × município × ano, especialmente nos anos com margens anteriormente ausentes. | Confrontar somas e cruzamentos com os originais oficiais, sem preencher lacunas por inferência silenciosa. | **Verificado nos 11 anos, inclusive as margens municipais, em taxas-ed2** |
| PEN-002 | Reprodução dos vetores de 17 e oito pesos. | Totais por sexo e idade do Brasil na tabela 9514 e soma dos pesos. | Homologado e validado em taxas-ed2. |
| PEN-003 | Tratamento de `IDADE` no SIM e classificação de ignorados. | Testes de codificação por unidade, centenários, valores inconsistentes; conciliação com a contagem bruta. | Validado no G0 contra IDADE.CNV, com ignorados contabilizados. |
| PEN-004 | Divergência SIM federal 2024 versus relatório estadual preliminar. | Reconciliação explícita de período, edição, residência, critérios de elegibilidade e data de atualização; não forçar coincidência. | **Questão em aberto** |
| PEN-005 | Ruptura I50 entre `CAUSABAS_O` e `CAUSABAS`. | Preservar matriz, comparações nacionais, menções e dados de investigação; consulta institucional se necessária; não inferir mecanismo específico apenas das associações. | **Achado confirmado; mecanismo em aberto** |
| PEN-006 | Definições históricas de SIH, SIA, CNES e SIGTAP. | Distinguir AIH de pessoa, produção de indivíduo, competência de ocorrência, fluxos interestaduais, cadastros CNES mensais e vigência histórica SIGTAP; conferir cada linha empírica. | CNES, PA e SIGTAP calculados nas 132 competências. SIH estadual completo e cobertura nacional parcial por competência. |
| PEN-007 | Risco de identificação em células pequenas e outputs institucionais. | Separar resultados analíticos preservados de saídas públicas sujeitas a avaliação de divulgação; não alterar estatísticas silenciosamente. | **Pendente de desenho de publicação** |
| PEN-008 | Limites inferenciais de comparações territoriais. | Explicitar que Norte integra total ES e preferir "demais regiões" ou "ES sem Norte" quando se requer comparador não sobreposto. | Comparador aplicado, revisão textual pendente. |

## 4. Registro permanente de alterações do TCC decorrentes da execução

**Instrução:** este é um backlog cumulativo, não uma lista fechada. Cada nova descoberta empírica, incompatibilidade de dados ou decisão metodológica que exija alterar o manuscrito deve receber um novo `TCC-MOD-###`, com status, evidência e impacto. Nunca apagar registros resolvidos; manter histórico de decisão.

| ID | Seção provável do manuscrito | Alteração exigida ou condicionada | Evidência de suporte / origem | Status |
|---|---|---|---|---|
| TCC-MOD-001 | Objetivos e metodologia | Expandir rol de indicadores: mortalidade prematura 30–69 **e** taxas brutas gerais, específicas etárias e padronizadas todas idades. | MET-001 a MET-003 | **Aprovada; redação pendente** |
| TCC-MOD-002 | Metodologia demográfica | Explicitar os 17 quinquênios com terminal 80+, oito faixas prematuras, referência 2022 e sensibilidade 2010, fórmulas e denominadores anuais. | MET-003, MET-004, taxas-ed2 | Validado nos dados, pendente no TCC. |
| TCC-MOD-003 | Área e recorte territorial | Revisar mapas, municipalização, texto e tabelas para PDR/ES 2024 retroprojetado; Norte integrada às quatro regiões; não usar Noroeste 1 focal. | MET-005 | **Aprovada; revisão pendente** |
| TCC-MOD-004 | Fontes e reprodutibilidade | Substituir referências a numeradores herdados por cadeia de arquivos originais SIM 2014–2024 com edição, hash, leitores e QA; manter referências de reconciliação. | Relatório local SIM 2014–2024 e recibos | Validado contra os originais, redação pendente. |
| TCC-MOD-005 | Métodos, resultados e discussão | Distinguir `CAUSABAS`, `CAUSABAS_O` e menção; tratar descontinuidade I50 2022–2024 e sensibilidade por definição. | Relatório I50 e matrizes locais | **Achado disponível; redação pendente** |
| TCC-MOD-006 | Resultados e limitações | Relatar e contextualizar a divergência da edição federal SIM 2024 com fonte estadual preliminar. | PEN-004 | **Pendente de conciliação** |
| TCC-MOD-007 | Métodos e resultados | **Incluir obrigatoriamente análise por sexo e idade**, após validação dos denominadores e cruzamentos; indicar lacunas de cobertura e o uso de pesos comuns para comparação padronizada por sexo. | MET-002, MET-008, PEN-001 | Homologado, implementado e validado nos dados, redação pendente. |
| TCC-MOD-008 | Métodos assistenciais | Revisar unidades e denominadores após SIH/SIA/CNES/SIGTAP, incluindo competência, origem/destino, cobertura territorial, classificação histórica. | PEN-006 e lotes futuros | Indicadores assistenciais calculados, com cobertura indicada por competência. Redação pendente. |
| TCC-MOD-009 | Limitações e interpretação | Analisar idosos, idade ignorada, sensibilidade aos pesos e limitação de terminal 80+. | MET-003, PEN-003 | **Aprovada; redação pendente** |
| TCC-MOD-010 | Resultados, figuras e discussão | Exibir séries comparáveis e confrontar Norte com ES total de forma descritiva; quando necessário, produzir comparador ES sem Norte. | PEN-008 | **Pendente de redação** |
| TCC-MOD-011 | Metodologia, resultados e discussão | Apresentar Censo 2022 como padrão principal, estimativas anuais como denominadores e o padrão 2010 como análise de sensibilidade. | MET-004, PEN-002, confronto_2010.csv | Homologado, implementado e validado, pendente no TCC. |
| TCC-MOD-012 | Métodos e resultados | Explicitar as quatro regiões fixas para todas as análises regionais e o aprofundamento exclusivo da Região Norte no TCC; diferenciar da política institucional de quatro regiões em equilíbrio. | MET-005 | **Homologada; redação pendente** |
| TCC-MOD-013 | Métodos, limitações e discussão | Apresentar a comparação transversal causa original/final como protocolo institucional geral do SIM; aplicar ao TCC a análise de sensibilidade de I50, sem atribuir causa administrativa não demonstrada. | MET-006 | **Homologada; redação pendente** |

## 5. Modelo obrigatório para novas ocorrências

Para cada descoberta que altere o desenho ou o manuscrito, registrar:

- **ID, data, módulo e executor**.
- **O que o projeto/texto previa** (com trecho/localização quando o manuscrito for auditado).
- **O que a execução constatou**, com referência ao arquivo, tabela, campo, fonte oficial e hash/recibo.
- **Classificação:** decisão aprovada; limitação; discrepância; hipótese; alteração metodológica proposta; correção factual.
- **Impacto:** indicadores, comparabilidade histórica, regiões, idade, sexo, conclusões, figuras/tabelas, redação do TCC e demais módulos institucionais.
- **Alternativas e justificativa científica**, distinguindo decisão de hipótese.
- **Deliberação e responsável pela homologação**: nenhuma mudança substantiva sem decisão do orientador/responsável.
- **Ação de execução** e **evidência de validação** (código, teste, commit, arquivos de saída).
- **Ação de redação do TCC**: seção-alvo, texto necessário, figuras/tabelas a atualizar; manter `pendente` até revisão autorizada do manuscrito.
- **Status e vínculos**: `identificado`, `proposto`, `homologado`, `implementado_no_codigo`, `validado_nos_dados`, `pendente_no_TCC`, `incorporado_ao_TCC`, `descartado_com_justificativa`.

## 6. Governança e execução

1. Manter este registro na documentação do estudo, por exemplo em `docs/estudos/tcc_camila/registro_decisoes_metodologicas.md`, depois de verificar conflitos com documentos existentes; preservar histórico por Git.
2. Anexar/relacionar um ledger institucional comum para mudanças metodológicas com impacto em outros módulos do Observatório, evitando duplicar evidências entre TCC e núcleo transversal.
3. Atualizar o registro durante **ambas as etapas** do mandato integrado (TCC/assistenciais e comparabilidade transversal) sempre que surgir nova consequência metodológica.
4. Não alterar o TCC original sem autorização explícita. A conclusão de execução computacional **não** significa que uma alteração tenha sido aplicada ao manuscrito.
5. Nenhuma etapa pode ser anunciada como concluída sem reportar pendências de dados, método e texto separadamente.


## 7. Atualização obrigatória de escopo — 18/11/2026

### 7.1. Distinção: Censo, denominador e população-padrão

- **Censo 2022**. O mandato homologou a estrutura por idade do Brasil na tabela 9514. A apuração usa sexo total e forma de declaração total. As margens por sexo reconciliam por idade.
- **Denominadores 2014–2024:** utilizar estimativas populacionais oficiais **próprias de cada ano**, desagregadas por município, idade e sexo. O Ministério da Saúde/RIPSA publicou estudo 2000–2024 apoiado também no Censo 2022; inspecionar a **edição concreta** da série custodiada antes de afirmar que foi atualizada. Nunca usar a população recenseada em 2022 como denominador de 2014 ou dos demais anos.
- **Mudança de padrão:** com o Censo 2022 homologado, aplicar os **mesmos pesos por idade do Brasil** para todos os anos, regiões e comparações entre sexos; agregar 80+; recalcular as 55 taxas prematuras e as novas taxas de todas as idades. Conservar como produto histórico auditável as taxas já validadas no padrão 2010. Não justapor taxas 2010 e 2022 em um mesmo gráfico como se fossem diretamente comparáveis.
- **Estratificação por sexo:** exigência metodológica homologada para toda linha de mortalidade; realizar QA de completude e coerência dos cruzamentos. Dados ignorados devem ter contabilidade separada e não devem ser redistribuídos sem protocolo aprovado.

### 7.2. Regra territorial e institucional

- **Observatório SUS-ES:** as quatro Regiões de Saúde do PDR/ES 2024 — Norte, Central, Metropolitana e Sul — são a unidade regional comum nas análises estaduais, com codificação municipal explícita e versão. Nenhuma recebe destaque privilegiado por regra institucional. Estudos fora do ES ou em outra escala requerem contrato territorial próprio, sem impor artificialmente PDR/ES.
- **TCC da Camila:** mesmas quatro regiões, mesma atribuição retrospectiva e mesmo contrato dos 78 municípios. A **Região Norte** recebe aprofundamento adicional por decisão específica do estudo. Quando compará-la ao restante do estado, utilizar denominadores e subconjuntos não sobrepostos quando analiticamente pertinente.

### 7.3. Regra de abrangência do protocolo SIM

- Comparar `CAUSABAS_O` e `CAUSABAS` **para todas as categorias e causas elegíveis**, em todas as UFs e anos disponíveis, como função reutilizável; não limitar a I50, cardiologia ou ao TCC.
- Quando preenchidos e adequados, examinar menções no `ATESTADO` e demais campos de causas múltiplas como dimensão **separada**.
- O protocolo registra **toda discordância** individual, agregando a matriz por grupo, categoria, subcategoria, território e período; uma discrepância não constitui automaticamente erro. Investigação aprofundada para padrões epidemiologicamente relevantes, com critérios predefinidos e processo documental auditável.
- Quando `CAUSABAS_O` estiver ausente ou inválida, classificar como **não comparável**; não inferir concordância por ausência. Diferenciar variação de categoria, subcategoria e capítulo.
- Manter o campo final (`CAUSABAS`) como base das taxas convencionais; as demais medidas são complementares, com conceitos e denominadores próprios.

## 8. Referências oficiais verificadas para decisão demográfica

1. Ministério da Saúde. Dados Populacionais: seção *População municipal por sexo e idade — 2000 a 2025*, disponível em https://www.gov.br/saude/pt-br/composicao/seidigi/demas/dados-populacionais/dados-populacionais ; acessar a edição do estudo 2000–2024 efetivamente utilizada.
2. IBGE. *Censo Demográfico 2022: População por idade e sexo*, página oficial https://www.ibge.gov.br/estatisticas/sociais/populacao/22827-censo-demografico-2022.html ; consultar a Tabela SIDRA 9514 e documentação correspondente.
3. CONASEMS/RIPSA. *Rede Interagencial de Informações para a Saúde divulga estimativas populacionais dos municípios brasileiros*, 28 jan. 2025, https://portal.conasems.org.br/noticias/932_rede-interagencial-de-informacoes-para-a-saude-divulga-estimativas-populacionais-dos-municipios-brasileiros .

## Incremento de execução do mandato v3 em 18/11/2026

O registro v2 recebido tem SHA-256 ba34fd5ab66b11e7d4a103b8cf7898b8ce46266f6899280ae4e8d6b39124d585. A custódia preserva a íntegra dessa edição. As decisões transversais estão vinculadas ao ledger institucional em ../decisoes_institucionais.md. Executor dos cálculos e conferências deste incremento: Codex Local. A homologação científica dos parâmetros decorre do mandato do responsável em 18/11/2026. As localizações abaixo são seções previstas para revisão.

| ID e histórico | Evidência e deliberação | Efeito e seção pendente |
|---|---|---|
| TCC-MOD-014, desdobramento de 001/002/007/009/011 | O cruzamento antes limitado a sete anos foi completado com quatro originais POPSVS da mesma distribuição. taxas-ed2 confronta todas as margens anuais de sexo e idade por município com DEM.1.01, reproduz o padrão histórico e aplica o novo padrão aos mesmos denominadores. Homologado, implementado e validado nos dados. | Métodos, resultados, figuras e referências. Explicar universo bruto, idades ignoradas, limitação interna de 80+ e pesos comuns. Redação pendente. |
| TCC-MOD-015, desdobramento de 003/005/010/012 | A análise anterior agrupava o estado e as regiões. O comparador operacional ES sem Norte conserva o resíduo estadual com município desconhecido. A sensibilidade soma categorias mutuamente exclusivas I50, I11.0, I13.0 e I13.2 como causa final. O conjunto e as menções nas linhas A–D/II ou ATESTADO são produtos distintos. Evidências em estratos e sintese. | Métodos, mapas, legendas, resultados e discussão. A quebra classificatória e a divergência da edição estadual preliminar exigem interpretação separada. Mecanismo específico em aberto. Redação pendente. |
| TCC-MOD-016, desdobramento de 008 | O lote RD acrescenta ano clínico, competência, UF de atendimento, residência, sexo, unidade e idade do SIH. Controle do número de AIH repetido na competência, datas e balanço de registros. O volume mede AIH principal IDENT=1 com diagnóstico principal I00–I99. | Métodos e resultados assistenciais. Apresentar cobertura por competência/UF e fluxos com atratividade ou evasão observável. Para CNES, conservar a referência mensal. Para SIA usar quantidade aprovada e vigência SIGTAP. Redação e cobertura assistencial longitudinal pendentes. |

O texto deverá informar a diferença entre a vigência da atualização do SCB nas bases referentes a 2025 e o período observado na ruptura. A divergência entre a base federal e o relatório preliminar estadual permanece aberta. As implicações para a conclusão do manuscrito dependem da revisão epidemiológica.

### Reprodução do incremento

Com Python 3.12 e PYTHONPATH apontando para python, executar estratificar_sim_camila.py com manifesto e destino externo. Executar taxas_censo_camila.py com a raiz da custódia e uma versão nova de saída. Executar sintese_mortalidade_camila.py com o diretório mandato-v3 e um destino externo. A origem dos pesos é a variável 93 da tabela SIDRA 9514, Brasil, sexo total e margens por sexo, forma de declaração total, ano 2022. O JSON consultado tem SHA-256 e326cf81848da2a2517b24aaefe2a403849144a4b0ef41d812504be4975a2f15 e os metadados têm SHA-256 1d049151ee97b2f42705a7a53cead75fbe2cc6e63f528cafe548655823a6e911. Cada execução vincula os produtos aos arquivos de entrada em recibo.json.

Para lotes RD, lote_assistencial_camila.py recebe o diretório de custódia v3 e objetos identificados por família, UF e competência. assistencia_ftp_camila.py usa FTP oficial com SIZE/MDTM e mantém recibos por objeto. O leitor pyreaddbc 2.0.4 utiliza os nomes relativos no processo de decodificação para aceitar caminhos locais Unicode. Os resultados analíticos ficam na custódia.

## Incremento assistencial e transversal de 19/11/2026

| ID | Previsão e deliberação | Evidência de implementação e validação | Seção do TCC a revisar |
|---|---|---|---|
| TCC-MOD-017 | O piloto conhecia dois instantâneos SIGTAP de espelho. A distribuição primária FTP2 oferece tabelas mensais versionadas. Aplicar a edição de PA_CMP para qualificar procedimentos de cada arquivo PA_MVM. AC1 pode conter AC2. A consulta genérica depende de CBO admitido na competência. A seleção clínica dos candidatos mantém as ressalvas de D2. | sigtap_serie_camila.py, oferta_producao_camila.py e series_oferta_camila.py. Preservados os dois espelhos, originais primários, manifesto de vigência e confronto histórico. | Métodos, resultados, referências e limitações da assistência. Distinguir linha PA e quantidades aprovadas/apresentadas. Explicar estoques ST/HB/LT, equipamentos EQ, equipes EP e vínculos e horas PF. Pendente no texto. |
| TCC-MOD-018 | O contrato anterior agregava idosos e ignorados pelo leitor legado. A conversão oficial IDADE.CNV inclui menores de uma hora, unidades de idade com quantidade desconhecida e centenários até 199 anos. | Confronto célula a célula dos códigos etários observados no G0 com a tabela oficial. Resultado em controle-idade-tabdo.json. A infraestrutura comum incorpora o dicionário e o catálogo de causas pouco úteis, OBS-SIM-001. | Métodos e limitações etárias. Descrever as regras de conversão e o limite interpretativo de 80+. Validação do TCC concluída nos dados, redação pendente. |
| TCC-MOD-019 | A cobertura hospitalar de residentes fora do ES dependia dos arquivos das UFs de atendimento. O inventário identifica as partes efetivamente esperadas e a integralidade por competência. | consolidar_sih_camila.py, cobertura.csv e serie.csv. Novembro de 2024 no ES reutiliza o checkpoint regional anterior. Os produtos de idade, sexo e atração dependem do grau de detalhe disponível. | Métodos, tabelas de assistência e conclusão. Expor a diferença entre cobertura estadual e nacional, competências com evasão mensurável e natureza ecológica dos contrastes com oferta e mortalidade. Pendente no texto. |

Os novos recortes assistenciais medem registros, quantidades e estoques mensais. Relações entre mortalidade, oferta e produção exigem interpretação ecológica. Datas de cadastro de equipes, vínculo SUS, código de leito ou carga horária têm significado próprio e devem acompanhar os resultados apresentados.

### Sensibilidade ao capítulo perinatal

TCC-MOD-020, 19/11/2026. O conjunto inicialmente apurado em G0 privilegia o capítulo circulatório. A conferência dos títulos do TABDO também identificou P29.0, insuficiência cardíaca neonatal. O indicador complementar intracomponente usa I50 e as categorias hipertensivas com insuficiência explícita. A sensibilidade entre capítulos acrescenta P29.0. I11.9 traz exclusão explícita no título. O confronto foi implementado e validado nos 11 anos em sensibilidade-neonatal, com o vetor de códigos e os títulos examinados. Métodos, tabela de sensibilidade e discussão neonatal permanecem pendentes no manuscrito. A homologação do mandato preserva G2 e o conceito de causa básica final.

### Reprodução das séries assistenciais

O inventário nacional RD parte da listagem original de ftp.datasus.gov.br/dissemin/publicos/SIHSUS/200801_/Dados. A disponibilidade por UF é verificada sobre todos os objetos da competência. O quadro por competência distingue atendimento, atração com UF plausível, residentes observados e cobertura nacional integral. Consolidar com consolidar_sih_camila.py. Os quatro pilotos regionais anteriores e o lote de novembro de 2024 são controles de reconciliação.

Para oferta e produção, as famílias EP, EQ, HB, LT, PF, ST e PA usam a distribuição por UF e competência e os recibos de assistencia_ftp_camila.py. As edições SIGTAP vêm do diretório ftp2.datasus.gov.br/pub/sistemas/tup/downloads. Conservar a listagem em fontes/sigtap-downloads.txt e executar sigtap_serie_camila.py antes de oferta_producao_camila.py. vigencia_equipes_camila.py confronta IDEQUIPE, competência, ativação, desativação e motivo. A série de equipes apresenta sensibilidade ao desligamento no próprio mês. series_oferta_camila.py e validar_series_assistenciais.py produzem cobertura, tabelas mensais e médias dos estoques nos meses observados. Manter o vínculo entre arquivo de movimento e competência de produção ao agregar PA.

### Cobertura por residência e validação final

TCC-MOD-021, 19/11/2026, desdobramento de TCC-MOD-019. A ampliação nacional por competência usa a UF de atendimento do arquivo RD e o município de residência de cada AIH. O leitor de projeção de residentes foi confrontado com o leitor integral nos arquivos já em custódia de RJ, MG e BA, usando exatamente as mesmas dimensões e contagens para o subconjunto residente no ES. Nos meses com 27 UFs confrontadas ao inventário, calcular o total de residentes e a evasão. Para competências com cobertura parcial, conservar o observado e deixar o indicador nacional completo ausente. Fontes de execução: sih_residencia_camila.py e consolidar_sih_camila.py. Seções de métodos, resultados assistenciais e limites de inferência pendentes de redação.

Os controles de integridade dos originais e dos lotes analíticos podem ser reproduzidos com auditar_custodia_camila_v3.py, o arquivo idade_tabdo.csv da branch institucional e um novo diretório externo. Os testes empíricos consultam as referências históricas na custódia autorizada. Os registros de oferta aprovados e a cobertura de processamento não alteram a exigência de revisão dos conceitos clínicos candidatos antes da incorporação ao manuscrito.

### Fechamento dos checkpoints em 19/11/2026

Os oito domínios de assistência ST, HB, LT, EP, EQ, PF, PA e SIGTAP foram conferidos nas 132 competências. O atendimento hospitalar no ES tem a mesma janela. A cobertura nacional de residentes foi validada para todo o ano de 2024 e para outubro de cada ano anterior, com matriz de cobertura das demais competências. Os recibos sih-final, assistencia-final e qualidade-assistencial-final documentam as unidades, as ressalvas e a extensão da evidência. Em dezembro de 2024, o estoque de leitos reutiliza o agregado do CP04.

A comparação institucional abrange as 11 bases de mortalidade geral. O módulo validou o balanço em três e quatro caracteres, a sensibilidade das menções e a regressão empírica privada de I50. O dossiê J18 incluiu uma leitura adicional das covariáveis. Para o TCC, a comparação de classificação está apta a discussão descritiva. O mecanismo da ruptura e a discrepância estadual preliminar seguem abertos. O campo de situação do manuscrito permanece pendente de revisão autorizada.
