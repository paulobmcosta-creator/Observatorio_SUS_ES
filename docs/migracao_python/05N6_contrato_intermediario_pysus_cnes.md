# Etapa 5N.6 — contrato intermediário PySUS→CNES

## 1. Objetivo
Desenhar um contrato intermediário entre a estrutura PySUS observada (ST/LT/SR) e os contratos CNES existentes no legado metodológico.

Esta etapa:
- não gera base;
- não baixa dados;
- não salva dados observacionais;
- não substitui R;
- não valida paridade;
- não aplica classificação de habilitações.

## 2. Contexto herdado
- 5N reconheceu API funcional;
- 5N.1 resolveu lock DuckDB;
- 5N.2 estabilizou retry/backoff/jitter;
- 5N.3 inventariou grupos;
- 5N.3R confirmou ST;
- 5N.4 mapeou estrutura de ST/LT/SR;
- 5N.5 confirmou estabilidade multi-competência.

## 3. Justificativa do contrato intermediário
A estabilidade de colunas e dtypes não é suficiente para migração. É necessário explicitar equivalências entre colunas PySUS e campos metodológicos/contratuais CNES antes de qualquer transformação relacional.

## 4. Artefatos criados
- docs/migracao_python/05N6_contrato_intermediario_pysus_cnes.md
- python/observatorio_sus/cnes/contrato_intermediario_pysus_cnes.py
- metadata/cnes/contrato_intermediario_pysus_cnes.csv
- tests/python/test_contrato_intermediario_pysus_cnes.py

Sem alterações em scripts R, testes R, data_raw, data_interim, data_processed, metadata/cnes já existente, docs/cnes e workflows.

## 5. Grupos cobertos pelo contrato intermediário
| Grupo PySUS | Descrição | Situação |
|---|---|---|
| ST | estabelecimentos | coberto no contrato intermediário |
| LT | leitos | coberto no contrato intermediário |
| SR | serviços/classificação | coberto no contrato intermediário |

## 6. Campos observados por grupo
### 6.1 ST — estabelecimentos
CNES, CODUFMUN, COD_CEP, CPF_CNPJ, PF_PJ, NIV_DEP, CNPJ_MAN, TPGESTAO, COMPETEN, NAT_JUR, ESFERA_A, ATIVIDAD, RETENCAO, NATUREZA, CLIENTEL, TP_UNID, TURNO_AT, NIV_HIER, TERCEIRO.

### 6.2 LT — leitos
CNES, CODUFMUN, REGSAUDE, MICR_REG, DISTRSAN, DISTRADM, TPGESTAO, PF_PJ, CPF_CNPJ, NIV_DEP, CNPJ_MAN, ESFERA_A, ATIVIDAD, RETENCAO, NATUREZA, CLIENTEL, TP_UNID, TURNO_AT, NIV_HIER, TERCEIRO, TP_LEITO, CODLEITO, QT_EXIST, QT_CONTR, QT_SUS, QT_NSUS, COMPETEN, NAT_JUR.

### 6.3 SR — serviços/classificação
CNES, CODUFMUN, SERV_ESP, CLASS_SR, SRVUNICO, REGSAUDE, MICR_REG, DISTRSAN, DISTRADM, TPGESTAO, PF_PJ, CPF_CNPJ, NIV_DEP, ESFERA_A, ATIVIDAD, RETENCAO, NATUREZA, CLIENTEL, TP_UNID, TURNO_AT, NIV_HIER, TERCEIRO, CNPJ_MAN, CARACTER, AMB_NSUS, AMB_SUS, HOSP_NSUS, HOSP_SUS, COMPETEN, CONTSRVU, CNESTERC, NAT_JUR.

## 7. Matriz de equivalência inicial
| Grupo | Coluna PySUS | Campo contrato CNES | Campo legado R | Tipo equivalência | Status | Papel metodológico | Preservar texto | Risco coerção |
|---|---|---|---|---|---|---|---|---|
| ST/LT/SR | CNES | CO_CNES | cnes | NOMINAL_APROXIMADA | POTENCIAL_A_CONFIRMAR | CHAVE_PUBLICA | sim | sim |
| ST/LT/SR | CODUFMUN | CO_MUNICIPIO_GESTOR | co_municipio_gestor | SEMANTICA_POTENCIAL | POTENCIAL_A_CONFIRMAR | TERRITORIO | sim | sim |
| ST/LT/SR | COMPETEN | competencia | competencia | NOMINAL_APROXIMADA | CONFIRMADA_NOMINALMENTE | COMPETENCIA | sim | sim |
| ST/LT/SR | TPGESTAO | TP_GESTAO | tp_gestao | NOMINAL_APROXIMADA | POTENCIAL_A_CONFIRMAR | GESTAO | sim | sim |
| ST/LT/SR | NAT_JUR | natureza_juridica | nat_jur | NOMINAL_APROXIMADA | POTENCIAL_A_CONFIRMAR | NATUREZA_JURIDICA | sim | sim |
| ST | CPF_CNPJ | cpf_cnpj | cpf_cnpj | NOMINAL_APROXIMADA | POTENCIAL_A_CONFIRMAR | IDENTIFICADOR_PESSOA_JURIDICA | sim | sim |
| ST/SR | CNPJ_MAN | cnpj_mantenedora | cnpj_man | NOMINAL_APROXIMADA | POTENCIAL_A_CONFIRMAR | IDENTIFICADOR_PESSOA_JURIDICA | sim | sim |
| LT | CODLEITO | codigo_leito | codleito | NOMINAL_APROXIMADA | POTENCIAL_A_CONFIRMAR | OFERTA_LEITOS | sim | sim |
| LT | TP_LEITO | tipo_leito | tp_leito | NOMINAL_APROXIMADA | POTENCIAL_A_CONFIRMAR | OFERTA_LEITOS | sim | sim |
| LT | QT_EXIST | qt_existente | qt_exist | NOMINAL_APROXIMADA | POTENCIAL_A_CONFIRMAR | OFERTA_LEITOS | não | não |
| LT | QT_SUS | qt_sus | qt_sus | NOMINAL_APROXIMADA | POTENCIAL_A_CONFIRMAR | OFERTA_LEITOS | não | não |
| LT | QT_NSUS | qt_nsus | qt_nsus | NOMINAL_APROXIMADA | POTENCIAL_A_CONFIRMAR | OFERTA_LEITOS | não | não |
| SR | SERV_ESP | servico_especializado | serv_esp | NOMINAL_APROXIMADA | POTENCIAL_A_CONFIRMAR | OFERTA_SERVICOS | sim | sim |
| SR | CLASS_SR | classificacao_servico | class_sr | NOMINAL_APROXIMADA | POTENCIAL_A_CONFIRMAR | CLASSIFICACAO_SERVICO | sim | sim |
| SR | AMB_SUS | amb_sus | amb_sus | NOMINAL_APROXIMADA | POTENCIAL_A_CONFIRMAR | OFERTA_SERVICOS | não | não |
| SR | HOSP_SUS | hosp_sus | hosp_sus | NOMINAL_APROXIMADA | POTENCIAL_A_CONFIRMAR | OFERTA_SERVICOS | não | não |
| SR | CNESTERC | cnes_terceiro | cnesterc | NOMINAL_APROXIMADA | POTENCIAL_A_CONFIRMAR | IDENTIFICADOR_PESSOA_JURIDICA | sim | sim |

## 8. Tratamento da ausência de CO_UNIDADE
- CO_UNIDADE não apareceu literalmente nos grupos PySUS observados;
- CNES não deve ser automaticamente tratado como CO_UNIDADE;
- joins relacionais por co_unidade ainda não podem ser substituídos;
- R continua necessário como oráculo para chaves relacionais;
- esta pendência bloqueia substituição de bases finais de estabelecimentos/habilitações.

## 9. Regras de preservação textual
Devem permanecer como texto: CNES, CODUFMUN, COMPETEN, TPGESTAO, NAT_JUR, CPF_CNPJ, CNPJ_MAN, CNESTERC, qualquer campo COD/CO/CPF/CNPJ e outros identificadores administrativos.

## 10. Limitações do contrato intermediário
Não é contrato final; não é paridade com R; não valida qualidade de dados; não valida relações; não resolve CO_UNIDADE; não trata habilitações; não substitui metadata/cnes/classificacao_habilitacoes_cnes.csv.

## 11. Testes Python executados
pytest em `tests/python` e pytest específico do novo módulo, ambos com sucesso. Não houve acesso de rede nos testes e não houve escrita em `data_raw`, `data_interim` ou `data_processed`.

## 12. Perguntas obrigatórias
| Pergunta | Resposta | Evidência | Implicação |
|---|---|---|---|
| 1. A cadeia 5N até 5N.5 existia? | Sim | verificações `test -f` | pré-condição atendida |
| 2. O contrato intermediário foi criado? | Sim | módulo Python + documento | estrutura formal criada |
| 3. O CSV de metadados foi criado? | Sim | `metadata/cnes/contrato_intermediario_pysus_cnes.csv` | matriz tabular disponível |
| 4. O módulo Python importa sem rede? | Sim | testes unitários | uso offline possível |
| 5. ST está coberto? | Sim | grupos e campos ST | cobertura mínima ST atendida |
| 6. LT está coberto? | Sim | grupos e campos LT | cobertura mínima LT atendida |
| 7. SR está coberto? | Sim | grupos e campos SR | cobertura mínima SR atendida |
| 8. CNES foi mapeado? | Sim | matriz de equivalências | chave pública registrada |
| 9. CODUFMUN foi mapeado? | Sim | matriz de equivalências | território registrado |
| 10. COMPETEN foi mapeado? | Sim | matriz de equivalências | competência registrada |
| 11. Campos de leitos foram mapeados? | Sim | CODLEITO/TP_LEITO/QT_* | oferta de leitos mapeada |
| 12. Campos de serviços/classificação foram mapeados? | Sim | SERV_ESP/CLASS_SR/AMB_SUS/HOSP_SUS/CNESTERC | oferta/classificação mapeada |
| 13. CO_UNIDADE foi resolvido? | Não | linha explícita de inconclusão | pendência bloqueante mantida |
| 14. Há regras de preservação textual? | Sim | seção 9 + matriz | redução de risco de coerção |
| 15. Algum dado observacional foi salvo? | Não | escopo da etapa + artefatos | sem materialização CNES |
| 16. Algum script R pode ser substituído agora? | Não. Nenhum script R pode ser substituído nesta etapa. | conclusão metodológica | R permanece oráculo |

## 13. Classificação da Etapa 5N.6
CONTRATO_INTERMEDIARIO_CRIADO_COM_RESSALVAS.

## 14. Implicações para próxima etapa
Recomendar Etapa 5N.7: protótipo de transformação em memória para ST/LT/SR (sem persistência) com renomeação controlada e preservação textual; ou investigação específica da ausência de CO_UNIDADE antes de qualquer base final.

Não recomendar extração histórica 2008–2024, geração de base ou substituição de R.

## 15. Riscos remanescentes
Ausência de CO_UNIDADE; equivalências nominais/semânticas potenciais; risco de coerção; necessidade de validação com R; necessidade de validação humana; risco de assumir CNES como chave operacional indevida.

## 16. Critérios de aceite
- [x] Documento 5N.6 criado.
- [x] Módulo de contrato intermediário criado.
- [x] CSV de metadados criado.
- [x] Testes criados.
- [x] Testes executados.
- [x] ST coberto.
- [x] LT coberto.
- [x] SR coberto.
- [x] CNES/CODUFMUN/COMPETEN mapeados.
- [x] CO_UNIDADE registrado como inconclusivo.
- [x] Regras de preservação textual registradas.
- [x] Nenhum dado observacional salvo.
- [x] Nenhum script R alterado.
- [x] Nenhum metadado existente alterado.
- [x] Nenhum docs/cnes alterado.
- [x] Nenhum workflow alterado.

## 17. Conclusão
Contrato intermediário criado com cobertura ST/LT/SR. CO_UNIDADE permanece pendência. R permanece oráculo para chaves relacionais. Próxima etapa deve focar transformação em memória ou investigação da chave, sem geração de base.
