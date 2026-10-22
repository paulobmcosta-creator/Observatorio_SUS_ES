# Continuidade atual — reconciliação e avaliação de ferramentas, 22/10/2026

Branch `feat/ciclo-2026-2027-transicao`; commit-base `6478f93a50d03270a78959730221f2ea5a643658`. O diff local contém as rodadas 1–3, a reconciliação e a avaliação de ferramentas; não houve commit, merge, publicação nem alteração no relatório 2025–2026. Não reiniciar o inventário nem desfazer trabalho anterior.

## Ponto exato de retomada

1. Ler a [avaliação de ferramentas e PoC](avaliacao_ferramentas_2026-10-22.md), a [matriz de decisão](matriz_decisao_ferramentas.csv), a [cobertura por família](cobertura_ferramentas_por_familia.csv) e o [registro de reconciliação](reconciliacao_dossies.md), a [matriz de impacto](matriz_impacto_dossies.csv) e o [plano único atualizado](tarefas_operacionais.csv).
2. Retomar **T01/R06/R18**: obter os documentos oficiais citados no D2 (PDR ES 2024 e documentação territorial SESA 003/2026), conferir municípios/versão e referência temporal, confirmar Noroeste 1 como focal dentro de Norte e congelar a tabela central por hash. Selecionar a fonte populacional harmonizada e obter separadamente o padrão Brasil 2010. Não inferir municípios, pesos, versões ou vigências.
3. Em paralelo, **R08/R19/R17**: retomar um LT/ES/202401 oficial com hash e dois leitores quando houver acesso autorizado; ST/CO_UNIDADE exige contrato próprio. Não repetir sondagens recusadas sem mudança de acesso. A serialização PyArrow já validada pode ser reutilizada; a aquisição histórica ainda precisa de prova. Em seguida, verificar cobertura e layout por família, incluindo condições dos fluxos interestaduais, e inspecionar um pacote histórico SIGTAP antes de planejar aquisição ampla. Reutilizar infraestrutura comum; Python é preferencial em engenharia quando validado, com R/paridade preservados.
4. Aplicar o perfil do TCC apenas ao módulo cardiovascular. 2014–2024, G0–G5, classificação retrospectiva, quatro regiões e padronização estão decididos; não pedir nova confirmação dessas escolhas. IAM, whitelists históricas, população, composição focal, qualidade/publicação e ética permanecem pendentes no escopo identificado. IAM não bloqueia cálculos G0–G5 cujos próprios requisitos estejam satisfeitos.
5. Antes de calcular, preencher os pins vazios em `config/estudos/tcc_cardiovascular.csv` com fontes verificadas. `metadata/territorio/correspondencia_municipio_regiao_v2.csv` é somente cabeçalho. Os 77 candidatos/itens do Apêndice A não habilitam seleção final.

**DataHub identificado e avaliado:** o usuário forneceu `https://github.com/rafa-trindade/kaggle-datahub` (DataHub Brasil, Rafael Trindade). Ler a [complementação](avaliacao_datahub_2026-10-22.md), pin `60aa9cbd82509e0595d5c99ec74794e6be1588bd`. Seis casos locais: CSV de referência R 12.548×18 preservado integralmente; riscos de partes PA, coluna nova perdida, manifesto por tamanho e descarte tolerante demonstrados com sintéticos. Download de microdados Kaggle/oficiais e equivalência metodológica do corpus não demonstrados. Manter como alternativa condicionada e catálogo de referência; não adotar pipeline completo nem suas saídas correntes como histórico CNES, denominador estratificado ou território congelado. A identidade está resolvida; o próximo incremento continua LT/ES/202401 oficial conforme R08/R19.

## O que pode ser reutilizado

- Cache gzip verificado e fonte histórica; chaves operacionais/públicas separadas; schema e fixtures corrigidos.
- Preparadores com interrupção antes de descarte de duplicatas/chaves ausentes; não foi implementada deduplicação física presumida.
- Reprocessamento isolado `reconciliacao_dossies_20261022`: 115 verificações aprovadas; CSV de estabelecimentos/habilitações idênticos aos da rodada 2 por SHA-256. Totais 12.548/1.963; 501 selecionados = 304 status interno validado + 197 revisar.
- Inventário territorial/fila/fichas da rodada 3 continuam diagnósticos válidos; não equivalem a regionalização ou normas validadas.
- Novo aplicador central com papel explícito, versão/hash e distinção entre data de evento e classificação congelada. Validação com dados sintéticos não comprova tabela oficial.
- Configuração institucional e perfil cardiovascular separados; grupos, famílias e exclusões transcritos; [21 pendências](pendencias_dossies.csv) vinculadas às tarefas.
- 16 scripts de teste R passando localmente (R 4.5.0). CI remoto R 4.3 não executado. Python 3.12.14/PySUS 2.0.4/PyArrow 19.0.1 observados, sem atualização de versão.

- PoC `avaliacao_ferramentas/poc_20261022_v2`: CSV nacional 602.160×56 convertido integralmente para Parquet; restituição e preparadores R produziram campos/ordem/valores idênticos aos 12.548/1.963 da reconciliação; 115 verificações. DuckDB conferiu oito medidas, inclusive 1.297 zeros iniciais.
- DBC sintético PySUS/pyreaddbc conserva léxico e códigos, mas não equivale à interpretação R de ausentes. `parse=False` evita coerção municipal na leitura Parquet; não recupera campos perdidos no espelho. Não promover para DBC real ou série histórica sem novo ensaio.
- 55 testes Python aprovados localmente; workflow de serialização acrescentado, CI remoto não executado.
- PySUS 2.0.4 mantido; HEAD 2.11.7 somente inspecionado. pyreaddbc 2.0.4 instalado isoladamente em cache; ambiente base preservado.

## Bloqueios precisos

A rede continua sem `saude.es.gov.br`, `cnes.datasus.gov.br`, `bvsms.saude.gov.br` e `servicodados.ibge.gov.br`. As recusas estão documentadas na rodada 3; o estado do ambiente nesta reconciliação segue restrito e sem hosts personalizados. Não foi alterada a política nem repetida tentativa sem mudança de estado. Revalidar acesso após atualização legítima da configuração.

Os anexos agora fornecem decisões metodológicas e referências de busca, mas não tabelas territoriais/populacionais oficiais, pacotes históricos SIGTAP/CNES ou microdados 2014–2024. Não há resultados substantivos do TCC a apresentar ou recalcular. A [lista de recálculo](produtos_recalculo_dossies.csv) distingue reprocessamento verificado e primeiro cálculo pendente.

A versão anterior deste ponto de continuidade está preservada em `referencias/estado_pre_reconciliacao.zip`. Os logs e manifestos das rodadas anteriores não foram reescritos. Proposta PDF, dossiês originais e relatório encerrado continuam preservados; nenhuma revisão humana ou participação discente foi presumida.

A sondagem desta avaliação recusou também `nbg1.your-objectstorage.com` (catálogo espelhado PySUS) e `ftp.datasus.gov.br` por HTTPS com proxy 403. FTP direto não tentado por ausência de concessão TCP; a sondagem não prova suporte HTTPS do serviço. Ver [evidência](../../metadata/ciclo_2026_2027/avaliacao_ferramentas/aquisicao_20261022.json). Não há recálculo substantivo adicional exigido pela serialização aprovada. Backup do estado anterior desta continuidade e dos demais documentos atualizados: `referencias/estado_pre_avaliacao_ferramentas.zip`.

Complementação DataHub: extras `datasus-dbc==0.1.3` e `simpledbf==0.2.6` somente em cache isolado; base Python e R preservados. Nenhum produto analítico exige novo recálculo pela avaliação, pois o candidato não foi incorporado. Backup das dez versões documentais anteriores: `referencias/estado_pre_identificacao_datahub.zip`; [manifesto de preservação](../../metadata/ciclo_2026_2027/avaliacao_datahub/preservacao_sha256.csv). O log de busca antiga com identidade pendente permanece histórico, não representa o estado atual.
