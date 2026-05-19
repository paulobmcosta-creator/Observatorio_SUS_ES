# Classificação de habilitações CNES/SIPAC por linha de cuidado (Ciclo 1)

## Objetivo do Ciclo 1

O Ciclo 1 cria uma **camada de metadados analítica** para classificar habilitações CNES/SIPAC por linha de cuidado no Observatório SUS-ES. Esta camada **não é tabela oficial do Ministério da Saúde** e não produz, neste ciclo, base final de estabelecimentos habilitados nem indicadores.

## Arquivos CNES usados

Competência de referência: **202601**.

- Domínio de habilitações: `metadata/cnes/tbSubGruposHabilitacao202601.csv`
- Tabela relacional de habilitações por estabelecimento: `metadata/cnes/rlEstabSipac202601.csv`

## Domínio x Relacional

- `tbSubGruposHabilitacao202601.csv` é tabela de domínio (catálogo de códigos/descrições/tipos/origem).
- `rlEstabSipac202601.csv` é tabela relacional (vínculo entre estabelecimento CNES e habilitação no tempo).

Neste ciclo foi construída apenas a classificação de metadados sobre o domínio.

## Chave composta obrigatória

A identificação de habilitação **não usa apenas código**. A chave correta é composta por:

- `codigo_habilitacao` (`CO_CODIGO_GRUPO`)
- `tipo_habilitacao` (`TP_HABILITACAO`)

Justificativa: o mesmo código pode exigir distinção por tipo para evitar colisões semânticas e erros de join na aplicação posterior da classificação ao `rlEstabSipac`.

## Arquivo gerado

- `metadata/cnes/classificacao_habilitacoes_cnes.csv`

Colunas mínimas:

- `codigo_habilitacao`
- `tipo_habilitacao`
- `descricao_habilitacao`
- `origem_habilitacao`
- `linha_cuidado`
- `sublinha_cuidado`
- `componente_rede`
- `nivel_complexidade`
- `usar_observatorio` (Sim/Não)
- `prioridade` (Alta/Média/Baixa)
- `fonte_cnes`
- `fonte_normativa`
- `criterio_classificacao`
- `status_validacao`
- `observacao`

## Linhas de cuidado utilizadas

- Oncologia
- Cardiovascular
- RUE
- UTI / cuidado crítico
- Nefrologia
- Saúde mental
- Outras habilitações estratégicas
- Fora do escopo inicial
- Revisar

## Critérios de classificação

Classificação inicial baseada em leitura textual da `descricao_habilitacao` e categorização conservadora:

1. Casos com correspondência clara às linhas prioritárias recebem `usar_observatorio = Sim`.
2. Casos sem correspondência clara ficam como `Fora do escopo inicial` ou `Revisar`.
3. Casos ambíguos permanecem com `status_validacao = revisar`.
4. `fonte_normativa` foi mantida como `Revisar` até validação normativa dedicada.

## Limitações metodológicas

- Classificação preliminar, com foco analítico e rastreabilidade.
- Não substitui referência oficial do MS.
- Não deve ser usada para inferência substantiva sem validação normativa.
- Não aplica, neste ciclo, regra de vigência temporal (`CMTP_INICIO`/`CMTP_FIM`) da relacional.

## Próximos passos

- **Ciclo 2**: construir base tabular de estabelecimentos CNES do ES.
- **Ciclo 3**: aplicar esta classificação ao `rlEstabSipac` por chave composta (`codigo_habilitacao` + `tipo_habilitacao`).
