# Etapa 5R — reinicialização da Etapa 5 por correção da política de recorte CNES

## 1. Objetivo
Este documento registra a reinicialização controlada da Etapa 5 em razão de correção metodológica sobre o funcionamento do CNES.

Registro formal:
- as Etapas 5 e 5S anteriores foram removidas da árvore atual;
- elas foram removidas porque partiam da exigência de recorte por UF antes do download;
- essa exigência não corresponde ao funcionamento operacional usual do CNES;
- o histórico Git permanece preservado;
- a nova Etapa 5 deverá ser planejada com recorte UF pós-download/leitura temporária.

## 2. Premissa metodológica corrigida
Premissa inadequada anterior:
- exigir recorte por UF=ES antes do download;
- classificar ausência de UF pré-download como falha ou insegurança.

Premissa corrigida:
- o CNES deve ser tratado como fonte em que o arquivo é obtido por tabela/arquivo e competência;
- o recorte UF=ES ocorre depois da leitura temporária;
- a segurança operacional depende de tabela, competência, tamanho/limite, diretório temporário, exclusão e ausência de persistência no repositório.

## 3. O que foi descartado
Documentos/scripts/testes removidos:
- docs/migracao_python/05_extracao_minima_temporaria_cnes_2025.md
- docs/migracao_python/05_revisao_pos_etapa5.md
- docs/migracao_python/05S_investigacao_recorte_fallback_cnes.md
- python/observatorio_sus/extract/extrair_cnes_temporario_2025.py
- python/observatorio_sus/extract/investigar_fallback_cnes.py
- tests/python/test_extrair_cnes_temporario_2025_cli.py
- tests/python/test_investigar_fallback_cnes_cli.py

Esse descarte não invalida Etapas 0–4; invalida apenas a execução anterior das Etapas 5 e 5S por premissa inadequada.

## 4. O que permanece válido
Continuam válidos:
- baseline R pré-migração;
- classificação do legado R;
- governança híbrida R–Python;
- POC PySUS 2.x como parcialmente suficiente;
- contratos CNES da Etapa 4;
- revisão pós-Etapa 4;
- regras sobre CO_UNIDADE;
- regras sobre CO_CNES;
- preservação textual de códigos;
- proibição de escrita em data_raw/data_interim/data_processed;
- R como oráculo metodológico.

## 5. Nova política de segurança operacional para CNES
A nova Etapa 5 deve obedecer a:
1. identificar tabela/arquivo CNES;
2. identificar competência mensal;
3. conhecer ou limitar tamanho antes do download, quando possível;
4. baixar somente em diretório temporário;
5. registrar nome, origem, tamanho, competência, tabela, caminho temporário e exclusão;
6. filtrar UF=ES após leitura temporária;
7. validar CO_UNIDADE e CO_CNES após leitura temporária;
8. não salvar dado bruto ou recortado no repositório;
9. não aplicar transformação R;
10. não aplicar classificação de habilitações.

## 6. Deliberação humana necessária antes da nova Etapa 5
Ainda será necessária decisão humana sobre:
- tabela piloto;
- competência piloto;
- limite máximo de tamanho;
- se download nacional mensal temporário é aceitável;
- se o teste começa apenas por tbEstabelecimento;
- se tbMunicipio deve ser testada junto;
- se habilitações ficam proibidas até validação de estabelecimentos.

Sugestão preliminar:
- tabela piloto: tbEstabelecimento;
- competência piloto: 202501;
- UF pós-leitura: ES;
- limite máximo: a definir;
- persistência: nenhuma.

## 7. Próxima etapa recomendada
Recomendação:

Nova Etapa 5 — teste piloto de extração temporária CNES por tabela/competência com UF pós-leitura.

Não recomendar Etapa 6.

## 8. Critérios de aceite desta reinicialização
- [x] Artefatos da Etapa 5 anterior removidos.
- [x] Artefatos da Etapa 5S removidos.
- [x] Documento 05R criado.
- [x] Deliberação humana pré-Etapa 5 corrigida.
- [x] Nenhum script R alterado.
- [x] Nenhum dado alterado.
- [x] Nenhum metadado alterado.
- [x] Nenhum docs/cnes alterado.
- [x] Nenhum workflow alterado.
- [x] Testes Python executados.
- [x] Próxima etapa recomendada registrada.

## 9. Conclusão
A Etapa 5 foi reinicializada por correção metodológica e deverá ser refeita com política de recorte UF pós-download.
