# Base de habilitações CNES por estabelecimento (Ciclo 3)

## Objetivo
Consolidar a base intermediária de habilitações CNES para o ES, integrada à base de estabelecimentos sem alterar lógica analítica do ciclo de classificação.

## Competência de referência
202601.

## Regras estruturais
1. Integração com estabelecimentos por `co_unidade` (chave operacional CNES).
2. `cnes` é carregado da base de estabelecimentos como código público.
3. Chave composta de habilitação preservada: `codigo_habilitacao + tipo_habilitacao`.

## Natureza do produto
A base de habilitações permanece **intermediária** e não constitui indicador final.

## Critérios de validação esperados (competência 202601)
- 1.963 registros.
- 78 municípios.
- Integridade referencial por `co_unidade` (0 faltantes contra base de estabelecimentos).
- 0 registros com `linha_cuidado = "Não classificada"`.
- Auditoria fora do escopo conciliável quando gerada.

## Observações metodológicas
- Não alterar classificação analítica existente.
- Não criar indicadores, dashboards ou mapas neste ciclo.
- Produtos intermediários devem ser geráveis localmente sem versionar `data_interim`.
