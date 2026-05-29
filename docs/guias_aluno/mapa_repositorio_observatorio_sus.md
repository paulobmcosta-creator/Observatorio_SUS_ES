# Mapa do repositório — Observatório SUS-ES

| Diretório/Arquivo | O que é | Situação | O aluno pode alterar? | Observação |
| ----------------- | ------- | -------- | --------------------- | ---------- |
| `README.md` | Apresentação principal do repositório. | ENTRADA_PEDAGOGICA | Não, salvo orientação. | Deve apontar para os guias e o índice geral. |
| `docs/` | Documentação geral, metodológica e histórica. | NUCLEO_ATUAL | Apenas com autorização. | Contém documentação pedagógica, CNES, governança e arquivo histórico. |
| `docs/guias_aluno/` | Guias de entrada para o aluno. | ENTRADA_PEDAGOGICA | Sim, apenas se orientado. | Leitura inicial obrigatória. |
| `docs/cnes/` | Documentação consolidada do núcleo CNES. | NUCLEO_ATUAL | Não sem orientação. | Deve ser lida conforme indicação do orientador. |
| `docs/migracao_python/` | Status consolidado da migração Python/PySUS. | EXPERIMENTAL | Não. | Não é ponto de partida do aluno. |
| `docs/arquivo_historico/` | Documentos históricos e diagnósticos arquivados. | DOCUMENTACAO_HISTORICA | Não. | Consultar apenas por rastreabilidade. |
| `metadata/` | Metadados, dicionários, schemas e contratos. | NUCLEO_ATUAL | Não. | Alterações podem quebrar rastreabilidade. |
| `metadata/cnes/` | Metadados específicos do CNES. | NUCLEO_ATUAL | Não. | Área metodológica sensível. |
| `scripts/` | Scripts de instalação, utilitários ou apoio técnico. | LEGADO_ORACULO | Não. | Não executar sem autorização. |
| `src/` | Código-fonte do pipeline, principalmente R/CNES. | LEGADO_ORACULO | Não. | Referência metodológica e operacional. |
| `python/` | Protótipos e componentes experimentais Python/PySUS. | EXPERIMENTAL | Não. | Não é pipeline produtivo. |
| `tests/` | Testes automatizados e fixtures. | RESTRITO | Não. | Não alterar sem autorização técnica. |
| `config/` | Configurações e dependências declaradas. | RESTRITO | Não. | Mudanças afetam reprodutibilidade. |
| `.github/workflows/` | Integração contínua e validações automáticas. | NAO_EDITAR | Não. | Não alterar em etapa pedagógica inicial. |
| `data_raw/` | Dados brutos preservados. | RESTRITO | Não. | Não é área livre de escrita. |
| `data_interim/` | Dados intermediários. | RESTRITO | Não. | Não gerar saídas experimentais aqui. |
| `data_processed/` | Dados processados/finais. | RESTRITO | Não. | Não criar base final sem autorização. |
