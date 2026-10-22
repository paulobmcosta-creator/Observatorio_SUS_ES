# Primeiro incremento — conferência reprodutível de contrato CNES

## Escolha e fronteira

O diagnóstico demonstrou que as contagens históricas podem coincidir mesmo quando os snapshots divergem do contrato atual. Por isso o incremento escolhido foi uma rotina **nova em R**, somente de leitura das bases, que expõe essas divergências antes de qualquer cálculo regional. Corresponde a O1/O4 e ao plano P2, com consequências metodológicas para P1.

Não substitui o pipeline R, não migra para Python, não altera classificação, não atualiza competências e não reconstrói códigos. Usa os snapshots 202601 existentes, a classificação existente, um caso da fixture histórica do piloto e casos sintéticos explicitamente de teste. A fixture do ciclo 2, incompatível com o preparador atual por ausência de `CO_CNES`, não foi alterada para forçar aprovação.

## Arquivos implementados

- [Verificador](../../src/validation/conferir_contrato_snapshot_cnes.R): leitor CSV estrito e conferência de tipos, preenchimento, domínio, chaves, relações e classificação.
- [Executor com registro](../../scripts/conferir_snapshot_cnes.R): nova execução em diretório ainda inexistente, hashes de insumos/código/produtos, contagens e resultado.
- [Testes](../../tests/test_conferir_contrato_snapshot_cnes.R): 14 cenários, inclusive entradas inválidas.
- [CI R](../../.github/workflows/validar_pipeline_cnes_r.yml): adiciona execução do teste de contrato. O CI remoto não foi executado nesta tarefa.

O leitor usa todas as colunas como texto, preserva zeros e distingue `NA` em objetos R de vazios. Um CSV com número divergente de campos é recusado. O erro do schema é registrado e impede sua comparação completa; o núcleo de chaves descrito nos documentos continua conferido. Não é um reparo do schema.

Para estabelecimentos, a unicidade é por competência e `co_unidade`; para habilitações, competência, `co_unidade`, código e tipo da habilitação. A classificação usa código **e tipo**. Na relação muitos-para-um, o verificador exige chave de estabelecimento preenchida e única, confere existência e igualdade de código público/município, sem junção por `cnes` legado. Ausência de chave produz `nao_executado`, não aprovação.

O formato de sete dígitos para código público operacionaliza a distinção CNES/CO_UNIDADE nos schemas e documentos atuais. Não se impõe comprimento ao `CO_UNIDADE`, não se valida territorialmente um código apenas pelo número de dígitos e não se infere região oficial. Completude, domínios e relações cobrem o escopo descrito; não são auditoria integral de todo campo opcional ou de todas as regras do CNES.

## Reprodução

Pré-requisitos: R ≥4.3 (verificado localmente com R 4.5.0), Git, `sha256sum` do sistema. Não foi adicionada dependência R externa. No ambiente preparado nesta conversa, acrescente `/workspace/.setup-observatorio/bin` ao PATH. Execute **na raiz do checkout**:

```bash
Rscript tests/test_conferir_contrato_snapshot_cnes.R
```

Esperado: 14 cenários passam, incluindo reprovação controlada de entradas incorretas. Os testes usam diretórios temporários e não geram bases históricas.

Para uma nova conferência, escolha nome de execução ainda inexistente e identifique o executor real:

```bash
Rscript scripts/conferir_snapshot_cnes.R \
  metadata/ciclo_2026_2027/execucoes/nova_conferencia \
  'identificação real do executor'
```

No snapshot atual, a **saída esperada é código 1** e o estado `bloqueado_por_contrato`. Não use `|| true` para registrar aprovação. Diretório já existente é recusado: outra conferência exige outro nome. O destino deve ser subdiretório imediato de `metadata/ciclo_2026_2027/execucoes`; não há caminho de saída para `data_raw`, `data_interim` ou `data_processed`.

## Resultado da rodada

Registro canônico: [rodada_01_20261022_v2](../../metadata/ciclo_2026_2027/execucoes/rodada_01_20261022_v2/execucao.csv). O sufixo v2 identifica a revisão do verificador que passou a detectar a malformação do schema, em vez de interpretar sua sobra como campo. O rascunho diagnóstico anterior não integra as evidências finais. É **uma nova conferência em 22/10/2026**, não reexecução de extração e não manifesto histórico da RUE.

| Verificação | Resultado |
|---|---|
| Teste novo | 14 cenários aprovados |
| Conferência dos snapshots | 61 regras passaram, 7 falharam, 4 não foram executadas; processo retornou 1 |
| Falhas | Ausência de chave; códigos públicos incompatíveis; 3 nomes vazios; CSV de schema malformado |
| Não executadas | Duas unicidades por chave operacional, relação habilitações→estabelecimentos e comparação completa com schema de habilitações |
| Totais legados | Reconciliados no escopo da leitura; não transformados em validação de identidade/indicador |

As sete falhas são **regras reprovadas**, não sete problemas independentes: a ausência de `co_unidade` nos estabelecimentos é registrada tanto na comparação do schema quanto no núcleo. As ocorrências de campos e registros têm unidades diferentes e não devem ser somadas como um total de registros inválidos.

Arquivos de evidência:

- [verificacoes.csv](../../metadata/ciclo_2026_2027/execucoes/rodada_01_20261022_v2/verificacoes.csv): `escopo`, `regra`, `estado`, `ocorrencias`, `detalhe`; `ocorrencias=NA` significa check não executado. O significado da contagem depende da regra: colunas faltantes, linhas inválidas, tipos inadequados ou duplicações excedentes.
- [contagens_observadas.csv](../../metadata/ciclo_2026_2027/execucoes/rodada_01_20261022_v2/contagens_observadas.csv): `medida`, `valor`; valores descritivos de linhas/campos, com unidade explícita no nome e no diagnóstico.
- [insumos_sha256.csv](../../metadata/ciclo_2026_2027/execucoes/rodada_01_20261022_v2/insumos_sha256.csv): papel, caminho relativo, hash SHA-256 e tamanho, incluindo código e teste exatos executados.
- [execucao.csv](../../metadata/ciclo_2026_2027/execucoes/rodada_01_20261022_v2/execucao.csv): metadados chave/valor; timestamp UTC, executor automatizado, commit-base, ambiente, campos, ausência de filtros e resultado.
- [produtos_sha256.csv](../../metadata/ciclo_2026_2027/execucoes/rodada_01_20261022_v2/produtos_sha256.csv): arquivo/hash dos quatro produtos anteriores; não inclui seu próprio hash.

Todos os CSVs de evidência são UTF-8. O instante desta conferência não substitui o instante de extração original. Fonte oficial específica, URL, extrator original e data/hora de obtenção não constam dos snapshots; o manifesto informa a ausência em vez de fabricá-los. As contagens são reconciliadas sobre os insumos locais identificados por hash, não sobre uma nova coleta CNES.

O próximo incremento deve recuperar o objeto LFS em área isolada, corrigir a serialização do schema em mudança revisável e verificar separadamente os campos públicos e operacionais. Só depois cabe propor regeneração versionada, com comparação das diferenças e revisão metodológica, preservando estes snapshots.
