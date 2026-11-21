# Manual da estudante · v3.4

# Como usar o complemento quantitativo da v3.4

**Comece pela pergunta que sua tabela responde.** Para investigar a causa de morte, use as matrizes do SIM. Para descrever a estrutura de um prestador, consulte os recursos do CNES na competência. Para medir produção, escolha entre quantidade aprovada no PA e AIHs principais no RD. Para estudar deslocamentos ambulatoriais, use apenas a matriz de residência identificável.

## Mortalidade por residência e ano de ocorrência

Na tabela B01 e nas tabelas derivadas de G0, leia **7.990** como óbitos não fetais, de residentes do ES, ocorridos em 2024, com causa básica final I00–I99 no arquivo federal identificado pela nota SIM 2024. O valor inclui 13 residentes sem município classificável. O RAG 2024 informa 7.248 no corte preliminar e o RAG 2025 informa 8.062 para o mesmo ano em tabulação posterior. As diferenças de corte e a falta de consultas históricas completas impedem atribuir as diferenças a um processo específico.

Use `SIM/balanco_mensal.csv` para acompanhar a cronologia de I50 e `SIM/destinos.csv` para saber qual foi a causa final entre as declarações com I50 original. A unidade dos pares é uma declaração, contada uma vez. O conjunto das matrizes pareadas abrange as declarações com pelo menos uma das duas causas em I50. Na comparação de conceitos, o conjunto ampliado inclui I50, I11.0, I13.0 e I13.2 como causa final. A menção é a presença de I50 no atestado ou nas linhas, com uma contagem por declaração em cada definição. As quatro séries se sobrepõem.

Em 2024, seis das 436 declarações com I50 original mantiveram I50. Das 430 saídas, 266 tiveram I11.0 final e 33 tiveram I13.2 final. Três entradas completam as nove declarações com I50 final. Houve 3.040 declarações com menção no atestado. Esses valores descrevem campos diferentes da mesma fonte. Para 2022–2024, as tabelas por versão do sistema, investigação e cadastro qualificam o pareamento. O Ofício 208/2024 trata da atualização para as bases de 2025. Falta o histórico de execução que permita explicar as mudanças em cada declaração.

## Municípios e quatro Regiões de Saúde

Em 5.145 de 5.148 combinações de município, ano e grupo cardiovascular, ao menos uma das 17 faixas etárias teve zero óbitos. Esse diagnóstico pode coexistir com denominadores completos e com taxas calculáveis. Com população positiva, zero óbitos resulta em taxa específica zero. Com denominador ausente ou zero, deixe a taxa sem cálculo. Se a fonte estiver incompleta, a quantidade de eventos permanece desconhecida.

Para descrever um município, apresente os óbitos ao lado da população. A taxa bruta aplica a população total daquele lugar e ano. A taxa específica exige que óbitos e população pertençam ao mesmo estrato. A padronização direta pondera taxas etárias pelos pesos do padrão escolhido. Use o Censo 2022 como padrão principal, Censo 2010 para sensibilidade e faixa terminal 80+. O diagnóstico orienta prudência quanto à precisão. Compare longitudinalmente as quatro regiões em primeiro lugar. A Região Norte constitui o aprofundamento do TCC. Eventual agrupamento de anos, cálculo de incerteza ou suavização requer nova decisão documentada.

## Prestadores, territórios e produção

Para saber quantos prestadores tiveram recurso cadastrado e produção, abra `INTEGRACAO/E_territorios_anuais.csv.gz`, selecione ano, nível e território. O percentual usa os prestadores distintos presentes na união das fontes daquele território e ano. Para comparar os seis conceitos sem somá-los, use `seis_medidas_anuais.csv.gz`. Na Região Norte em 2024, constam 942 estabelecimentos cadastrados ao longo do ano, 313 com vínculo SUS em algum mês, 57 com recurso selecionado, 28 com produção específica no PA e 11 com AIHs cardiovasculares. Sete apresentaram produção nos dois sistemas. Um estabelecimento pode integrar várias colunas.

A matriz A conserva quantidade apresentada, quantidade específica aprovada e contextual. B usa AIHs principais com diagnóstico circulatório de prestadores do ES, incluindo residentes de outras UFs. A competência do RD é o processamento. O ano de admissão está no detalhe. Para moradores do ES atendidos fora, use os fluxos hospitalares nacionais preservados em T28. A classificação de C é mensal, enquanto E identifica atividade observada em qualquer mês do ano. D distingue entrada observada, permanência e saída mensal de cadastro. A primeira observação é o limite inicial da série. Um vínculo, leito, equipamento ou serviço é um atributo cadastral. A abertura ou continuidade operacional depende de outra fonte.

## Duas janelas do SIA e um cenário de sobreposição

A referência conserva os movimentos até dezembro de 2024. A sensibilidade examina os 12 movimentos seguintes dos prestadores do ES, mantendo PA_CMP em 2024. O campo PA_QTDPRO mede quantidade apresentada e PA_QTDAPR mede quantidade aprovada. Em 2024, a referência específica registra 380.188 e a janela estendida, 381.034. O cenário que maximiza a sobreposição de assinaturas idênticas resulta em 381.032. Duas unidades de ECG apresentam correspondência exata entre janelas após exclusão de PA_MVM. Esse teste pode reconhecer coincidências documentais. Ele não resolve retificações com campos alterados nem separa atendimentos clinicamente distintos de bytes coincidentes. Leia os cenários como quantidades observáveis em janelas de processamento.

A classe A reúne os códigos específicos historicamente elegíveis. A classe B conserva Doppler vascular e consulta especializada por CBO em grupos próprios, com os códigos no detalhe. A soma das quantidades expressa procedimentos. Uma pessoa pode receber vários. A densidade pelo local do prestador usa a população do território e admite atendimento de não residentes.

## Origem e destino no SIA

Na janela original de 2014–2024, apenas 494.726 dos 2.840.730 procedimentos específicos aprovados têm município de residência identificável e válido segundo o protocolo (17,42%). A matriz de fluxo utiliza esse subconjunto. Entre os demais, 2.346.003 são registros consolidados e uma unidade tem residência inválida ou ignorada. A atribuição ao município do estabelecimento, comum no BPA-C, explica por que comparar diretamente os dois campos municipais geraria erro de classificação.

Selecione janela, instrumento e classe antes de somar os destinos. A produção com origem declarada fora do estado pode aparecer na matriz porque o prestador fica no ES. Atendimentos ambulatoriais de residentes capixabas realizados fora do estado estão fora da cobertura desta fonte. Um pedido posterior pode ampliar prestadores de destino, avaliar mudanças no preenchimento ou examinar uma série de código específico. Documente o novo universo antes de comparar os resultados.


---

# Manual da estudante · edição v3.3.1

## Limites de interpretação dos indicadores do TCC da Camila — 2014–2024

Antes de comparar dois valores, anote a tabela, a coluna, o ano, o território, a unidade, o numerador e o denominador.

| Quando a pergunta for sobre… | Leia assim |
|---|---|
| Óbitos de residentes | No SIM, o ano é o de ocorrência. G0 abrange a causa básica final I00–I99. Use a mesma definição de causa e a mesma população nas comparações. Para 2024, cite a edição federal usada no TCC e identifique o corte ao mencionar o valor estadual preliminar. |
| Insuficiência cardíaca | Escolha entre I50 final, I50 original, causa final ampliada ou menção. A mesma declaração pode aparecer em mais de uma medida. A mudança de original para final está demonstrada, mas o mecanismo que a produziu continua aberto. |
| Internações e deslocamentos | O SIH conta AIHs principais no ano de processamento. Uma pessoa pode ter mais de uma AIH. Para utilização e evasão use a residência. Para atração use o local de atendimento. T04 distingue o ano de admissão. |
| Oferta e produção | No CNES, compare recursos cadastrados na mesma unidade e competência. No SIA, compare quantidades apresentadas ou aprovadas em prestadores localizados, com a mesma vigência e janela de movimento. A operação diária, a cobertura individual e a origem de cada usuário do prestador ficam indeterminadas. |
| Municípios | Comece por contagem e população. Acompanhe a taxa bruta ou a taxa no mesmo estrato. Uma faixa sem óbitos pode ter taxa zero e denominador válido. Uma célula sem denominador continua sem taxa. |
| Norte e demais regiões | Para localização territorial conhecida use ES sem Norte estrito. Em 2024, esse comparador reúne 7.037 óbitos circulatórios. O residual estadual inclui ainda 13 óbitos de residentes do ES sem município identificável e chega a 7.050. As 297 células CNES/SIA vazias no residual de T29 têm valores na linha estrita. |

**Comparações que exigem cautela.** Ao atravessar a ruptura de I50, conserve o campo da definição e mostre o pareamento antes de interpretar a tendência. Ao comparar municípios pequenos, leia as contagens e o perfil etário. Ao comparar o fim da série de PA com anos anteriores, considere que o último movimento disponível é dezembro de 2024. A justaposição de mortalidade, internações, capacidade e produção em T29 permite formular perguntas sobre territórios, mas não estabelece causalidade.

**Questões em aberto.** Para explicar a divergência federal–estadual de 2024 é preciso recuperar o corte histórico e seus filtros. Para explicar a mudança de I50 é preciso identificar a sequência de codificação ou investigação. A equipe não encontrou essa evidência nos agregados nem nos documentos oficiais examinados.

**O que a estudante pode solicitar.** Com o orientador, é possível definir uma comparação de períodos com denominadores compatíveis, solicitar margens de I50 por mês de ocorrência e investigação, ou pedir um recorte por código e instrumento de produção. A ficha de solicitação deve especificar a pergunta, o território, o período, a unidade e o ganho esperado. O aprofundamento territorial homologado é a Região Norte. A redação do manuscrito que ainda cita Noroeste 1 será revista pela estudante e pelo orientador.


**Documentação de apoio** · SIM 2024 (referência da edição de origem) · [I50](../07_DOCUMENTACAO_METODOLOGICA/nota_I50.md) · [Leitura municipal](../07_DOCUMENTACAO_METODOLOGICA/orientacao_taxas_municipais.md) · [CNES e SIA](../07_DOCUMENTACAO_METODOLOGICA/nota_CNES_SIA.md)

# Complementação v3.3

Comece com T29 para escolher domínio e território. Use T20 para reproduzir a antiga T10. Para a comparação territorial use a linha estrita em T25/T29 e confira o resíduo em T09. Na produção, leia F26–F28 junto com a vigência em T21. Para o município, examine o número de meses válidos e a tabela de estabilidade antes de comparar taxas. Em arquivos CSV.GZ, descompacte primeiro para abrir o CSV num editor de planilhas. O ponto decimal e a vírgula delimitadora seguem os arquivos de origem.

## Material de orientação herdado da edição v3.2.1

# Manual de leitura para a Camila

## Comece pela pergunta

Para estudar o que acontece com os moradores de um território, comece pelas tabelas de mortalidade e hospitalização. Para estudar o que está cadastrado ou foi produzido em um território, abra as séries de oferta e produção. Um hospital pode receber moradores de vários municípios. Cada arquivo no índice traz a definição da unidade, do lugar e do período. O CSV ao lado de cada figura contém os valores usados para desenhá-la.

1. Escolha um ano e um território na tabela T10. Leia o título de cada coluna antes de comparar números.
2. Para aprofundar um valor, siga o identificador no índice. Por exemplo, B01 permite selecionar um grupo, um sexo, uma faixa de análise e um padrão censitário.
3. Em uma figura, siga uma legenda de cada vez. Antes de comparar duas curvas, verifique a escala, o denominador e o que marca a passagem do tempo.
4. Ao importar um CSV no Excel ou no Calc, escolha UTF-8, separador vírgula e ponto decimal. Importe códigos de procedimento, CBO, município e UF como **texto** para conservar zeros iniciais.
5. Ao citar um resultado, anote o ID, os filtros, a coluna, a unidade, a fonte e a versão do recibo. Para propor outro cruzamento, faça uma cópia da ficha de solicitações na sua pasta de trabalho.

## Mortalidade e população

O SIM registra óbitos. A seleção considera óbitos não fetais, com data válida de ocorrência no ano e residência no ES. O grupo G0 reúne causas básicas finais do capítulo circulatório da CID-10, I00–I99. G1 representa doenças isquêmicas do coração (I20–I25), G2 insuficiência cardíaca (I50), G3 doenças cerebrovasculares (I60–I69), G4 doenças hipertensivas (I10–I15) e G5 doenças das artérias, arteríolas e capilares (I70–I79). Os cinco grupos cobrem parte do G0. Somar G0 aos grupos repetiria os mesmos óbitos.

Uma taxa bruta divide os óbitos pelos habitantes do mesmo lugar e ano e multiplica por 100 mil. Uma taxa específica repete a conta entre pessoas do mesmo sexo ou da mesma idade. A taxa padronizada reúne as taxas por idade com pesos comuns a todos os territórios. A população do Censo brasileiro de 2022 fornece os pesos principais. Os pesos do Censo de 2010 permitem verificar quanto a escolha do padrão altera a comparação. Os habitantes no denominador de cada ano vêm da série anual harmonizada RIPSA. Um padrão censitário e uma estimativa anual de habitantes têm funções diferentes.

As idades conhecidas formam faixas de cinco anos e terminam em 80 anos ou mais. A análise prematura restringe numeradores, populações e pesos às oito faixas entre 30 e 69 anos. Essa taxa mede óbitos por 100 mil habitantes da faixa. O total inclui os registros com sexo ignorado. Idade e sexo ignorados têm controles próprios. Uma taxa específica requer denominador correspondente. Uma célula vazia indica indisponibilidade ou cálculo inaplicável. Consulte o campo de situação para distinguir um zero observado.

O SIM oferece maneiras diferentes de examinar a insuficiência cardíaca. CAUSABAS contém a causa básica final e CAUSABAS_O guarda a original. A menção identifica I50 em qualquer linha da declaração. Uma mesma declaração pode atender aos três critérios. B03 apresenta a união das menções, as leituras do atestado e das linhas, a sensibilidade ampliada e, quando disponíveis, os movimentos de entrada, saída e retenção entre original e final. A série principal G2 usa a causa básica final. A avaliação de uma mudança de classificação exige campos emparelhados e evidência operacional. O Ofício MS nº 208/2024 situa a atualização do seletor no tratamento das bases referentes a 2025.

## Internações e fluxos

O SIH usa a Autorização de Internação Hospitalar. A seleção considera AIHs principais ativas, IDENT igual a 1 e diagnóstico principal I00–I99. Uma pessoa pode gerar mais de uma AIH. Os arquivos nacionais das 27 UFs permitem observar residentes do ES atendidos em outro estado. A série anual acompanha o ano de processamento. A tabela T04 permite consultar o ano de admissão dos mesmos registros.

Para obter evasão interestadual, divida as AIHs dos residentes atendidos fora do ES pelas AIHs de residentes em qualquer UF. Para atração, divida as AIHs atendidas no ES com residência plausível em outra UF pelo total de AIHs atendidas no ES. Um deslocamento entre duas regiões capixabas pertence ao fluxo inter-regional. Na matriz, a linha identifica a residência e a coluna identifica o atendimento. A diagonal conta atendimentos na própria região. Procure o resíduo de origem ou destino indeterminado antes de fechar qualquer balanço.

## Cadastro, força de trabalho e território

O CNES descreve o que os estabelecimentos registraram em cada competência. ST identifica estabelecimentos e vínculo cadastral SUS. SR identifica serviços e suas classificações. HB identifica habilitações vigentes. LT registra leitos existentes e destinados ao SUS. EQ distingue equipamento existente, em uso e marcado SUS. PF descreve registros de vínculos e cargas horárias por ocupação. Uma pessoa pode ter vários vínculos. EP identifica equipes ativas ao fim do mês com datas e identificador compatíveis. A série geral das equipes é contextual.

Em T05, escolha uma única medida pelo identificador e leia a unidade no dicionário. Para comparar anos, use a média dos estoques mensais e confira a coluna de meses válidos. Uma soma de doze estoques repetiria recursos presentes em vários meses. Uma habilitação permite estudar a organização cadastrada da rede. Para estudar utilização observada, procure os registros de produção ou as AIHs.

As quatro Regiões de Saúde são Central, Metropolitana, Norte e Sul. A mesma composição municipal do PDR/ES 2024 vale para toda a série. O recorte adicional do TCC é a Região Norte. O total ES contém a Norte. Para comparar grupos sem essa sobreposição, utilize Norte e ES sem Norte, onde calculados. No SIM, o comparador conserva o resíduo estadual sem município identificado. Os mapas municipais de mortalidade usam residência. Os de oferta e produção usam a localização do estabelecimento.

## Produção ambulatorial e SIGTAP

O SIA/PA registra quantidades apresentadas e aprovadas de procedimentos. Um mesmo usuário pode realizar vários procedimentos. PA_CMP identifica a competência de produção e PA_MVM a de movimento. O SIGTAP mensal indica vigência, modalidades e instrumentos admitidos. A classificação usa o procedimento e o instrumento efetivo do registro. P e S em PA identificam APAC principal e secundária. Uma regra exclusivamente APAC sem evidência de produção coberta exige consulta à fonte correspondente. Nesse caso, preserve a lacuna.

O total específico soma quantidades elegíveis em oito exames cardíacos nominados e três procedimentos fisioterapêuticos cardiovasculares (0302040030, 0302040048 e 0302040064). As cintilografias em repouso e sob estresse conservam códigos e séries independentes. Para recuperar cada código, consulte o catálogo. Leia os subtotais de exames e fisioterapia em separado antes de usar a soma. Dezembro de 2024 está no limite da janela de movimentos disponíveis. Produção informada depois desse limite pode faltar nas séries por PA_CMP.

O Doppler vascular é um indicador contextual da produção vascular. A consulta especializada é contextual e requer um CBO do recorte (225120, 225210 ou 225203) com compatibilidade histórica no SIGTAP. O CBO informa a ocupação do executante. O motivo clínico individual permanece desconhecido. Os dois recortes ficam fora do total específico. As intervenções AC, a fisioterapia vascular periférica e a reabilitação pós-COVID permanecem sob revisão clínica. O arquivo de situações de uso identifica outras limitações, inclusive a continuidade histórica de códigos de terapia intensiva.

## Como relacionar os cinco sistemas

Acompanhe um território em T10 e consulte as séries individuais antes de formular uma pergunta conjunta. O óbito tem ano de ocorrência, a AIH tem admissão e processamento, o estabelecimento tem competência cadastral e o procedimento tem produção, movimento e edição do SIGTAP. Os cinco sistemas permitem descrever dimensões diferentes da atenção. As agregações por território não acompanham a trajetória de uma pessoa e não demonstram o efeito de um serviço sobre um óbito. A leitura, a seleção dos resultados e a discussão científica cabem à estudante.


## Como ler a edição corretiva

Em F11, o código 116 identifica o serviço de atenção cardiovascular/cardiologia. As tabelas T17 e T19 descrevem cinco outras classes. Em T17, 122/003 identifica cadastro para exame eletrocardiográfico, 122/007 para tele-ECG e 126/004 para fisioterapia cardiovascular e pneumo-funcional em conjunto. A classe 140/014 descreve o cadastro de pronto-socorro cardiovascular. Em T19, 162/005 é uma série provisória de UCO. Para verificar se os mesmos estabelecimentos aparecem em duas classes, escolha um mês, um território e um par em T18. A contagem de CNES de um período inteiro tem significado diferente do estoque de um único mês.

Presença no cadastro da competência, marcação de vínculo SUS e produção aprovada positiva são três observações distintas. O funcionamento efetivo de cada estabelecimento, incluindo abertura, continuidade de operação e disponibilidade ao longo do mês, permanece **não mensurável** com as fontes e os campos validados. O código ATIVIDAD, os atributos de atendimento e a data de atualização não demonstram esse funcionamento. Um mês sem registro de produção específica pode ter outras formas de atendimento.

Em B02, compare taxas dentro da mesma faixa conhecida de idade e sexo. Para a contagem de óbitos com idade ignorada, consulte a coluna idade_ignorada de B01. T08 apresenta a taxa bruta municipal. No catálogo histórico, use id para acompanhar a série e chave_historica para citar a definição e a edição aplicável.
