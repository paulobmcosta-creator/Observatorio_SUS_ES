# Base de estabelecimentos CNES (Ciclo 2)

## Objetivo
Consolidar a base intermediária de estabelecimentos CNES para o Espírito Santo (ES), mantendo separação entre chave operacional e código público.

## Competência de referência
202601.

## Chaves: diferença entre `co_unidade` e `cnes`
- `co_unidade`: chave operacional CNES originada de `CO_UNIDADE`.
- `cnes`: código público CNES originado de `CO_CNES`.

Regra metodológica: joins relacionais do CNES devem usar `co_unidade`; `cnes` é usado para identificação pública e comunicação externa.

## Regras de relacionamento
- Relacionais `rl*` (ex.: `rlEstabSubTipo`, `rlEstabAtendPrestConv`) são agregadas por `co_unidade`.
- A base final mantém uma linha por `co_unidade` para o ES na competência.

## Regras de enriquecimento
- `tipo_estabelecimento`: join por chave compatível `CO_TIPO_ESTABELECIMENTO` quando há domínio compatível.
- `nome_estabelecimento`: usa nome fantasia; se vazio, aplica fallback para `razao_social`.

## Limitação metodológica de `gestao`
Na competência 202601, `TP_GESTAO` da `tbEstabelecimento` não apresentou compatibilidade estrutural com `CO_GESTAO` da `tbGestao`; por isso não há preenchimento artificial de `gestao`.

## Regra de `atende_sus`
Campo categórico conservador (`Sim`, `Não`, `Revisar`) com base em evidências relacionais. Não deve ser interpretado como prova absoluta de vínculo e não constitui indicador final.

## Natureza do produto
Esta base é **intermediária** (insumo de integração) e não um indicador final.

## Versionamento
- `data_interim` é produto gerável localmente.
- CSV intermediário não é fonte de verdade do repositório.
- Fonte de verdade: código + metadados + testes + documentação.
