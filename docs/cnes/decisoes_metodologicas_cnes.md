# Decisões metodológicas do módulo CNES

## Objetivo
Registrar decisões estruturais estáveis do módulo CNES para garantir rastreabilidade e reprodutibilidade.

1. `co_unidade` é a chave operacional do estabelecimento CNES.
2. `cnes` é o código público CNES (oriundo de `CO_CNES`).
3. Joins relacionais CNES devem usar `co_unidade`.
4. A base de habilitações integra com estabelecimentos por `co_unidade`.
5. A chave de habilitação é composta por `codigo_habilitacao + tipo_habilitacao`.
6. `tipo_estabelecimento` só deve ser preenchido quando houver domínio compatível.
7. `gestao` não deve receber preenchimento artificial quando houver incompatibilidade estrutural de domínio.
8. `nome_estabelecimento` usa fallback para `razao_social` quando nome fantasia estiver vazio.
9. `atende_sus` é classificação conservadora (`Sim`/`Não`/`Revisar`), não indicador final.
10. `data_interim` é produto gerável localmente e não fonte de verdade do repositório.
