# Reconciliação de D1/D2 com o trabalho realizado

Rodada de 22/10/2026. Dossiês v1.0 de 03/10/2026, incorporados por solicitação explícita do usuário juntamente com o prompt complementar. Branch `feat/ciclo-2026-2027-transicao`; commit-base `6478f93a50d03270a78959730221f2ea5a643658`. As mudanças das rodadas anteriores e desta permanecem no diff local, sem merge ou publicação.

## Fontes e estado encontrado

Os dois DOCX foram lidos integralmente, incluindo quadros, apêndices, notas de status, fontes e pendências. Os originais estão preservados em `referencias/`, com nomes recebidos, incluindo o sufixo `(1)` do D2; ele não é outra versão metodológica. [Hashes e identificação](referencias/dossies_sha256.csv). As leituras pesquisáveis, derivadas do XML de todos os parágrafos e células, estão em [D1](referencias/dossie1_leitura_integral.txt) e [D2](referencias/dossie2_leitura_integral.txt). Os DOCX não continham mídia, notas de rodapé/finais ou comentários adicionais. Referências precisas abaixo usam seção/quadro, sem inventar páginas da renderização.

O projeto em PDF continua definindo objetivos, vigência e planos. D1 governa regras comuns; D2 governa o TCC; o complemento foi adotado como instrução operacional pelo usuário. As afirmações documentais sobre implementação não foram tratadas como prova: checkout, código, arquivos, logs e hashes foram inspecionados. O relatório 2025–2026 e seus produtos permanecem encerrados e intactos.

Antes das adequações havia: inventário/matriz candidata e plano; conferência negativa dos snapshots legados; recuperação íntegra da fonte LFS e cache gzip; correções de serialização/fixture; saída isolada 202601 com 115 checks aprovados; inventário de 78 códigos municipais; fila de 555 combinações de habilitações; 12 fichas preparatórias e 13 scripts R passando. Nenhum indicador substantivo, fluxo, taxa, série anual ou resultado do TCC havia sido calculado nesta sessão.

Os arquivos anteriores que precisavam ser atualizados foram arquivados byte a byte em [estado anterior à reconciliação](referencias/estado_pre_reconciliacao.zip), antes de alterações funcionais. Não houve reset, limpeza global ou alteração de trabalho de terceiros.

## Matriz de impacto e decisões

A [matriz de impacto](matriz_impacto_dossies.csv) confronta **33 decisões**: estado documental, evidência do estado anterior, consumidores afetados, compatibilidade, ação, verificação e pendência humana. Foi construída antes das mudanças funcionais. Sua coluna de resultado registra a adequação efetivamente executada ou o limite remanescente.

**Permaneceu válido:** RAW/snapshots preservados; SHA-256; cache gzip fora do Git; `CO_UNIDADE` distinto de CNES público; códigos textuais; classificação clínica não alterada; qualidade técnica distinta de validação científica; papéis territoriais separados; ausência de região não preenchida; matriz institucional ainda candidata; R preservado como referência validada. Git LFS segue como recuperação histórica e não como fonte científica. O arquivo bruto tem origem primária/data de extração ainda desconhecidas; a recuperação não inventou esses metadados.

**Orientações ajustadas:**

1. **Tecnologia (D1 §4.2–4.3/Q5):** o estágio experimental observado em determinados caminhos PySUS não é proibição permanente. A configuração comum declara arquitetura híbrida e Python preferencial em engenharia quando validado, preservando R/paridade. Ambiente observado: R 4.5.0, Python 3.12.14, PySUS 2.0.4, PyArrow 19.0.1. Nenhuma atualização/rebaixamento/migração foi feita; êxito por família ainda deve ser demonstrado. O script Python da RUE não foi confundido com PySUS.
2. **Infraestrutura (D1 §6/Q7):** SIM/SIH/SIA/CNES/SIGTAP/população/território são estruturantes, com incorporação progressiva. R12 e as referências correntes de S05/S06 foram corrigidas. Isso não seleciona automaticamente esses indicadores para a matriz mínima nem incorpora todas as medidas do TCC ao núcleo.
3. **Território (D1 §7; D2 §6):** o diagnóstico antigo é válido para município gestor, mas não implementava a classificação congelada de um estudo. Novo aplicador comum preserva original/canônico, papel, data do evento, data da classificação, modo e versão. O TCC aplica retrospectivamente uma versão central explícita; não se escolhe a mais recente automaticamente. Quatro regiões e Noroeste 1 focal são decisões consolidadas; composição oficial, referência temporal e hash continuam pendentes.
4. **Descartes (D1 §11.1; D2 §20.1):** havia descarte silencioso de `co_unidade` vazio/duplicado e `unique()` das linhas de habilitação. Os preparadores agora interrompem com diagnóstico antes da escrita. Não presumem duplicidade física, não apagam eventos e não aplicam EX05 sem comprovar a causa. A conferência completa não encontrou esses casos no recorte real atual; a alteração protege próximas entradas.
5. **Manifestos (D1 §5/Q6):** novas saídas recebem sistema/família, abrangência, competência, arquivo original, recuperação, origem primária desconhecida explícita, tempos de processamento, bytes, SHA-256, contagens de entrada/recorte/saída, schema e responsável. O commit-base identifica a referência, e o hash do manifesto de insumos identifica o conjunto efetivo de códigos do diff não commitado. Não foi reescrito nenhum manifesto histórico.

Há uma condição importante explicitada pelo complemento: D2 §16/Q17 escreve evasão como `100−F1`. Essa igualdade só é válida se o denominador estiver completamente classificado entre destino próprio e externo. O contrato temático agora exige cálculo direto, parcela ignorada explícita e cobertura dos atendimentos interestaduais; não foi alterado o DOCX nem produzido fluxo artificial.

## Separação institucional e temática

[Configuração comum](../../config/institucional.csv) e [perfil do TCC](../../config/estudos/tcc_cardiovascular.csv) são declarativos e separados. O perfil não inicia cálculos automaticamente. Não há período 2014–2024, CID I00–I99, Noroeste 1 ou Prais-Winsten como padrão global. Ambos apontam à mesma tabela territorial central; não foi criada uma base territorial/populacional paralela para a discente.

O TCC registra 2014–2024, granularidade mensal pertinente, G0–G5/traçadores, mortalidade por causa básica/residência, padronização direta Brasil 2010, prematura 30–69, faixas quinquenais distintas das faixas de apresentação, produção aprovada e consulta com CBO, oferta mensal, fluxos com desconhecidos, comparações sobrepostas, integração ecológica e tendência seletiva. Mantém 2020–2022. IAM, fonte populacional, pesos oficiais, pins territoriais, limiares, ética e variante prematura para tendência não receberam valores fabricados.

Os [grupos CID](../../config/estudos/grupos_cid_tcc_cardiovascular.csv), [famílias AC](../../config/estudos/familias_ac_tcc.csv) e [EX01–EX07](../../metadata/estudos/tcc_cardiovascular/motivos_exclusao.csv) preservam sua função: G0 contém subgrupos; AC2 pertence a AC1; motivos de exclusão são por análise e podem se sobrepor. Não existem totalizadores que somem essas categorias indevidamente.

Foram transcritos **77 registros de códigos/itens candidatos** do Apêndice A, em [candidatos_codigos.csv](../../metadata/estudos/tcc_cardiovascular/candidatos_codigos.csv). Código original, descrição, localização e normalização são separados. Remover pontuação tipográfica de SIGTAP/08.xx não inventa código municipal nem validade histórica. Todos permanecem `preliminar_nao_verificado`, sem competências/fonte oficial preenchidas e sem habilitação para seleção final. Itens de leitos/equipamentos sem código permanecem sem código; tipos de habilitação não foram presumidos. A exclusão expressa de `0406010684` do núcleo foi registrada, e as ambiguidades da descrição de `0406010617` foram mantidas para conferência. Nenhum candidato alterou a classificação institucional de 555 combinações.

As **21 pendências** de D1 Q18 e D2 Q25 foram [transcritas literalmente e vinculadas](pendencias_dossies.csv) ao plano existente. As referências bibliográficas PDR ES 2024 e edital SESA 003/2026 delimitam a busca; não comprovam que seus anexos foram consultados nem autorizam preencher municípios por memória.

## Contratos operacionais e limites de implementação

- **Camadas:** `data_raw` é RAW; `data_interim`/cache de comparação abrigam preparação e alguns derivados já filtrados/classificados, portanto têm função parcialmente ANALYTIC apesar do nome físico. `data_processed` é o destino analítico previsto; `outputs`, relatórios e dashboards são OUTPUT. As evidências em `metadata` são auditoria, não produtos públicos validados. Não houve renomeação geral da árvore nem promoção das bases de comparação.
- **Território v2:** `metadata/territorio/schema_correspondencia_v2.csv` adiciona versão explícita. A tabela v2 contém só cabeçalho enquanto a fonte não está disponível. O diagnóstico v1 continua reproduzível e restrito ao gestor; não é uma tabela oficial concorrente. `ler_territorio_congelado()` exige versão/hash, e `territorializar_municipios()` distingue modo contemporâneo e retrospectivo, preserva cada entrada e não reconstrói identificadores. Chamadores devem manter a semântica real de cada campo: rotular um gestor como localização não o transforma em localização.
- **Estoque anual comum, ainda não calculado:** para cada recurso/unidade/território/ano, validar uma observação mensal por chave e estado da competência; a média usa apenas meses válidos. Meses ausentes não entram como zero. Registrar meses válidos/esperados, ano parcial, última competência válida, mínimo/máximo e meses ativos quando definidos. Ausência do recurso só é zero se a competência e a cobertura estiverem observadas. Não foi definido corte mínimo de meses para publicação. Pessoas distintas são recalculadas em cada território/mês; vínculos e horas permanecem medidas distintas. Uma observação 202601 não se tornou estoque anual de 2026 nem série do TCC.
- **SIGTAP/população/elegibilidade/fluxos:** contratos e parâmetros foram especificados, mas não há implementação analítica ou dados históricos validados nesta rodada. Uma lista candidata não substitui catálogo mensal. População anual não é a população padrão de 2010. Um registro sem idade pode permanecer no total e sair apenas da estratificação. AIH/continuidade/reapresentação requerem regra por análise. Para fluxos, o plano de aquisição deve cobrir residentes ES atendidos fora e não residentes atendidos no ES, com ignorados explícitos.

Não foram implementados todos os métodos do TCC para produzir testes sem insumos. O incremento executável foi delimitado às divergências demonstradas: proteção contra descarte, aplicação territorial congelada e proveniência, com verificação da separação dos perfis e do status dos candidatos.

## Recálculos e comparação

A [lista de produtos e decisão de recálculo](produtos_recalculo_dossies.csv) distingue resultados existentes, novas execuções e produtos ainda não gerados.

As duas bases de comparação de 202601 foram **reprocessadas**, em `.cache/cnes/execucoes/reconciliacao_dossies_20261022/`, sem sobrescrever a rodada 2. Foram lidas 602.160 linhas da tabela mãe e 115.103 do relacional; o recorte produziu 12.548 estabelecimentos e 1.963 habilitações. Houve **115 checks aprovados, zero falhas e zero não executados**. Permanecem 501 registros selecionados, sendo 304 com status interno `validado` e 197 `revisar`; isso não é validação documental de normas.

Comparação com a rodada 2: **mesmo schema, mesmas chaves, nenhuma linha adicionada/removida, nenhuma diferença de campo e SHA-256 idêntico dos dois CSV**. Assim, a fila de revisão e o inventário territorial da rodada 3 continuam válidos no escopo de diagnóstico e não exigiram recálculo. Não há taxas, indicadores anuais, fluxos ou modelos cardiovasculares anteriores a recalcular nesta sessão; suas primeiras execuções permanecem pendentes de insumos/decisões afetadas.

[Verificações](../../metadata/ciclo_2026_2027/execucoes/reconciliacao_dossies_20261022/verificacoes.csv), [comparação com rodada 2](../../metadata/ciclo_2026_2027/execucoes/reconciliacao_dossies_20261022/comparacao_rodada02.csv), [manifesto novo](../../metadata/ciclo_2026_2027/execucoes/reconciliacao_dossies_20261022/manifesto_derivados.csv), [execução](../../metadata/ciclo_2026_2027/execucoes/reconciliacao_dossies_20261022/execucao.csv). A comparação campo a campo é uma conferência posterior independente; os hashes das bases nos manifestos de ambas as execuções comprovam a igualdade de bytes.

Reprodução, escolhendo novo identificador e executor real:

```bash
Rscript scripts/comparar_reprocessamento_cnes.R \
  .cache/cnes/fontes/a6dd87e847e2905949dd160f1d88ddd5e7f088fdf61b1124404cf566297d36d6.csv.gz \
  reconciliacao_nova_execucao 'Nome do executor'
```

Os **16 scripts de teste do workflow R** passaram localmente, incluindo recusa de descarte, versão territorial congelada e separação dos perfis/candidatos. [Log](../../metadata/ciclo_2026_2027/testes_reconciliacao_2026-10-22.txt). Os testes territoriais são sintéticos e não validam a regionalização real. O CI remoto em R 4.3 não foi executado; ambiente local R 4.5.0. [Dicionário das novas evidências](../../metadata/ciclo_2026_2027/schema_dicionario_reconciliacao.csv).

## Continuidade corrigida

O [plano operacional](plano_operacional.md) e as [tarefas existentes](tarefas_operacionais.csv) foram atualizados, sem planejamento concorrente. R16–R21 explicam pendências comuns; T01–T10 são o módulo temático. O [ponto de continuidade](continuidade_2026-10-22.md) agora é a referência atual da próxima sessão.

Próximo incremento: completar T01/R06/R18 com fontes territoriais/populacionais verificadas e pins; em paralelo, R08/R17 inspecionam cobertura/layouts e SIGTAP histórico. Fechar IAM bloqueia somente as análises IAM, não G0–G5. Whitelists bloqueiam seus próprios cálculos. O painel completo não é pré-requisito do TCC.

A rede do ambiente continua restrita, sem os quatro hosts oficiais listados na rodada 3; não houve alteração de permissões. Documentos fornecidos resolvem decisões de método, mas não substituem tabelas oficiais ou dados ausentes. Não foram repetidas consultas bloqueadas sem mudança de estado. A liberação dos hosts segue necessária para o trabalho documental externo. Nenhuma decisão consolidada foi reaberta para pedir confirmação desnecessária.

A avaliação corrente de S01/S02 também foi atualizada: o bloqueio técnico encontrado na primeira rodada já foi resolvido na saída isolada, enquanto os bloqueios territoriais/normativos permanecem. O diagnóstico negativo inicial e os snapshots originais continuam preservados; não foram reinterpretados como se tivessem usado a base corrigida.

## Preservação e identidade final desta entrega

Foram conferidos 233 arquivos existentes antes desta rodada: 222 permaneceram byte a byte iguais; 11 foram alterados intencionalmente e possuem cópia anterior exata no ZIP de preservação. [Manifesto de preservação](../../metadata/ciclo_2026_2027/preservacao_reconciliacao_sha256.csv). As únicas alterações preexistentes foram índice, avaliação/matriz candidatas, plano/protocolo/continuidade/tarefas, dois preparadores, executor da comparação e workflow. Raw, snapshots, classificação, PDF e evidências anteriores não foram modificados. Os novos DOCX também foram conferidos contra os anexos recebidos.

O [manifesto dos artefatos desta reconciliação](../../metadata/ciclo_2026_2027/artefatos_reconciliacao_sha256.csv) identifica os arquivos novos/alterados desta rodada, sem incluir seu próprio hash. `comparacao_rodada02.csv` e os controles documentais foram acrescentados após o processamento, portanto estão nesse manifesto final; o manifesto de produtos do executor preserva o conjunto que ele próprio gerou. Nenhum artefato foi tratado como evidência de revisão humana ou validação normativa não realizada.

## Complemento: avaliação de ferramentas em 22/10/2026

A [avaliação com código e documentação originais](avaliacao_ferramentas_2026-10-22.md) completa R08/R19: 13 candidatos/versões e 14 linhas de cobertura; PySUS preferencial sob prova por família. A [complementação DataHub Brasil](avaliacao_datahub_2026-10-22.md) resolve a identidade pelo link do usuário e registra seis casos locais, adicionando sua cobertura à matriz; mantém o candidato como alternativa condicionada, sem adoção integral. PyArrow/Parquet e DuckDB integrados no escopo de serialização comprovado; reexecução R produziu os mesmos 12.548/1.963 registros e passou 115 verificações. Não houve troca de regra sanitária ou remoção de R. Download, conversão e equivalência estão documentados separadamente; aquisição atual bloqueada pelo proxy. F01–F07 na matriz de impacto e P10–P11 na lista de produtos registram as consequências.

Nenhum resultado substantivo existente exige recálculo por esta serialização; fontes normativas, série histórica, SIGTAP e denominadores continuam com seus próprios bloqueios. O relatório 2025–2026, anexos, snapshots, fontes e evidências anteriores foram preservados. Estado documental anterior em `referencias/estado_pre_avaliacao_ferramentas.zip`.
