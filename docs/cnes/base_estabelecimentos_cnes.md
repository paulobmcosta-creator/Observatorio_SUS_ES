# Base de estabelecimentos CNES (Ciclo 2)

## Objetivo
Construir a base-mãe tabular de estabelecimentos CNES para a competência 202601, restrita ao Espírito Santo (ES).

## Competência usada
202601.

## Arquivos utilizados
- tbEstabelecimento202601
- tbMunicipio202601
- tbTipoEstabelecimento202601
- tbNaturezaJuridica202601
- tbGestao202601
- rlEstabSubTipo202601
- tbSubTipo202601
- rlEstabAtendPrestConv202601
- tbAtendimentoPrestado202601
- tbConvenio202601

## Diferença entre tb* e rl*
- `tb*`: tabelas de domínio/cadastro (ex.: município, tipo, natureza).
- `rl*`: tabelas relacionais (N:N), exigem agregação antes de juntar na base-mãe.

## Justificativa metodológica
A base de estabelecimentos é a base-mãe do módulo CNES porque centraliza o CNES e permite enriquecimentos posteriores sem duplicar registros.

## Regra de filtragem ES (aplicada antes dos joins)
1. Ler `tbMunicipio`.
2. Selecionar municípios da UF ES por sigla (`CO_SIGLA_ESTADO = ES`) ou código de UF 32 quando existir.
3. Extrair códigos de município do ES.
4. Ler `tbEstabelecimento`.
5. Filtrar estabelecimentos cujo código de município esteja na lista ES.
6. Só então realizar joins auxiliares.

## Relacionamentos e controle de duplicidade
- `rlEstabSubTipo + tbSubTipo`: agregação de subtipos por CNES via valores únicos separados por ` | `.
- `rlEstabAtendPrestConv + tbAtendimentoPrestado + tbConvenio`: agregação por CNES para atendimento e convênio.
- Regra final: uma linha por CNES.

## Regra do campo `atende_sus`
- Regra conservadora baseada em `rlEstabAtendPrestConv` + domínios (`tbConvenio`, `tbAtendimentoPrestado`):
  - `Sim`: existe ao menos um registro relacional com evidência explícita de SUS (ex.: descrição contendo `SUS`).
  - `Não`: há registros relacionais válidos e totalmente interpretados, sem qualquer evidência SUS, sem ambiguidade e com evidência explícita não-SUS.
  - `Revisar`: ausência de relacionamento, join incompleto com domínios, campos vazios ou evidência ambígua.
- Princípio metodológico: ausência de evidência **não** é tratada automaticamente como não atendimento SUS.
- Ressalva metodológica: o valor `Não` indica ausência de evidência de atendimento/convênio SUS nas tabelas relacionais utilizadas no Ciclo 2B, quando há informação relacional válida e interpretável, mas **não deve ser interpretado** como prova absoluta de inexistência de qualquer relação do estabelecimento com o SUS em outros sistemas, competências ou dimensões cadastrais.

## Campos gerados
`competencia`, `cnes`, `nome_estabelecimento`, `razao_social`, `cod_municipio`, `municipio`, `uf`, `tipo_estabelecimento`, `subtipo_estabelecimento`, `natureza_juridica`, `gestao`, `atende_sus`, `atendimento_prestado`, `convenio`, `fonte`, `arquivo_origem`, `data_processamento`.

## Limitações
- O script depende de arquivo real de `tbEstabelecimento` (csv/csv.gz/zip). Ponteiro Git LFS sem conteúdo real interrompe o processamento.
- Nomes de colunas podem variar entre layouts; o script faz mapeamento por candidatos conhecidos.

## Versionamento
- Base nacional não é gerada nem versionada no Ciclo 2.
- Produto esperado: `data_interim/cnes/estabelecimentos/cnes_estabelecimentos_es_202601.csv`.
- No Ciclo 2B (execução com base real), o arquivo final ES ficou com ~3,1 MB e foi versionado.

## Execução real (Ciclo 2B, competência 202601)
- Estabelecimentos ES gerados: **12.548**.
- Municípios ES representados: **78**.
- Distribuição de `atende_sus`:
  - `Sim`: **2.594**
  - `Não`: **9.706**
  - `Revisar`: **248**
- Registros com `cnes` vazio: **0**.
- Registros com `cod_municipio` vazio: **0**.
- Tamanho aproximado do arquivo final: **3.058.707 bytes** (~3,1 MB).

## Próximo ciclo
No Ciclo 3, a classificação de habilitações será aplicada ao `rlEstabSipac` e cruzada com esta base de estabelecimentos.
