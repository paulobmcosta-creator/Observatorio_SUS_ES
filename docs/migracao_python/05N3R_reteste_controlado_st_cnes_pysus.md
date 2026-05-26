# Etapa 5N.3R — reteste controlado do grupo ST no PySUS/CNES

## 1. Objetivo
Retestar exclusivamente o grupo ST, que ficou inconclusivo na Etapa 5N.3 por erro de rede/ReadTimeout.

Esta etapa:
- não é migração plena;
- não gera base;
- não salva dados;
- não substitui R;
- não altera scripts;
- não altera metadados;
- não altera docs/cnes;
- não avança para 5N.4.

## 2. Justificativa
ST está associado a estabelecimentos e é estratégico para comparação futura com contratos CNES (estabelecimentos, CNES, unidade e município). Na 5N.3, LT e SR retornaram DataFrame; ST ficou inconclusivo.

## 3. Condição prévia
Foram confirmados os arquivos:
- `docs/migracao_python/05N_reinicio_cnes_python_api_pysus.md`
- `docs/migracao_python/05N1_isolamento_pysus_duckdb_cnes.md`
- `docs/migracao_python/05N2_diagnostico_falha_cnes_pos_isolamento.md`
- `docs/migracao_python/05N3_inventario_grupos_cnes_pysus.md`
- `python/observatorio_sus/extract/inventariar_grupos_cnes_pysus.py`

## 4. Ambiente usado
- branch: `work`
- commit HEAD: `aeb8a2fb3848291f448993c2f9f72126a032aec7`
- último commit: `aeb8a2f feat(migracao): inventariar grupos CNES via PySUS (script, testes e doc)`
- Python: 3.12.3
- PySUS: 2.0.4
- status inicial: limpo
- status final: apenas documento 5N.3R criado

## 5. Comando de reteste
`python python/observatorio_sus/extract/inventariar_grupos_cnes_pysus.py --uf ES --ano 2024 --mes 1 --modo testar_grupos --grupos-candidatos ST --tentativas 5 --base-backoff 2 --jitter-max 1`

## 6. Resultado do reteste ST
| Grupo | Chamada aceita? | DataFrame? | Linhas | Colunas | Tentativas | Causa/erro | Interesse metodológico | Nível de evidência |
|---|---|---|---:|---:|---:|---|---|---|
| ST | Sim | Sim | 8867 | 208 | 1 | GRUPO_ACEITO_COM_RETORNO | ALTO_INTERESSE | EVIDENCIA_MODERADA |

## 7. Colunas retornadas, se houver
ST retornou DataFrame. Colunas:
CNES, CODUFMUN, COD_CEP, CPF_CNPJ, PF_PJ, NIV_DEP, CNPJ_MAN, COD_IR, REGSAUDE, MICR_REG, DISTRSAN, DISTRADM, VINC_SUS, TPGESTAO, ESFERA_A, RETENCAO, ATIVIDAD, NATUREZA, CLIENTEL, TP_UNID, TURNO_AT, NIV_HIER, TP_PREST, CO_BANCO, CO_AGENC, C_CORREN, CONTRATM, DT_PUBLM, CONTRATE, DT_PUBLE, ALVARA, DT_EXPED, ORGEXPED, AV_ACRED, CLASAVAL, DT_ACRED, AV_PNASS, DT_PNASS, GESPRG1E, GESPRG1M, GESPRG2E, GESPRG2M, GESPRG4E, GESPRG4M, NIVATE_A, GESPRG3E, GESPRG3M, GESPRG5E, GESPRG5M, GESPRG6E, GESPRG6M, NIVATE_H, QTLEITP1, QTLEITP2, QTLEITP3, LEITHOSP, QTINST01, QTINST02, QTINST03, QTINST04, QTINST05, QTINST06, QTINST07, QTINST08, QTINST09, QTINST10, QTINST11, QTINST12, QTINST13, QTINST14, URGEMERG, QTINST15, QTINST16, QTINST17, QTINST18, QTINST19, QTINST20, QTINST21, QTINST22, QTINST23, QTINST24, QTINST25, QTINST26, QTINST27, QTINST28, QTINST29, QTINST30, ATENDAMB, QTINST31, QTINST32, QTINST33, CENTRCIR, QTINST34, QTINST35, QTINST36, QTINST37, CENTROBS, QTLEIT05, QTLEIT06, QTLEIT07, QTLEIT08, QTLEIT09, QTLEIT19, QTLEIT20, QTLEIT21, QTLEIT22, QTLEIT23, QTLEIT32, QTLEIT34, QTLEIT38, QTLEIT39, QTLEIT40, CENTRNEO, ATENDHOS, SERAP01P, SERAP01T, SERAP02P, SERAP02T, SERAP03P, SERAP03T, SERAP04P, SERAP04T, SERAP05P, SERAP05T, SERAP06P, SERAP06T, SERAP07P, SERAP07T, SERAP08P, SERAP08T, SERAP09P, SERAP09T, SERAP10P, SERAP10T, SERAP11P, SERAP11T, SERAPOIO, RES_BIOL, RES_QUIM, RES_RADI, RES_COMU, COLETRES, COMISS01, COMISS02, COMISS03, COMISS04, COMISS05, COMISS06, COMISS07, COMISS08, COMISS09, COMISS10, COMISS11, COMISS12, COMISSAO, AP01CV01, AP01CV02, AP01CV03, AP01CV04, AP01CV05, AP01CV06, AP01CV07, AP02CV01, AP02CV02, AP02CV03, AP02CV04, AP02CV05, AP02CV06, AP02CV07, AP03CV01, AP03CV02, AP03CV03, AP03CV04, AP03CV05, AP03CV06, AP03CV07, AP04CV01, AP04CV02, AP04CV03, AP04CV04, AP04CV05, AP04CV06, AP04CV07, AP05CV01, AP05CV02, AP05CV03, AP05CV04, AP05CV05, AP05CV06, AP05CV07, AP06CV01, AP06CV02, AP06CV03, AP06CV04, AP06CV05, AP06CV06, AP06CV07, AP07CV01, AP07CV02, AP07CV03, AP07CV04, AP07CV05, AP07CV06, AP07CV07, ATEND_PR, DT_ATUAL, COMPETEN, NAT_JUR.

Dtypes observados: todos os 208 campos como `object`.

## 8. Campos-chave detectados
| Campo/termo | Detectado? | Observação |
|---|---|---|
| cnes | Sim | Campo CNES presente (CNES). |
| co_cnes | Não | Não apareceu literalmente. |
| unidade | Não | Não apareceu literalmente. |
| co_unidade | Não | Não apareceu literalmente. |
| município | Sim (aproximado) | CODUFMUN sugere município de forma indireta. |
| co_municipio | Não | Não apareceu literalmente. |
| uf | Sim (aproximado) | Detectado por heurística via CODUFMUN. |
| estabelecimento | Não | Não apareceu literalmente. |

## 9. Relação preliminar com contratos CNES
- Relação nominal: `NOMINAL_APROXIMADA`.
- Campos contratuais literais encontrados: nenhum.
- Campos aproximados: `cnes`.
- Cobertura: `COBERTURA_POTENCIAL_PARCIAL`.
- Ressalvas: não há confirmação de cobertura contratual plena; resultado serve para mapeamento estrutural exploratório.

## 10. Comparação com resultado anterior da 5N.3
| Item | 5N.3 | 5N.3R | Interpretação |
|---|---|---|---|
| ST retornou DataFrame? | Não | Sim | Falha anterior foi transitória de rede. |
| Causa/erro | ERRO_DE_REDE (ReadTimeout) | GRUPO_ACEITO_COM_RETORNO | Reteste superou a instabilidade. |
| Tentativas | 3 (sem sucesso) | 1 (com sucesso) | Backoff conservador foi suficiente. |
| Colunas | 0 | 208 | ST voltou a ser operacionalmente utilizável. |
| Recomendação para 5N.4 | pendente | incluir ST | Pode compor escopo exploratório junto de LT/SR. |

## 11. Implicações para a 5N.4
Como ST retornou DataFrame, recomenda-se 5N.4 com ST, LT e SR em caráter de mapeamento estrutural exploratório (sem validar cobertura contratual plena e sem substituir R).

## 12. Testes executados
- `python -m pytest tests/python`
- Resultado: 29 testes aprovados.
- Não houve escrita em `data_raw`, `data_interim` e `data_processed`.

## 13. Perguntas obrigatórias
| Pergunta | Resposta | Evidência | Implicação |
|---|---|---|---|
| 1. A 5N.3 existia? | Sim. | Arquivo 05N3 presente. | Reteste viável. |
| 2. ST foi retestado isoladamente? | Sim. | `--grupos-candidatos ST`. | Escopo estrito cumprido. |
| 3. Foram usadas 5 tentativas? | Sim (configuradas). | `--tentativas 5`; `retry.tentativas=5`. | Backoff robusto aplicado. |
| 4. Foi usado backoff maior? | Sim. | `--base-backoff 2 --jitter-max 1`. | Reduz risco de timeout transitório. |
| 5. ST retornou DataFrame? | Sim. | `eh_dataframe=true`. | ST apto ao mapeamento exploratório. |
| 6. Quantas linhas e colunas foram observadas? | 8867 linhas e 208 colunas. | `numero_linhas` e `numero_colunas`. | Amostra estrutural suficiente para próxima etapa exploratória. |
| 7. Houve campos relacionados a CNES/unidade/município? | Sim, parcialmente. | CNES e CODUFMUN detectados. | Relação nominal preliminar existe. |
| 8. A falha anterior foi superada? | Sim. | 5N.3R obteve sucesso na 1ª tentativa. | Evidência de instabilidade transitória. |
| 9. ST deve entrar na 5N.4? | Sim, exploratoriamente. | `recomendado_para_5n4=true`. | 5N.4 pode incluir ST/LT/SR. |
| 10. Algum dado foi salvo em data_*? | Não. | Escopo e execução controlada. | Conformidade mantida. |
| 11. Algum script R pode ser substituído agora? | Não. Nenhum script R pode ser substituído nesta etapa. | Diretriz metodológica. | R permanece oráculo. |

## 14. Classificação da Etapa 5N.3R
**RETESTE_ST_CONCLUIDO_COM_SUCESSO**.

## 15. Critérios de aceite
- [x] Documento 5N.3R criado.
- [x] ST retestado isoladamente.
- [x] Resultado empírico registrado.
- [x] Nenhum dado salvo em data_*.
- [x] Nenhum script Python alterado.
- [x] Nenhum teste Python alterado.
- [x] Nenhum script R alterado.
- [x] Nenhum metadado alterado.
- [x] Nenhum docs/cnes alterado.
- [x] Nenhum workflow alterado.
- [x] Recomendação para 5N.4 atualizada.

## 16. Conclusão
ST funcionou no reteste controlado e a falha anterior mostrou-se transitória (rede). ST pode entrar na 5N.4 junto com LT e SR, em escopo exploratório. A 5N.4 pode seguir como trilha completa de mapeamento estrutural (não validação final), mantendo R como oráculo e sem migração/substituição nesta etapa.
