# Convenções de versionamento de dados

## Diretrizes por diretório
- `data_raw`: dados brutos; podem exigir Git LFS quando indispensável.
- `data_interim`: produtos intermediários gerados; não versionar por padrão.
- `data_processed`: produtos analíticos finais; avaliar versionamento caso a caso.
- `metadata`: versionar schemas, dicionários, classificações e manifestos.
- `docs`: versionar documentação metodológica e operacional.
- `src`: versionar scripts de transformação/integração.
- `tests`: versionar testes automatizados.

## Princípios
- CSV intermediário não é fonte de verdade.
- Fonte de verdade do repositório = código + metadados + testes + documentação.
- Produtos intermediários devem ser regeneráveis localmente de forma reprodutível.
