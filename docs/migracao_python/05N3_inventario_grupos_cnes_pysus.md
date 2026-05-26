# Etapa 5N.3 — inventário dos grupos CNES disponíveis e de interesse no PySUS

## 1. Objetivo
Inventariar grupos CNES aceitos/disponíveis/interessantes no PySUS antes de fixar ST, LT e SR como escopo. Esta etapa não é migração plena, não gera base, não salva dados, não substitui R, não aplica transformação e não aplica classificação de habilitações.

## 2. Justificativa
ST/LT/SR vêm do script local funcional e devem ser tratados como candidatos iniciais, não lista fechada.

## 3. Contexto herdado
5N reconheceu `from pysus import cnes`; 5N.1 resolveu lock DuckDB com isolamento; 5N.2 diagnosticou instabilidade transitória de rede e adotou retry/backoff/jitter.

## 4. Ambiente usado
- branch: `work`
- commit HEAD (início da correção): `e6ab54f9234333a59c5f450413bf732d95e36504`
- último commit: `e6ab54f feat(migracao): inventariar grupos CNES via pysus`
- Python: 3.12.3
- PySUS: 2.0.4
- status inicial/final: validado com `git status --short`.

## 5. Arquivos criados/alterados
- docs/migracao_python/05N3_inventario_grupos_cnes_pysus.md
- python/observatorio_sus/extract/inventariar_grupos_cnes_pysus.py
- tests/python/test_inventariar_grupos_cnes_pysus_cli.py

Sem alterações em scripts/testes R, `data_*`, `metadata`, `docs/cnes`, workflows.

## 6. Grupos candidatos iniciais
- ST = estabelecimentos
- LT = leitos
- SR = serviços/classificação

## 7. Grupos detectados por inspeção da API
A inspeção de assinatura/docstring da função `cnes` não identificou lista oficial completa de grupos. Resultado: `grupos_detectados_por_inspecao.grupos = []`, assinatura com parâmetro `group` e docstring curta (“Fetch CNES health facilities for a state, year, month, and group.”). Portanto, ST/LT/SR permanecem candidatos operacionais iniciais. Limitação: inspeção sem download não garante exaustividade.

## 8. Teste dos grupos candidatos
Comando executado:
`python python/observatorio_sus/extract/inventariar_grupos_cnes_pysus.py --uf ES --ano 2024 --mes 1 --modo testar_grupos --tentativas 3 --base-backoff 1 --jitter-max 0.5`

| Grupo | Origem | Chamada aceita? | DataFrame? | Linhas | Colunas | Campos-chave detectados | Causa/erro | Interesse metodológico | Nível de evidência |
|---|---|---|---|---:|---:|---|---|---|---|
| ST | Script local funcional | Não (falha de rede em 3 tentativas) | Não | 0 | 0 | nenhum | ERRO_DE_REDE (ReadTimeout) | INCONCLUSIVO | INCONCLUSIVO |
| LT | Script local funcional | Sim | Sim | 1014 | 28 | cnes, leito, uf | GRUPO_ACEITO_COM_RETORNO | ALTO_INTERESSE | EVIDENCIA_MODERADA |
| SR | Script local funcional | Sim | Sim | 20699 | 32 | cnes, uf | GRUPO_ACEITO_COM_RETORNO | ALTO_INTERESSE | EVIDENCIA_MODERADA |

### 8.1 Colunas retornadas por grupo
- **ST**: sem colunas (falha controlada de rede).
- **LT**: CNES, CODUFMUN, REGSAUDE, MICR_REG, DISTRSAN, DISTRADM, TPGESTAO, PF_PJ, CPF_CNPJ, NIV_DEP, CNPJ_MAN, ESFERA_A, ATIVIDAD, RETENCAO, NATUREZA, CLIENTEL, TP_UNID, TURNO_AT, NIV_HIER, TERCEIRO, TP_LEITO, CODLEITO, QT_EXIST, QT_CONTR, QT_SUS, QT_NSUS, COMPETEN, NAT_JUR.
- **SR**: CNES, CODUFMUN, SERV_ESP, CLASS_SR, SRVUNICO, REGSAUDE, MICR_REG, DISTRSAN, DISTRADM, TPGESTAO, PF_PJ, CPF_CNPJ, NIV_DEP, ESFERA_A, ATIVIDAD, RETENCAO, NATUREZA, CLIENTEL, TP_UNID, TURNO_AT, NIV_HIER, TERCEIRO, CNPJ_MAN, CARACTER, AMB_NSUS, AMB_SUS, HOSP_NSUS, HOSP_SUS, COMPETEN, CONTSRVU, CNESTERC, NAT_JUR.

### 8.2 Campos-chave detectados por grupo
| Grupo | Campos-chave detectados | Interpretação |
|---|---|---|
| ST | nenhum | Inconclusivo por falha de rede. |
| LT | cnes, leito, uf | Grupo funcional e relevante para mapeamento exploratório de leitos. |
| SR | cnes, uf | Grupo funcional e relevante para mapeamento exploratório de serviços/classificação. |

## 9. Relação com contratos CNES
| Grupo | Relação nominal com contratos | Campos contratuais encontrados literalmente | Campos aproximados | Cobertura potencial | Observação |
|---|---|---|---|---|---|
| ST | NAO_AVALIADA | nenhum | nenhum | COBERTURA_INCONCLUSIVA | Falha de rede impediu avaliação nominal. |
| LT | NOMINAL_APROXIMADA | nenhum literal crítico | cnes, leito | COBERTURA_POTENCIAL_PARCIAL | Relação preliminar; sem paridade com R. |
| SR | NOMINAL_APROXIMADA | nenhum literal crítico | cnes | COBERTURA_POTENCIAL_PARCIAL | Relação preliminar; sem validação contratual plena. |

### 9.1 Lacunas frente aos contratos da Etapa 4
Os contratos da Etapa 4 abrangem, entre outros: `tbEstabelecimento`, `tbMunicipio`, `rlEstabSubTipo`, `tbSubTipo`, `rlEstabAtendPrestConv`, `tbAtendimentoPrestado`, `tbConvenio`, `tbTipoEstabelecimento`, `tbNaturezaJuridica`, `tbGestao`, `rlEstabSipac`, `tbSubGruposHabilitacao`, `base_estabelecimentos`. A 5N.3 não comprova cobertura completa dessas tabelas; apenas identifica grupos candidatos para mapeamento estrutural.

## 10. Grupos recomendados para mapeamento na próxima etapa
Recomendação explícita: **LT e SR** para 5N.4 em caráter exploratório, porque retornaram DataFrame e foram classificados como ALTO_INTERESSE com EVIDENCIA_MODERADA. **ST** ficou inconclusivo nesta execução por ERRO_DE_REDE e requer reteste controlado. A recomendação não implica cobertura integral de contratos nem substituição de R.

## 11. Testes Python executados
`python -m pytest tests/python` (29 passed), sem teste de rede nos testes unitários desta etapa, sem escrita em `data_*`.

## 12. Perguntas obrigatórias
| Pergunta | Resposta | Evidência | Implicação |
|---|---|---|---|
| 1. A cadeia 5N/5N.1/5N.2 existia? | Sim. | Presença dos três documentos. | Pré-condição atendida. |
| 2. ST/LT/SR foram tratados como candidatos, não como lista fechada? | Sim. | `grupos_candidatos_iniciais.observacao`. | Governança metodológica mantida. |
| 3. A API PySUS indicou lista de grupos? | Não, lista oficial completa não identificada. | `grupos_detectados_por_inspecao.grupos = []`. | Pode exigir 5N.3A. |
| 4. Algum grupo adicional foi identificado? | Não. | Inspeção da API. | Mantém ST/LT/SR como candidatos operacionais iniciais. |
| 5. ST foi testado? | Sim. | Resultado por grupo. | Resultado inconclusivo por rede. |
| 6. LT foi testado? | Sim. | Resultado por grupo. | Apto a mapeamento exploratório. |
| 7. SR foi testado? | Sim. | Resultado por grupo. | Apto a mapeamento exploratório. |
| 8. Quais grupos retornaram DataFrame? | LT e SR. | `eh_dataframe = true` em LT/SR. | Há base para decisão parcial. |
| 9. Quais grupos têm interesse metodológico alto? | LT e SR. | `interesse_metodologico = ALTO_INTERESSE`. | Recomendação parcial para 5N.4. |
| 10. Há relação preliminar com contratos CNES? | Sim, nominal aproximada (LT/SR). | Seção 9. | Não é validação final. |
| 11. Algum dado foi salvo em data_*? | Não. | Escopo e execução. | Conformidade. |
| 12. Algum script R pode ser substituído agora? | Não. Nenhum script R pode ser substituído nesta etapa. | Regra metodológica. | R permanece oráculo. |

## 13. Classificação da Etapa 5N.3
**INVENTARIO_GRUPOS_CONCLUIDO_COM_RESSALVAS**.

Justificativa: houve inventário e evidência empírica para LT/SR, mas ST ficou inconclusivo por erro de rede e a lista oficial completa de grupos não foi identificada.

## 14. Implicações para próxima etapa
A autorização de 5N.4 é **exploratória** e **parcial** para LT e SR. Escopo: mapeamento estrutural (colunas, dtypes e relações nominais preliminares), sem extração histórica, sem substituição de R e mantendo proibição de salvar dados em `data_*`.

## 15. Riscos remanescentes
- Lista oficial de grupos não confirmada;
- ST/LT/SR podem não cobrir todo o contrato da Etapa 4;
- relação com contratos é nominal/preliminar;
- necessidade de mapear colunas/dtypes antes de ampliar escopo;
- risco de coerção indevida de códigos;
- necessidade de preservar R como oráculo.

## 16. Critérios de aceite
- [x] Relatório sem “Ver saída JSON” nas seções decisivas.
- [x] Resultados empíricos incorporados.
- [x] Script com justificativa/nível de evidência/relação contratual/cobertura potencial.
- [x] Testes offline atualizados e passando.
- [x] Sem alteração de scripts R, dados, metadados, docs/cnes e workflows.

## 17. Conclusão
Grupos testados: ST, LT e SR. DataFrame retornou para LT e SR; ST foi inconclusivo por falha de rede (ReadTimeout). Grupos recomendados para 5N.4: LT e SR, em natureza exploratória. 5N.3A permanece recomendável caso seja necessário ampliar investigação de grupos oficiais no PySUS.

## 18. Atualização posterior — resultado da Etapa 5N.3R
Após a conclusão da 5N.3, foi executada a Etapa 5N.3R, documentada em:

`docs/migracao_python/05N3R_reteste_controlado_st_cnes_pysus.md`

A 5N.3R retestou exclusivamente o grupo ST com os seguintes parâmetros:

- UF = ES;
- ano = 2024;
- mês = 1;
- grupo = ST;
- 5 tentativas;
- backoff maior;
- jitter maior;
- isolamento de ambiente;
- sem persistência de dados.

Resultado da 5N.3R:

- ST retornou DataFrame;
- 8867 linhas;
- 208 colunas;
- causa: GRUPO_ACEITO_COM_RETORNO;
- classificação da 5N.3R: RETESTE_ST_CONCLUIDO_COM_SUCESSO;
- a falha anterior foi interpretada como instabilidade transitória de rede.

Implicação metodológica da atualização posterior:

- A recomendação original da seção 10 da 5N.3, que autorizava 5N.4 apenas para LT e SR, foi superada pela evidência posterior da 5N.3R.
- A recomendação atualizada é que a Etapa 5N.4 pode incluir ST, LT e SR.
- A inclusão de ST, LT e SR na 5N.4 permanece exploratória.
- A 5N.4 não deve ser tratada como validação contratual plena.
- A 5N.4 não deve gerar base versionada.
- A 5N.4 não deve substituir R.
- R permanece como oráculo metodológico.
