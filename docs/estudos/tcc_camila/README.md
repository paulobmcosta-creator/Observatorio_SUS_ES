# Atenção cardiovascular especializada no Espírito Santo, 2014–2024

O módulo do TCC da Camila integra o cadastro territorial do Observatório, o perfilador institucional de DBC e a custódia de objetos. A unidade geográfica de aprofundamento é a Região Norte, contida no estado do Espírito Santo. A linha de base de software é a implementação da PR 82 no commit `cf2bf830cf964bab52bcc8c0ecb4ce40b33070a2`. O código e as provas do TCC têm ramificação própria.

## Execução offline

Usar Linux com Python 3.12, R, GNU sha256sum e Poppler (`pdftotext`). A partir da raiz do checkout, preparar um ambiente Python com as versões de NumPy, pandas, Pillow, dbfread e pyreaddbc fixadas para o estudo. A distribuição de pyreaddbc pode exigir compilador e cabeçalhos Python. A suíte institucional ampliada também usa as versões em `requirements-implementacao.txt`.

```bash
python -m venv /tmp/venv-tcc
. /tmp/venv-tcc/bin/activate
python -m pip install -r config/estudos/requirements-camila.txt
export PYTHONPATH="$PWD/python"
export PACOTES=/dados/entrada
export ACERVO=/dados/tcc/acervo
export PROVAS=/dados/tcc/execucao-01
python -m observatorio_sus.estudos.camila.pacotes "$PACOTES" "$ACERVO"
Rscript tests/test_configuracao_dossies.R
python -m unittest discover -s tests/python -p 'test_camila*.py' -v
python scripts/verificar_pilotos_camila.py "$ACERVO" "$PROVAS"
python scripts/diagnosticar_ruptura_i50.py "$ACERVO" /dados/tcc/i50-v1 --custodia /dados/custodia
```

O importador procura um exemplar por nome e SHA dos quatro checkpoints, dos dois volumes e do manifesto de divisão. Confere domínio de caminhos, duplicação, bytes, CRC durante leitura, hashes por membro e inventário do consolidado em CP02. Os dois volumes preservam 113 caminhos. O hash histórico do ZIP único de 34.726.374 bytes é `52649590f52581b2150af7ea239a12112f6f80dcc00e3dba83cf2073fb0b3a14`. A conferência direta recaiu sobre os dois volumes e seus membros.

Cada processamento escreve em staging externo, registra hashes de entradas, método, parâmetros, controles e saídas. O mesmo comando reutiliza a edição íntegra. Uma edição diferente exige outro destino. A prova integrada exige um diretório novo para confrontar baselines, testar idempotência e injetar uma falha sem atingir o lote positivo. Um staging com falha ou interrupção permanece fora do caminho promovido. Em caso de queda com `escritor.lock`, inspecionar o proprietário do lock antes de retomar. O diagnóstico I50 pode ser repetido em novo destino quando a custódia receber originais. O fato de um arquivo estar ausente em uma raiz local só descreve aquela busca.

Os dois produtos de inspeção permitem localizar cada código do Work e rastrear seu uso. A inspeção abriu os 113 membros diretamente, incluindo os 89 anteriormente conhecidos apenas por inventário. Abrange documentos Word e PDF, tabelas e dicionários, código, imagens, registros JSON, cabeçalhos DBC e membros/CRC dos ZIPs internos. Os quatro RD, os sete POPSBR e os dois SIGTAP passaram também por leitura de seus registros. Os textos de orientação, incluindo a proposta histórica de Noroeste 1, permanecem identificados no inventário. [Inspeção dos 113 membros](inspecao_consolidado.csv) · [Matriz dos 38 arquivos de código](migracao_scripts.csv)

## Território e população

A CIB/SUS-ES 259/2024 foi aberta e conferida em 18/11/2026. O Anexo III, páginas 6 a 9, relaciona 15 municípios na Central, 14 na Norte, 23 na Metropolitana e 26 na Sul. A correspondência aceita a grafia “Divino São Lourenço” no ato e “Divino de São Lourenço” no cadastro. Confere as 78 chaves de seis e sete posições, seus dígitos verificadores, unicidade e Mantenópolis na Central. Os municípios anteriormente designados Noroeste 1 permanecem entre os 78. [Resolução CIB/SUS-ES 259/2024](https://e-docs.es.gov.br/d/2024-L5WDBB)

O instantâneo identificado como `PDR_ES_2024_CIB259_TCC_v1` usa 20/12/2024 como data documental de classificação. O intervalo de um dia no CSV canônico identifica o corte usado pelo modo retrospectivo. A data do evento permanece disponível para análise de 2014 a 2024. Os outros estudos conservam seus modos de regionalização. A versão adaptada tem SHA `681c0031cf830dffdaa18085bddffba472c7c07e8cc1ce85e5f2c5a7cbfd692e`, a correspondência CP01 tem SHA `4eaa33867efdc1c7197f64d5fbbbb04618f13028f6ab9a572e557afff67352d1` e o PDF tem SHA `cc4dedb5dba7bdb18d6ac60c200426fe3a1e1ad031ab8c4ebceba0099d631896`. A transformação é reproduzível em outro destino.

```bash
python -m observatorio_sus.estudos.camila.territorio \
  "$ACERVO/CP01/Territorio/TERRITORIO_FIXO_PDR_ES_2024.csv" \
  "$ACERVO/consolidado/Referencias/CIB_259_2024.pdf" /tmp/cadastro-tcc.csv
cmp /tmp/cadastro-tcc.csv metadata/territorio/pdr_es_2024_tcc_v1.csv
```

Para cada um dos 858 pares município/ano, DEM.1.01 exige uma célula de total, duas de sexo e 81 de idade, de 0 a 80+. O total deve coincidir exatamente com cada soma marginal. Sete anos têm POPSVS original (2016 e 2018–2023), com 88.452 chaves de município, sexo e idade. A conferência compara 45.864 margens. Os demais quatro anos participam das taxas brutas pelo denominador total validado. A distribuição conjunta de idade e sexo nesses quatro anos continua indisponível. DEM.1.01 entrou como extrato municipal do CP03. Sua extração desde o arquivo nacional de 140.675.784 bytes continua documentada pelo Work.

Para cada território, soma-se primeiro a população dos municípios. A taxa bruta é 100.000 vezes a razão entre óbitos e população do mesmo universo. As tabelas usam seis casas decimais. Nos oito quinquênios de 30–69, o peso é a população do estrato no Brasil/Censo 2010 dividida pela população do padrão nesse intervalo. A taxa direta é a soma das taxas específicas multiplicadas pelos pesos. Os 330 registros brutos cobrem 11 anos, cinco territórios e seis grupos. Há 55 posições para a mortalidade prematura G0. Dez padronizadas foram recalculadas do cubo CP02 de 2023/24, 30 carregam a padronização legada e 15 dependem dos numeradores etários de 2014, 2015 e 2017. A padronização geral aguarda denominadores separados de 80–84 e 85+.

## SIM e investigação da ruptura I50

O denominador territorial do SIM segue residência. A seleção usa não fetais (`TIPOBITO=2`), data válida no ano de ocorrência do óbito e causa básica `CAUSABAS`. G0 abrange I00–I99. G1 é I20–I25, G2 é I50, G3 é I60–I69, G4 é I10–I15 e G5 é I70–I79. Os grupos selecionados cobrem parte de G0. O total ES inclui prefixo de residência 32 com município desconhecido, registrado em categoria residual. Uma residência sem identificação de UF fica fora desse total. As saídas do diagnóstico mantêm o município de origem e a categoria residual.

Os leitores CSV e pandas verificam o conteúdo do único membro da edição anual. Removem espaços externos, aceitam caixa baixa e o ponto na posição de separação da subcategoria. Distinguem I50, I500, I501, I509, demais sufixos observados, campo vazio e sintaxe inválida. A aceitação lexical de um sufixo exige posterior interpretação no domínio clínico aplicável. A rotina também mede quantos registros entrariam em I50 pela retirada irrestrita de pontos usada no código legado. Reconcilia as duas leituras por mês, idade quinquenal, município, região e causa, além de exclusões por data, ano e elegibilidade. O arquivo é esparso. Inferir zero em um estrato exige cobertura comprovada daquela edição. Idades e municípios ignorados conservam categorias próprias.

O comando de investigação procura por bytes e SHA com prioridade para 2022. Para o que localizar, produz os cubos privados dos dois leitores, QA, cabeçalho observado, hashes, recibo e comparação com o agregado de referência. Para cada original ausente, emite uma linha com o nome esperado, a identidade do ZIP e a contagem de referência, deixando o campo de resultado do original vazio. É possível executar e verificar uma edição separadamente.

```bash
python -m observatorio_sus.estudos.camila.sim 2022 /dados/custodia/SIM2022.zip /dados/tcc/sim-2022 --conferir
```

A conferência segue a mesma edição e filtros. O aceite da explicação da ruptura exige reconciliar definição, edição federal, datas de atualização e comparador estadual. O rótulo de paridade preservado nas taxas CP02 refere-se à execução documentada pelo Work. A busca desta implementação encontrou apenas agregados e intermediários para SIM em 2022–24. [Edições, membros, bytes e SHA](../../../config/estudos/edicoes_sim_camila.csv)

## SIH, CNES e SIA

No SIH, cada observação elegível é uma linha de AIH ativa por competência de processamento, `DIAG_PRINC` I00–I99 e `IDENT=1` no piloto. O script conserva o perfil de IDENT, repetições de N_AIH, datas inválidas e ano da admissão. Mantém em camada privada os municípios de residência e atendimento e o fluxo por região. A tabela detalhada distingue as categorias de outra UF com código plausível, município ES ausente do mapa e origem indeterminada. A tabela de cobertura contém as 132 competências e distingue zero observado, valor positivo e falta de cobertura para cada filtro. O perfil padrão reproduz a matriz histórica e a produção das quatro competências com DBC (201401, 201412, 202401, 202412). A quinta, 202411, dispõe de recibo e balanço dos derivados CP04. A evasão para fora do ES exige cobertura de atendimentos de residentes nas outras UFs. Os filtros de análise de sensibilidade podem ser passados em `assistencia --ident 5 --cid-min I20 --cid-max I25`, em um destino novo.

No CNES 202412, a junção por CNES e competência confronta município em HB e ST, vínculo SUS, habilitações, vigência e duplicidade. O perfilador também registra os marcadores DBF. A auditoria de interoperabilidade identificou um byte diferente no terminador do cabeçalho ST (deslocamento 6688, 00 no Work e 0D no institucional). Os registros coincidiram. Os dois caminhos de decodificação compartilham ancestralidade em blast. O estoque médio usa somente os meses válidos de uma medida no mesmo ano e informa quantos participaram, mínimo, máximo, última competência, valor final e meses ativos. HB/ST cobre um único mês. O piloto LT dispõe de derivados conciliáveis por tipo/código/campo. Sua interpretação cardiovascular requer classificação histórica. O contrato permanece aberto para as demais famílias e competências.

O transporte `envelope_datasus` integra a entrada institucional `scripts/adquirir_lote_controlado.py`. Usa `uf[]`, ano, mês, família e fonte, exige URI lógica compatível com o catálogo e o pedido oficial de empacotamento. Registra URL efetiva HTTPS, revisão, tamanho e SHA do envelope, membro, CRC e SHA do conteúdo. Para um lote novo, declarar no plano `limite_envelope_bytes` dentro de `limite_temporarios_bytes`, o inventário explícito por parte, os limites por objeto e os caminhos externos do contrato institucional. A execução padrão faz preflight, e a opção `--adquirir` inicia a transferência. Nesta entrega foram executados o replay de catálogos e o teste do adaptador com bytes sintéticos. Os 503 anteriores em PA/ES, EQ/ES e RD/RJ indicam falhas de transporte.

Os dois ZIP SIGTAP do consolidado (202401 e 202412) vieram do espelho identificado no inventário. O leitor confronta largura fixa, competência mensal de cada linha, tabela de procedimentos, relação procedimento–ocupação e conjunto AC1 com o controle do Work. AC2 está contida em AC1. Para SIA-PA, a regra testada usa `PA_CMP`, `PA_PROC_ID`, `PA_CBOCOD`, `PA_QTDAPR` e conserva `PA_QTDPRO`. O procedimento de consulta genérica exige CBO pertinente aprovado para o recorte e relação válida na mesma competência. Os candidatos 225120, 225210 e 225203 permanecem para revisão semântica. A apuração real de produção depende do PA, de edição SIGTAP de origem oficial confirmada e da seleção histórica aprovada. Esforço e repouso permanecem componentes distintos.

## Aceite e continuidade

| Componente | Prova reproduzível | Alcance ou dependência |
|---|---|---|
| Custódia e território | Recibo de importação, inventário dos 113 membros e teste R de 78 × 11 | Classificação fixa do estudo |
| População e mortalidade | Regressores positivo e negativo, 15 comparações de CSV no conjunto dos pilotos | Taxas calculadas a partir do nível de entrada identificado para cada ano |
| SIM/I50 | Dois leitores com SHA por edição, layout, causas e chaves | Recuperar primeiro os originais 2022–24 e investigar a divergência externa de 2024 |
| CNES e SIH | Seis DBC, cinco CSV reproduzidos do CP02, recibos e balanços CP04 | Recuperar LT/RD por hash e expandir competências e UFs para as perguntas elegíveis |
| SIA/SIGTAP | Conferência mensal de dois arquivos de espelho, consulta de catálogo e teste de quantidade/CBO | Verificar origem primária e adquirir os PA faltantes por lote |
| Divulgação | Código, parâmetros, hashes e testes disponíveis para revisão | Séries, microdados e células pequenas ficam na camada analítica autorizada; divulgação requer decisão própria |

Para retomar, manter a edição validada e criar um novo lote quando mudar uma entrada, revisão do método, população padrão ou contrato territorial. O recibo acompanha os derivados. A reprodução por um segundo operador pode partir de um checkout limpo do commit informado, ambiente fixado e originais com os hashes declarados. Comparar `regressoes.json` e os hashes dos CSV, preservando os logs de eventuais divergências. A execução automatizada em outra máquina de CI usa os contratos públicos e dados de teste. A reprodução empírica independente por outra equipe depende de acesso autorizado aos insumos.

### Aquisição anual direta e comparação com os checkpoints

Em um ambiente com acesso HTTPS ao endereço federal registrado em `edicoes_sim_camila.csv`, os comandos abaixo buscam cópias locais por tamanho e SHA-256 antes do GET. A transferência usa o cliente HTTPS institucional com revisão por HEAD, limite individual de bytes e promoção após verificação do hash e do membro ZIP. Preservar os diretórios de recibos e os originais em custódia externa. O domínio exigido pelas 11 edições é `s3.sa-east-1.amazonaws.com`. Uma recusa na abertura do túnel pelo proxy deixa o resultado da leitura do original em aberto.

```bash
export PYTHONPATH="$PWD/python"
export RAIZ_SIM=/dados/tcc/continuacao_sim
export ACERVO=/dados/tcc/acervo
python scripts/obter_edicoes_sim_camila.py "$RAIZ_SIM/custodia" --custodia /dados --anos 2022 2023 2024 --adquirir
python scripts/confrontar_sim_camila.py "$ACERVO" "$RAIZ_SIM/comparacao-2022-24-v1" --custodia /dados --anos 2022 2023 2024
python scripts/obter_edicoes_sim_camila.py "$RAIZ_SIM/custodia" --custodia /dados --anos 2014 2015 2016 2017 2018 2019 2020 2021 --adquirir
python scripts/confrontar_sim_camila.py "$ACERVO" "$RAIZ_SIM/comparacao-2014-21-v1" --custodia /dados --anos 2014 2015 2016 2017 2018 2019 2020 2021
```

A aquisição devolve código 1 quando há impedimento. Cada ano tem um manifesto próprio. A comparação pode ser executada sobre os materiais já disponíveis. O recibo informa quantos originais foram relidos e quantos pares efetivamente puderam ser comparados. Depois que a custódia receber novas edições, usar outro destino de comparação. As semânticas das saídas são as seguintes.

- `cobertura.csv` identifica a fonte mais detalhada para cada ano e a disponibilidade de mês, município, subcategoria, região e idade. A ausência de suporte deixa as células de resultado original vazias.
- `confronto_anual.csv` preserva as contagens do consolidado e do CP02. As colunas seguintes mostram, quando disponíveis, a reconstrução desde o cubo CP02, a leitura do original, os desvios de contagem e a taxa bruta frente ao CP03.
- `qa.csv`, `edicoes.csv` e `regra_historica_divulgacao.csv` permitem verificar filtros, hashes dos membros entre etapas e a regra histórica que retinha um grupo inteiro quando uma das regiões tinha de 1 a 9 óbitos. As contagens analíticas são conservadas.
- `i50_por_idade.csv` detalha G0 e I50 por região e quinquênio, com o resíduo estadual explícito. Para cada ZIP presente, o subdiretório do ano conserva as leituras independentes por mês, município, região, faixa etária e causa básica normalizada. A coluna de diferença por idade exige ambas as fontes.
- `prematura_desde_original.csv` recebe linhas apenas para anos com dupla leitura do ZIP. Aplica os denominadores e pesos da edição já conferida no P0, incluindo a renormalização do padrão entre 30 e 69 anos. As diferenças com as taxas e contagens anteriores ficam disponíveis nos arquivos privados.

O SHA registrado pelo Work permite identificar a edição exata. ETags e datas de atualização ajudam a rastrear a distribuição. Uma análise do efeito de revisões de um mesmo ano exigiria duas edições distintas desse ano.

A comparação nacional de I50, as matrizes de causas e a reconstituição histórica têm comandos próprios. [Protocolo de investigação e reprodução](investigacao_i50.md)
