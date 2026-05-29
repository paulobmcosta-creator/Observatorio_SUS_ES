# Migração Python/PySUS — status consolidado

## 1. Status atual

A migração Python/PySUS está encerrada como prova de viabilidade com ressalvas. A Etapa 5N demonstrou que PySUS/CNES pode apoiar acesso e mapeamento estrutural, mas não autorizou geração de base, substituição do pipeline em R ou uso produtivo sem validação adicional.

Esta pasta foi reduzida a um status consolidado para evitar que documentos diagnósticos longos sejam interpretados como orientação operacional atual.

## 2. Decisão atual

| Tema | Decisão |
| ---- | ------- |
| PySUS | Viável para acesso e mapeamento estrutural do CNES, com ressalvas metodológicas e operacionais. |
| ST/LT/SR | Mantidos como grupos operacionais iniciais para exploração controlada. |
| Contrato intermediário | Criado para organizar a relação PySUS→CNES, mas não equivale a base final. |
| Transformação em memória | Validada apenas parcialmente; não constitui pipeline produtivo completo. |
| ST | Permanece instável/intermitente e exige cautela. |
| `CO_UNIDADE` | Permanece não resolvido; não deve ser manipulado livremente. |
| R | Permanece como oráculo metodológico e referência de paridade. |
| Geração de base | Não autorizada nesta etapa. |
| `data_interim` | Não é área livre de escrita; não deve receber saídas experimentais sem autorização. |

## 3. Onde está o histórico completo

O histórico completo da migração R–Python/PySUS foi preservado em:

- `docs/arquivo_historico/migracao_python/`

Esse arquivo histórico inclui baseline, classificações, governança de migração, provas de conceito, revisões pós-etapa, documentos 5N, documentos 5N.7-8 e o encerramento da viabilidade PySUS/CNES.

## 4. Orientação para aluno

- O aluno não deve começar por esta pasta.
- O aluno deve começar por `docs/guias_aluno/`.
- Scripts Python/PySUS não são pipeline produtivo.
- Python/PySUS permanece experimental/prototípico no repositório.
- R permanece o oráculo metodológico do CNES.
- Geração de base não está autorizada sem orientação explícita.
