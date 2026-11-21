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
