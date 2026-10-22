# DataHub Brasil: identificação, avaliação e prova local

> Complemento de planejamento: as conclusões técnicas desta avaliação permanecem no escopo ensaiado. A prioridade global foi revista no [parecer integral](parecer_revisao_integral_2026-10-22.md): SIH/RD é o primeiro percurso proposto; LT/ES/202401 continua como ensaio específico de oferta. Ver [CI remoto por commit](../../metadata/ciclo_2026_2027/revisao_integral_20261022/ci_remoto.json) para o estado posterior às execuções locais aqui registradas.


O link fornecido pelo pesquisador resolve a identidade: **[DataHub Brasil, de Rafael Trindade](https://github.com/rafa-trindade/kaggle-datahub)**. Foi examinado o commit `60aa9cbd82509e0595d5c99ec74794e6be1588bd`, de 09/10/2026, com código, documentação, licença, dependências e 25 commits recentes. A identificação veio do usuário; não foi inferida da menção sem URL em D2 §26. O [registro anterior da busca](../../metadata/ciclo_2026_2027/avaliacao_ferramentas/busca_datahub_historico.json) permanece como evidência histórica.

**Decisão:** manter como alternativa de consulta e aquisição condicionada, aproveitar o catálogo e a estratégia de partição PA mensal como referências. Não integrar o pipeline completo nem promover os Parquet Kaggle a RAW verificado nesta rodada. A PoC encontrou limites reproduzíveis de seleção de arquivos, preservação de schema e tratamento de ausentes. CNES corrente não reconstrói 2014–2024. Mantêm-se Python/PySUS como direção de engenharia sob prova por família, o adaptador PyArrow já validado e os preparadores R como referência de paridade. Não há novo cálculo sanitário nem alteração do relatório 2025–2026.

## Identidade, origem e manutenção

É um projeto de scripts de extração, conversão, armazenamento e publicação, com dois destinos declarados: [dataset principal](https://www.kaggle.com/datasets/rafatrindade/brazilian-kaggle-datahub) e [SIA-PA mensal](https://www.kaggle.com/datasets/rafatrindade/sia-producao-ambulatorial). Não é biblioteca de catálogo de metadados homônima. O utilitário `download-datasets/baixar_dataset.py` usa a API Kaggle, permite seleção de arquivos ou intervalo PA e baixa tudo quando `ARQUIVOS=[]`; não foi executado.

- **Código:** GNU GPLv3, conforme [LICENSE pinado][licenca]. Nenhum código original foi incorporado ao pipeline do Observatório; a PoC importa funções do checkout externo. Reutilização futura deve respeitar a licença.
- **Dados:** o README declara CC0 1.0 para o trabalho de curadoria/harmonização. Essa declaração não transforma o espelho em fonte oficial nem substitui condições e citações das fontes primárias.
- **Manutenção observada:** commits de outubro acrescentam armazenamento local/MinIO, novas famílias e escrita atômica. Não foi identificada versão de pacote; o commit é o pin. Nenhum conjunto de testes ou configuração de CI foi localizado na árvore examinada. Isso delimita a evidência disponível, sem medir adequação científica pela atividade no GitHub.
- **Metadados publicados no repositório:** nomes, tamanho, número de registros e atualização; não constituem manifesto de SHA-256, versão do layout e origem de cada arquivo oficial. As cópias preservadas são declarações do mantenedor, não contagens auditadas dos dados Kaggle. PA declara 12 arquivos mensais em cada ano de 2014 a 2024; isso não comprova completude por UF/parte. CNES de estabelecimentos declara 638.547 registros em outubro, universo/data diferentes dos 12.548 registros ES/202601 de referência; os totais não são diretamente comparáveis.

[Identificação e manutenção](../../metadata/ciclo_2026_2027/avaliacao_datahub/identificacao.json), [37 fontes originais com URLs permanentes e hashes](../../metadata/ciclo_2026_2027/avaliacao_datahub/fontes_originais.csv) e [histórico examinado](../../metadata/ciclo_2026_2027/avaliacao_datahub/historico_git.txt).

## Cobertura confrontada com os contratos

São capacidades declaradas/implementadas no pin, **sem inventário oficial remoto validado nesta rodada**. A [matriz por família](cobertura_ferramentas_por_familia.csv) incorpora uma coluna DataHub mantendo as exigências anteriores.

| Sistema/família | Cobertura encontrada | Consequência no Observatório |
|---|---|---|
| CNES HB/LT/PF/EQ/SR/EP | FTP: `achar_competencia_mais_recente` escolhe o máximo disponível por prefixo; processamento substitui o retrato anterior | Útil como referência de retrato corrente. Não fornece série mensal 2014–2024; nem garante mesma competência/completude de UFs entre famílias |
| CNES estabelecimentos | ZIP/CSV corrente de dados abertos do MS; não é implementação ST/DBC nem demonstra o pacote relacional completo | Não presumir equivalência a `tbEstabelecimento+rlEstabSipac`. Passagem de campos pelo SQL não prova presença de `CO_UNIDADE`; não fabricar essa chave |
| SIM DO | CID-10: consolidados nacionais `DOBR` desde 1996 e preliminares desde 2016. README também descreve CID-9 1979–1995 e outras famílias | 2014–2024 está no intervalo nominal. Separar residência/ocorrência, versão final/preliminar, campos de causa/idade e origem; não basta filtrar ano |
| SIH RD/RJ/SP | Série moderna 2008 em diante; 1992–2007 explicitamente fora do escopo | RD é candidato a consulta/ensaio posterior. Preservar residência, atendimento, AIH, diagnóstico, competência e cobertura interestadual antes de comparação |
| SIA PA | Diretórios desde 199407; saída mensal. Filtro de aquisição aceita UF+AAMM, rejeita partes com sufixo a/b | Cobertura nominal não garante todas as partes. PoC reproduz incompatibilidade entre aquisição e processamento |
| SIA demais | AM/AQ/AR/AD desde 200801; ATD/ACF desde 201406; AN até 201410; PS desde 201301; SAD desde 201211; AB até 201303; ABO desde 201304 | Intervalos são os documentados; disponibilidade efetiva e layouts não conferidos. BI não localizado como família implementada. Não substituir seleção histórica de procedimentos/APAC |
| SIGTAP | Nenhum módulo/pacote histórico identificado | R17 permanece dependente de pacote oficial por competência, relações e vigência |
| IBGE população | SIDRA tabela 6579, variável 9324; busca anos desde 2001; saída município/ano/população total | Sem idade/sexo: não atende denominadores estratificados nem padrão Brasil 2010. R18 permanece aberto |
| Macrorregião | CSV corrente do MS associado a XLS manual, códigos preenchidos até seis posições | Não é validação do PDR ES 2024/SESA 003/2026, congelamento territorial ou correspondência canônica 6↔7 dígitos. T01/R06 permanecem abertos |

O README também descreve SINASC, SINAN, CIHA, SRAG, ANS, PNS e PIB. Essa amplitude pode ajudar a descoberta institucional, mas não foi homologada operacionalmente nem acrescentada ao escopo cardiovascular. A presença de campos identificadores não autoriza junções entre sistemas sem contrato e finalidade definidos.

Fontes específicas: [CNES corrente][cnes], [SIM DO][sim], [SIA][sia], [população][pop], [território][geo].

## Limites verificáveis de engenharia

1. **RAW e revisão:** o [README][readme] declara que o histórico bruto não é persistido. A conversão remove os arquivos de trabalho. O [manifesto de aquisição][ftp] compara nome/tamanho; conteúdo revisado com mesmo tamanho pode ser ignorado. MD5 de objeto derivado para sincronização não é hash do arquivo oficial original. No PA, a margem recente descrita no README tem padrão **zero** no código (`PA_COMPETENCIAS_MARGEM`, [linha 98][pa]); reprocessamento recente não está garantido sem configuração.
2. **Partes e schema:** o [filtro SIA][sia] exige seis caracteres UF+AAMM após o prefixo, enquanto o parser de competência aceita sufixos. Na [consolidação PA][pa], campos novos são anunciados no log, mas o writer mantém o schema da primeira parte e seleciona apenas essas colunas. Ambos os comportamentos foram reproduzidos localmente.
3. **Tipagem e ausentes:** [simpledbf/patch][patch] e dbfread interpretam números/datas antes de converter a texto. Os zeros de campos caractere da fixture sobreviveram; o léxico dos campos numéricos/datas não. Leitor principal retornou o texto `nan`, fallback retornou nulo. Não tratar essa diferença como equivalência automática com `NA` do R. Registros DBF marcados como excluídos, erros de encoding e layouts reais exigem ensaio próprio.
4. **Falhas parciais:** [base_process_dbc][dbc] admite continuar após falhas; a rotina incremental registra no manifesto os arquivos presentes antes da conversão. A inspeção indica risco de contabilizar arquivo que não integrou o resultado se outros tiverem sucesso. Esse cenário não foi ensaiado: registrar como risco estático, não como perda observada em produto publicado.
5. **CSV tolerante:** o [processador CNES][csv] usa `all_varchar=true` com `ignore_errors=true`. O primeiro ajuda a preservar códigos; o segundo pode descartar linhas. O ensaio malformado comprova a possibilidade, sem alegar que o CSV oficial ou o Kaggle tenham essa perda.
6. **Versionamento SIM:** final e preliminar usam o mesmo diretório local e chaves por nome/tamanho. A origem final/preliminar precisa constar do manifesto; eventual colisão/revisão não foi validada com arquivos oficiais. Não presumir um corpus final congelado.

## Ambiente e prova de conceito

O README indica Python 3.11. `requirements.txt` fixa PyArrow 11.0.0, DuckDB 1.4.3, boto3 1.28.17, pandas 2.3.3, dbfread 2.0.7, datasus-dbc 0.1.3, simpledbf 0.2.6 e outros componentes. O ambiente do Observatório usa Python 3.12.14, Arrow 19.0.1, DuckDB 1.5.6, NumPy 1.26.4 e boto3 1.43.117. **Não foi instalada/validada a pilha completa do DataHub**, nem houve downgrade do ambiente base.

Somente `datasus-dbc==0.1.3` (metadado MIT; [distribuição](https://pypi.org/project/datasus-dbc/0.1.3/)) e `simpledbf==0.2.6` (metadado BSD; [origem](https://github.com/rnelsonchem/simpledbf)) foram instalados sem dependências em cache isolado, por serem usados pelo conversor original. Não se tornaram dependências produtivas ou alternativas automaticamente aprovadas. O aviso de ausência de PyTables refere-se a HDF, não à saída Parquet ensaiada.

O [executor local](../../scripts/executar_poc_datahub.py) exige o pin original limpo, checkout sem `.env`, hash da referência R e destinos novos. Importa funções originais e registra hashes antes/depois; não executa os programas de aquisição/publicação. Python é justificado por executar o próprio candidato, conforme D1 §§4.2–4.3. Resultados completos em [resultados.json](../../metadata/ciclo_2026_2027/avaliacao_datahub/poc_20261022/resultados.json).

| Caso | Resultado observado | O que demonstra |
|---|---|---|
| DBC sintético microdatasus, mesmos 165 bytes do ensaio PySUS | Ambos os leitores: 2 registros, `CODE=001/010`; principal produz `nan` textual e fallback nulo. Datas e números interpretados divergem do léxico RAW PySUS | Descompressão/leitura funcionam nesta fixture; exige contrato explícito de tipos/ausentes. Asserções R originais consultadas; pacote microdatasus R não executado |
| Nomes PA sintéticos | `PAES2401.dbc` aceito; `PASP2401a.dbc` e `...b.dbc` rejeitados no fetch, ambos interpretados como 202401 pelo processador | Divergência concreta no suporte a partes; não prova o conteúdo atual do dataset Kaggle |
| Revisão com mesmo tamanho | `AAAA` e `BBBB`: SHA-256 diferentes, quatro bytes; nenhum download selecionado pelo verificador com transporte simulado | Nome/tamanho não comprovam identidade; nenhuma comunicação FTP realizada |
| Duas partes PA com schemas diferentes | 2 linhas preservadas; `CAMPO_NOVO` da segunda parte ausente no Parquet | Falha de preservação estrutural na função original. Leitor e descompressor substituídos por doubles para isolar a consolidação |
| CSV da referência R ES/202601 → função DuckDB original → Parquet | **12.548×18; zero células diferentes; quatro chaves conferidas idênticas**, incluindo `co_unidade`, CNES, município e competência | Integridade deste derivado comprovada. Leitura adaptada a UTF-8/vírgula do CSV R; não é execução do main CNES/Latin-1, nem download/conversão do produto Kaggle |
| CSV sintético com 31 registros, um malformado | Configuração tolerante produz 30 linhas; modo estrito rejeita o arquivo | Risco de descarte confirmado; schema explicitado para isolar a opção. Não evidencia perda nos dados oficiais |

**Aquisição:** o código original foi obtido pelo Git; nenhum microdado oficial/Kaggle foi baixado nesta complementação. As recusas 403 de origem oficial/catálogo na avaliação anterior continuam documentadas; não foram contornadas nem repetidas. Acesso Kaggle e autenticação não foram testados. **Integridade de conversão:** parcial e discriminada nos seis casos acima. **Equivalência metodológica:** não demonstrada para corpus DataHub; a igualdade do derivado R não valida períodos, recortes, chaves ausentes ou indicadores. A paridade R da PoC anterior permanece válida em seu escopo e não foi reexecutada sem necessidade.

## Matriz de decisão e adequações

| Componente/uso | Decisão | Justificativa e condição |
|---|---|---|
| Catálogo, nomes, endereços e períodos | Reutilizar como referência de descoberta | Citar commit e validar inventário oficial esperado versus obtido; metadados declarados não são prova de cobertura |
| Utilitário de download Kaggle | Manter alternativa condicionada | Reutilizar a seleção existente se necessário; limitar arquivos, fixar versão do dataset, hash e pareamento oficial. Não desenvolver outro downloader enquanto esse uso não exigir função ausente |
| Partição PA mensal | Aproveitar desenho; adaptar somente se surgir necessidade comprovada | Ideia adequada ao volume, mas implementação examinada falha em partes/schema; não copiar o pipeline defeituoso. O Observatório ainda não exige um novo particionador |
| CSV→Parquet/DuckDB | Manter implementação existente do Observatório | Já validada com conferência integral e falha explícita; função do candidato passou na referência limpa, mas traz leitura tolerante. Evitar implementação duplicada |
| CNES corrente como série histórica TCC | Descartar esse uso | Substituição de retrato não reconstrói 2014–2024 nem `CO_UNIDADE`; preservar RAW oficial e contrato relacional |
| População total/macrorregião corrente como denominador/território do TCC | Descartar esses usos | Ausência de estratos/padrão e versão territorial exigidos. Manter fontes oficiais próprias de R18/T01 |
| Adoção integral e substituição dos componentes R | Não integrar nesta rodada | Cobertura operacional, conversão e equivalência incompletas; necessidade não demonstrada |

A [matriz geral de 13 candidatos/versões](matriz_decisao_ferramentas.csv) passa a identificar e avaliar DataHub; a [cobertura de 14 linhas](cobertura_ferramentas_por_familia.csv) ganha a coluna específica. R08/R19 e F03 foram atualizados no plano/matriz de impacto; R17, R18 e T01 não são encerrados por esse catálogo. P11 continua primeiro cálculo pendente. **Nenhum produto analítico existente exige recálculo em função desta avaliação**, pois a transformação do candidato não foi adotada.

A prioridade global vigente é a segunda revisão e, se aprovada, o percurso SIH/RD especificado no plano integral. O LT/ES/202401 antes proposto permanece ensaio de oferta em R32, com RAW preservado/hash/layout, dois leitores e comparação com referência antes de ampliar cobertura. Se houver motivo para usar um produto DataHub, fazer ensaio independente do mesmo arquivo/competência/origem, registrar versão Kaggle e comparar campos, linhas, chaves e ausentes; para arquivos/partes ausentes, recorrer ao oficial via acesso autorizado e conversores já disponíveis. Não inferir suficiência histórica a partir de um download bem-sucedido. R e a serialização validada permanecem referências.

As dez versões documentais anteriores estão em `referencias/estado_pre_identificacao_datahub.zip`. Hashes, logs e produtos das rodadas anteriores permanecem preservados. A [auditoria desta complementação](../../metadata/ciclo_2026_2027/avaliacao_datahub/preservacao_sha256.csv) distingue mudanças documentais autorizadas dos arquivos intactos; não houve alteração no relatório encerrado.

[licenca]: https://github.com/rafa-trindade/kaggle-datahub/blob/60aa9cbd82509e0595d5c99ec74794e6be1588bd/LICENSE
[readme]: https://github.com/rafa-trindade/kaggle-datahub/blob/60aa9cbd82509e0595d5c99ec74794e6be1588bd/README.md
[cnes]: https://github.com/rafa-trindade/kaggle-datahub/blob/60aa9cbd82509e0595d5c99ec74794e6be1588bd/scripts/extract/datasus/base_cnes.py#L15
[sim]: https://github.com/rafa-trindade/kaggle-datahub/blob/60aa9cbd82509e0595d5c99ec74794e6be1588bd/scripts/extract/datasus/fetch_sim_declaracao_obito_cid10.py
[sia]: https://github.com/rafa-trindade/kaggle-datahub/blob/60aa9cbd82509e0595d5c99ec74794e6be1588bd/scripts/extract/datasus/base_sia.py#L15
[pop]: https://github.com/rafa-trindade/kaggle-datahub/blob/60aa9cbd82509e0595d5c99ec74794e6be1588bd/scripts/process/ibge/process_populacao_estimada.py#L20
[geo]: https://github.com/rafa-trindade/kaggle-datahub/blob/60aa9cbd82509e0595d5c99ec74794e6be1588bd/scripts/process/dados_abertos/process_macroregiao_de_saude.py
[ftp]: https://github.com/rafa-trindade/kaggle-datahub/blob/60aa9cbd82509e0595d5c99ec74794e6be1588bd/scripts/extract/datasus/base_ftp.py#L54
[pa]: https://github.com/rafa-trindade/kaggle-datahub/blob/60aa9cbd82509e0595d5c99ec74794e6be1588bd/scripts/process/datasus/base_process_pa.py#L98
[patch]: https://github.com/rafa-trindade/kaggle-datahub/blob/60aa9cbd82509e0595d5c99ec74794e6be1588bd/scripts/common/simpledbf_patch.py
[dbc]: https://github.com/rafa-trindade/kaggle-datahub/blob/60aa9cbd82509e0595d5c99ec74794e6be1588bd/scripts/process/datasus/base_process_dbc.py#L344
[csv]: https://github.com/rafa-trindade/kaggle-datahub/blob/60aa9cbd82509e0595d5c99ec74794e6be1588bd/scripts/process/dados_abertos/process_cnes_estabelecimentos.py#L23
