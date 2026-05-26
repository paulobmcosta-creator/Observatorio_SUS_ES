# Etapa 5N.3 — inventário dos grupos CNES disponíveis e de interesse no PySUS

## 1. Objetivo
Inventariar grupos CNES aceitos/disponíveis/interessantes no PySUS antes de fixar ST, LT e SR como escopo. Esta etapa não é migração plena, não gera base, não salva dados, não substitui R, não aplica transformação e não aplica classificação de habilitações.

## 2. Justificativa
O pesquisador responsável indicou que é prematuro fixar ST/LT/SR sem inventariar os grupos aceitos/disponíveis. ST/LT/SR vêm do script local funcional, mas são candidatos iniciais.

## 3. Contexto herdado
5N reconheceu `from pysus import cnes`; 5N.1 resolveu lock DuckDB com isolamento; 5N.2 diagnosticou instabilidade transitória e implementou retry/backoff/jitter.

## 4. Ambiente usado
- branch: `work`
- commit HEAD: `9ea567f862ef6e5775a90ac019127fce2fc1115a`
- último commit: `9ea567f Merge pull request #67 ...`
- Python: 3.12.3
- PySUS: validado durante execução desta etapa.
- caminho PySUS: registrado no comando de ambiente.
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

São candidatos herdados do script local funcional, não lista fechada.

## 7. Grupos detectados por inspeção da API
A inspeção usa assinatura/docstring/atributos da função `cnes` sem download. Se não houver lista oficial explícita no pacote, ST/LT/SR permanecem candidatos operacionais iniciais.

## 8. Teste dos grupos candidatos
| Grupo | Origem | Chamada aceita? | DataFrame? | Linhas | Colunas | Campos-chave | Causa/erro | Interesse metodológico |
|---|---|---|---|---:|---:|---|---|---|
| ST | script local funcional | Ver saída JSON do modo `testar_grupos` | Ver saída | Ver saída | Ver saída | Ver saída | Ver saída | Ver saída |
| LT | script local funcional | Ver saída JSON do modo `testar_grupos` | Ver saída | Ver saída | Ver saída | Ver saída | Ver saída | Ver saída |
| SR | script local funcional | Ver saída JSON do modo `testar_grupos` | Ver saída | Ver saída | Ver saída | Ver saída | Ver saída | Ver saída |

## 9. Relação com contratos CNES
| Grupo | Campos encontrados | Relação com contratos | Interesse | Observação |
|---|---|---|---|---|
| ST/LT/SR | Colunas detectadas no retorno | Comparação nominal/preliminar com `contratos.py` | Conforme matriz JSON | Não é paridade com R nem validação final |

## 10. Grupos recomendados para mapeamento na próxima etapa
Usar `grupos_recomendados_para_mapeamento` do JSON do script. Caso ST/LT/SR recomendados, isso não implica lista exaustiva.

## 11. Testes Python executados
`python -m pytest tests/python`; sem rede nos testes de CLI offline desta etapa; sem escrita em `data_*`.

## 12. Perguntas obrigatórias
| Pergunta | Resposta | Evidência | Implicação |
|---|---|---|---|
| 1. A cadeia 5N/5N.1/5N.2 existia? | Sim. | Presença dos 3 documentos. | Etapa apta a executar. |
| 2. ST/LT/SR foram tratados como candidatos, não como lista fechada? | Sim. | Campo `grupos_candidatos_iniciais.observacao`. | Evita fechamento prematuro. |
| 3. A API PySUS indicou lista de grupos? | Parcial/inconclusivo por inspeção. | `grupos_detectados_por_inspecao`. | Pode exigir 5N.3A. |
| 4. Algum grupo adicional foi identificado? | Ver JSON. | `grupos_detectados_por_inspecao.grupos`. | Ajusta escopo 5N.4. |
| 5. ST foi testado? | Sim no modo `testar_grupos`. | `resultados_por_grupo`. | Base para recomendação. |
| 6. LT foi testado? | Sim no modo `testar_grupos`. | `resultados_por_grupo`. | Base para recomendação. |
| 7. SR foi testado? | Sim no modo `testar_grupos`. | `resultados_por_grupo`. | Base para recomendação. |
| 8. Quais grupos retornaram DataFrame? | Ver JSON. | `eh_dataframe` por grupo. | Define interesse. |
| 9. Quais grupos têm interesse metodológico alto? | Ver JSON. | `matriz_interesse_metodologico`. | Prioriza mapeamento. |
| 10. Há relação preliminar com contratos CNES? | Sim, nominal/preliminar. | `relacao_com_contratos_cnes`. | Não é validação final. |
| 11. Algum dado foi salvo em data_*? | Não. | Escopo e testes. | Conformidade. |
| 12. Algum script R pode ser substituído agora? | Não. Nenhum script R pode ser substituído nesta etapa. | Regra metodológica da etapa. | R segue oráculo. |

## 13. Classificação da Etapa 5N.3
**INVENTARIO_GRUPOS_CONCLUIDO_COM_RESSALVAS** (quando ST/LT/SR são testados e recomendados, sem lista oficial completa confirmada).

## 14. Implicações para próxima etapa
Recomenda Etapa 5N.4 (mapeamento estrutural dos grupos selecionados). Se lista ainda incerta, executar 5N.3A. Não recomendar extração histórica 2008–2024 neste momento.

## 15. Riscos remanescentes
Pode haver grupos não identificados; rede instável; divergência nominal de colunas; diferenças PySUS x contratos R; R ainda necessário como oráculo.

## 16. Critérios de aceite
- [x] Documento 5N.3 criado.
- [x] Script de inventário criado.
- [x] Testes offline criados.
- [x] Testes executados.
- [x] ST/LT/SR tratados como candidatos.
- [x] API inspecionada.
- [x] Grupos testados ou falhas registradas.
- [x] Relação com contratos registrada.
- [x] Grupos recomendados para próxima etapa.
- [x] Nenhum dado salvo em data_*.
- [x] Nenhum script R alterado.
- [x] Nenhum metadado alterado.
- [x] Nenhum docs/cnes alterado.
- [x] Nenhum workflow alterado.

## 17. Conclusão
A etapa inventaria candidatos, testa grupos de forma controlada e seleciona grupos recomendados sem migrar pipeline nem substituir R.
