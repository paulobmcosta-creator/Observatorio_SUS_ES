# Nota analítica independente — cadastro e produção cardiovascular por estabelecimento (ES, 2024)

**Finalidade:** examinar a pertinência dos denominadores da matriz CNES × SIA × SIH da entrega acadêmica v3.4 do TCC da Camila. Esta nota é um produto de conferência exploratória **não homologado como nova edição do pacote**.

## Proveniência e unidade

Fonte examinada: `ENTREGA_TCC_CAMILA_2014_2024_v3.4.zip`, especialmente `09_COMPLEMENTO_v34/INTEGRACAO/C_cadastro_producao_integrada.csv.gz`, `recursos_vigentes.csv.gz`, `servicos_e_classes.csv.gz`, `PA_detalhe_janela_original.csv.gz`, `dicionario_recursos.csv` e `08_REPRODUTIBILIDADE/v34/codigo/integrar.py`.

Unidade primária: **CNES distinto com ocorrência em pelo menos uma competência de 2024**, por critério. Os cruzamentos anuais contam o mesmo estabelecimento uma única vez por universo. Cadastro e produção podem ocorrer em meses diferentes; o arquivo CSV de acompanhamento apresenta também a coincidência por mês. `tem_pa` significa produção ambulatorial **específica homologada** aprovada no PA, não qualquer produção ambulatorial. `tem_sih` representa AIHs com diagnóstico circulatório principal em prestadores do ES no SIH, não a totalidade da produção hospitalar.

## Conjuntos de estabelecimentos e interseções no ES em 2024

| Critério cadastral | CNES distintos no ano | Desses, com PA específico em algum mês | Desses, com AIH cardiovascular em algum mês | Com PA ou SIH no ano |
|---|---:|---:|---:|---:|
| Todos os estabelecimentos cadastrados | 9.536 | 208 | 70 | 221 |
| Com vínculo SUS em algum mês | 2.092 | 208 | 70 | 221 |
| Com recurso cardiovascular segundo o algoritmo composto v3.4 | 618 | 111 | 56 | 120 |
| Serviço cardiovascular SR116, independentemente da indicação SUS | 143 | 32 | 22 | 35 |
| SR116 com indicação de atendimento ambulatorial SUS | 52 | 28 | 18 | 31 |
| Habilitação HB_0801 | 7 | 7 | 7 | 7 |
| Leitos clínicos de cardiologia LT_32 cadastrados | 29 | 12 | 15 | 15 |
| Eletrocardiógrafo com quantidade cadastrada em uso `EQ_441_QT_USO` | 692 | 172 | 67 | 183 |
| Serviço de exame eletrocardiográfico SR122/003 | 469 | 157 | 63 | 165 |

**Atenção às definições:** o indicador composto `recurso_especifico` do código v3.4 é a união de seleção por SR116, leitos LT02/LT32, habilitações selecionadas e vínculos de determinados profissionais, além de serviço SR140/014. Ele não é o universo de todos os equipamentos capazes de apoiar exames cardiovasculares; eletrocardiógrafos precisam ser verificados separadamente. O conjunto SR116 compreende diferentes classificações, inclusive modalidades que não necessariamente geram PA específico.

## Distribuição por Região de Saúde — serviço SR116 com indicação ambulatorial SUS

| Região | Com registro SR116 amb. SUS | Com PA específico observado | Com PA ou SIH cardiovascular observado |
|---|---:|---:|---:|
| Norte | 8 | 1 | 1 |
| Central | 17 | 7 | 7 |
| Metropolitana | 18 | 14 | 15 |
| Sul | 9 | 6 | 8 |
| **ES** | **52** | **28** | **31** |

Essas razões são descritivas da **coincidência entre cadastro e produção selecionada**, e não taxas de funcionamento, acesso, qualidade ou aproveitamento da capacidade. Há diferenças no tipo de serviço, vigência cadastral, universo de procedimentos, utilização dos instrumentos PA/APAC e cobertura de atendimento SUS/privado.

## Perfil dos 208 prestadores com PA cardiovascular específico em 2024

- **176** produziram eletrocardiograma (`0211020036`), dos quais **122** apresentaram somente esse código entre os procedimentos cardiovasculares específicos selecionados.
- **86** produziram pelo menos um dos demais procedimentos específicos; destes, **54** também produziram ECG e **32** não produziram ECG.
- **157** dos 208 possuíam cadastro SR122/003 (exame eletrocardiográfico) em algum mês; entre os 176 produtores de ECG, **146** tinham SR122/003.
- **172** dos 208 tinham eletrocardiógrafo com quantidade cadastrada em uso em algum mês, dos quais **159** efetivamente produziram ECG.
- **32** dos 208 tiveram SR116 em algum momento; logo **176** prestadores com produção específica não constavam no SR116 nesse ano. Isso não é incompatibilidade automática, porque vários procedimentos, sobretudo ECG, podem ocorrer fora de um serviço especializado cadastrado no SR116.
- **111** dos 208 tinham ao menos um recurso selecionado pelo algoritmo composto; **97** não tinham. Desses 97, **71** possuíam eletrocardiógrafo cadastrado em uso, excluído da definição composta do recurso.

## Inferências que não se sustentam

- A razão `208/9.536` não mede a proporção de serviços de cardiologia funcionando no estado: o denominador contém estabelecimentos de todas as naturezas e o numerador inclui produção diagnóstica de baixa complexidade em prestadores não especializados.
- A razão `32/143` não mede inatividade dos outros 111 serviços: o SR116 inclui unidades sem indicação ambulatorial SUS e modalidades que podem gerar outras produções ou nenhuma produção dos códigos selecionados.
- `28/52` descreve serviços SR116 com indicação ambulatorial SUS e PA específico observado em algum momento de 2024, mas não demonstra que os demais 24 estivessem fechados ou improdutivos.
- Para relacionar equipamento ou serviço ao atendimento, o ideal é verificar **procedimento correspondente**, além de comparar as competências de cadastro e produção, não apenas sua ocorrência no mesmo ano.
- Nenhuma das razões acima deve ser chamada de taxa de funcionamento efetivo, cobertura ou capacidade utilizada.

## Recomendações de aprofundamento

1. Produzir uma **matriz de elegibilidade por modalidade**: diagnóstico básico/ECG; ecocardiograma e outros exames; assistência especializada SR116; habilitações e internações; fisioterapia cardiovascular. Definir para cada modalidade um conjunto cadastral pertinente e os códigos/instrumentos de produção correspondentes, preservando indicadores específicos e contextuais.
2. Calcular em cada modalidade a dupla leitura: **entre cadastrados, quantos apresentaram produção observada?** e **entre produtores, quantos possuíam o registro cadastral pertinente?** Essas duas razões têm denominadores e perguntas distintos.
3. Distinguir encontro cadastral **no mesmo mês** versus presença em qualquer mês do ano. Avaliar a vigência da habilitação, serviço, equipamento e vínculo SUS na mesma competência da produção.
4. Para SR116, desagregar por **classificação histórica** e situação de atendimento SUS; para SR122/003, relacionar especificamente à produção de ECG; para leitos e habilitações, relacionar à modalidade hospitalar pertinente, sem exigir que toda AIH cardiovascular dependa de cadastro especializado.
5. Examinar os estabelecimentos com `PA sem SR116`, `SR116 sem PA`, `cadastro pertinente sem produção no recorte` e `produção sem recurso correspondente` como perfis **para qualificação documental**, não como irregularidades ou evidências conclusivas de ausência de funcionamento.
6. Repetir por 2014–2024 e quatro Regiões de Saúde após verificar a consistência temporal das classificações. A apresentação acadêmica deve priorizar poucos indicadores interpretáveis; a matriz completa pode ficar no dossiê do Observatório.

**Arquivo complementar:** `Quadro_Denominadores_CNES_SIA_SIH_2024.csv`, com 125 linhas para os universos selecionados e as cinco territorialidades (ES e quatro regiões). Valores calculados a partir das tabelas da v3.4, sem novo processamento dos arquivos DBC oficiais.
