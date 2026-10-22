# Rodada 2 — fonte CNES, armazenamento e comparação isolada

Continuidade autorizada em 22/10/2026, após a primeira rodada. Esta nota atualiza o ponto de retomada; os registros da rodada 1 continuam descrevendo o estado encontrado antes das correções.

## Decisão sobre Git LFS

**Os dados ainda são necessários; Git LFS não precisa ser uma dependência da execução.** O objeto foi recuperado do repositório e corresponde exatamente ao ponteiro histórico: 284.224.999 bytes, SHA-256 `a6dd87e847e2905949dd160f1d88ddd5e7f088fdf61b1124404cf566297d36d6`. Não era um artefato descartável: contém `CO_UNIDADE` e `CO_CNES`, necessários para conferir a identidade dos estabelecimentos.

| Alternativa | Avaliação nesta rodada |
|---|---|
| CSV de 284,2 MB no Git comum | Inadequado; ultrapassa o limite de 100 MiB por arquivo do GitHub e amplia os clones. |
| Gzip de 85,5 MB no Git comum | Cabe no limite por arquivo, mas acrescenta binário volumoso ao histórico a cada atualização. Não adotado. |
| Manifesto pequeno no Git + gzip em cache ignorado | Implementado. Validação do tamanho e SHA-256 dos bytes originais antes do uso. O preparador recebe o caminho explicitamente. |
| Objeto em armazenamento externo durável + manifesto | Próxima etapa para eliminar a dependência de LFS também na recuperação. Requer uma cópia durável e endereço verificável; não foi inventado nem publicado um destino. |

A compressão `gzip -n` produz 85.482.494 bytes nesta máquina, redução de aproximadamente **69,9%**. A identidade científica da fonte é o hash do CSV descomprimido; o hash do gzip também é registrado, mas não se presume idêntico entre implementações de compressão.

O ponteiro, `.gitattributes` e o objeto remoto LFS foram **mantidos como recuperação histórica**. O LFS ainda é a única origem remota deste arquivo específico que foi efetivamente recuperada e verificada. Removê-lo agora deixaria a recuperação dependente deste ambiente temporário. A migração operacional está implementada; a migração do arquivo histórico para outro armazenamento durável ainda não está concluída.

## Implementação e reprodução

Requisitos: R (verificado localmente em 4.5.0; CI configurado em 4.3), `gzip` e `sha256sum`. Git LFS só é necessário na recuperação histórica abaixo; não é usado pelo importador, pelos testes nem pelo reprocessamento quando o arquivo já está disponível.

Na raiz do repositório, para a recuperação histórica em cache separado do checkout:

```bash
git -c lfs.storage="$PWD/.cache/lfs" lfs fetch origin \
  6478f93a50d03270a78959730221f2ea5a643658 \
  --include=data_raw/cnes/202601/tbEstabelecimento202601.csv --exclude=

Rscript scripts/preparar_cache_cnes.R \
  .cache/lfs/objects/a6/dd/a6dd87e847e2905949dd160f1d88ddd5e7f088fdf61b1124404cf566297d36d6
```

Também se pode fornecer um CSV ou CSV.GZ obtido de outra origem, desde que corresponda **exatamente** ao manifesto. Não há download implícito, transformação de códigos nem aceitação de arquivo parecido. O cache padrão é `.cache/cnes/fontes/<sha256-do-csv>.csv.gz`, ignorado pelo Git. Arquivos divergentes ou gzip corrompido são rejeitados; cache existente divergente não é substituído automaticamente.

Para reproduzir a comparação, escolhendo um identificador de execução novo e identificando o executor real:

```bash
Rscript scripts/comparar_reprocessamento_cnes.R \
  .cache/cnes/fontes/a6dd87e847e2905949dd160f1d88ddd5e7f088fdf61b1124404cf566297d36d6.csv.gz \
  comparacao_local_01 'Nome do executor'
```

O comando grava as bases de comparação somente em `.cache/cnes/execucoes/<id>/` e as evidências agregadas em `metadata/ciclo_2026_2027/execucoes/<id>/`. Recusa identificador já utilizado. Usa a competência histórica **202601**, não representa atualização da competência nem nova extração do DATASUS. A data de processamento corresponde à nova execução. O CSV e os auxiliares históricos permanecem intactos. Se o contrato falhar, as evidências são gravadas e o comando termina com código 1.

O manifesto identifica o repositório, commit e caminho recuperados. A URL e a data da extração primária continuam desconhecidas, explicitamente registradas como `nao_documentada`; recuperar bytes do Git LFS não reconstitui essa proveniência.

## Correções delimitadas

- `ler_csv_cnes()` e `preparar_estabelecimentos_cnes()` aceitam caminho explícito da tabela mãe, permitindo gzip mesmo com ponteiro CSV presente. O comportamento anterior continua disponível; ponteiro não materializado ainda gera erro claro quando selecionado.
- A linha de `data_atualizacao` no schema de habilitações recebeu aspas ao redor da expressão com vírgula. Nenhuma definição metodológica foi alterada.
- A fixture sintética ganhou `CO_CNES` com sete posições e zeros iniciais, distinto de `CO_UNIDADE`. Nenhum identificador real foi construído.
- Os testes do cache cobrem integridade, corrupção, reutilização, caminhos com espaços/aspas, seleção explícita e transformação com chaves textuais distintas. O teste negativo de CSV malformado foi mantido.

O dicionário das novas evidências e do manifesto está em [schema_dicionario_rodada02.csv](../../metadata/ciclo_2026_2027/schema_dicionario_rodada02.csv). Os schemas de estabelecimentos/habilitações descrevem as saídas locais; a comparação não as promove a bases oficiais ou indicadores validados.

## Resultado observado e evidências

Execução `rodada_02_20261022`, de 04:07:00 a 04:09:32 UTC em 22/10/2026, por Codex identificado como automação solicitada pelo pesquisador. O comando terminou com **código 0**, com **115 checks aprovados, zero falhas e zero verificações não executadas**. Isso comprova o contrato técnico conferido, não homologação de indicadores ou validação externa.

| Medida | Resultado da saída isolada |
|---|---:|
| Estabelecimentos / códigos municipais observados | 12.548 / 78 |
| CNES públicos com exatamente sete dígitos | 12.548 |
| CNES públicos com zero inicial preservado | 1.297 |
| Registros de habilitação | 1.963 |
| Habilitações no escopo | 501 |
| No escopo com status interno `validado` / `revisar` | 304 / 197 |
| Habilitações fora do escopo | 1.462 |

A associação do `cnes` legado ao `co_unidade` observado na nova saída não perdeu nem acrescentou chaves, tanto nos estabelecimentos quanto na chave composta estabelecimento/código/tipo das habilitações. Assim, neste snapshot, a correspondência está comprovada por comparação completa; não foi obtida truncando ou completando códigos.

As únicas diferenças em campos compartilhados foram:

- `cnes`: 12.548 linhas de estabelecimentos e 1.963 de habilitações agora contêm o código público lido diretamente de `CO_CNES`.
- `nome_estabelecimento`: três estabelecimentos receberam o fallback para razão social já previsto no preparador; nenhum nome foi inventado.
- `data_processamento`: atualizada em todas as linhas da saída nova, conforme a execução.

`co_unidade` é um campo adicional nas duas saídas novas. Não houve diferenças nos demais campos compartilhados, incluindo vínculo SUS, município e classificação de habilitações. O vínculo territorial utilizado continua sendo o município gestor do layout; seis dígitos e cobertura de 78 códigos não comprovam correspondência com regiões de saúde.

Evidências: [contagens](../../metadata/ciclo_2026_2027/execucoes/rodada_02_20261022/contagens_observadas.csv), [comparação campo a campo](../../metadata/ciclo_2026_2027/execucoes/rodada_02_20261022/comparacao_legado.csv), [verificações](../../metadata/ciclo_2026_2027/execucoes/rodada_02_20261022/verificacoes.csv), [insumos](../../metadata/ciclo_2026_2027/execucoes/rodada_02_20261022/insumos_sha256.csv), [produtos](../../metadata/ciclo_2026_2027/execucoes/rodada_02_20261022/produtos_sha256.csv) e [execução](../../metadata/ciclo_2026_2027/execucoes/rodada_02_20261022/execucao.csv).

Os **11 scripts de teste configurados no workflow R** passaram localmente. Após acrescentar a regressão do schema real, o teste de contrato foi reexecutado com **15 cenários aprovados**. O novo teste do cache passou sem usar Git LFS. [Log dos testes](../../metadata/ciclo_2026_2027/testes_rodada02_2026-10-22.txt). Os dois scripts manuais antigos `test_base_*`, que usam o caminho bruto padrão, não foram executados: o ponteiro do checkout foi preservado. O reprocessamento real foi verificado pelo novo executor e pelo contrato completo, usando a seleção explícita do cache. O workflow remoto em R 4.3 não foi disparado nesta sessão.

## Preservação e próximo trabalho

R04 (recuperação/layout/chaves) e R05 (serialização/fixture) estão concluídas tecnicamente nesta rodada, com revisão humana ainda não presumida. A comparação isolada antecipa a conferência técnica de R09, mas não encerra R09: faltam seus pré-requisitos metodológicos e temporais. As situações registradas em `tarefas_operacionais.csv` permanecem como fotografia da primeira rodada; esta nota registra a atualização posterior.

Retomar em **R06/R07**: significado territorial, fonte oficial de correspondência município–região com vigência, revisão normativa do recorte e tratamento dos 197 registros selecionados ainda em revisão. Em paralelo, definir armazenamento durável para o gzip e testar recuperação em ambiente limpo antes de retirar a dependência histórica de LFS. Nenhum passo depende de reabrir o relatório 2025–2026.

Os snapshots históricos, os dados brutos, a classificação, o PDF e os registros de execução da primeira rodada foram preservados. O schema corrigido possui um hash novo; o hash antigo nas evidências da rodada 1 continua válido para o arquivo daquela rodada e pode ser recuperado do commit-base. Não se deve reinterpretar o resultado antigo como se tivesse usado o schema corrigido. [Manifesto de preservação desta rodada](../../metadata/ciclo_2026_2027/preservacao_rodada02_sha256.csv) discrimina as alterações autorizadas.

Não houve alteração no relatório encerrado, envio a parceiros, merge ou publicação. As bases novas permanecem em cache para comparação; os arquivos de código, metadados e documentação estão no checkout para revisão.
