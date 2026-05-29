# Etapa 5N.7-8 — transformação em memória multi-competência PySUS→CNES

## 1. Objetivo
Esta etapa criou um protótipo de transformação experimental **somente em memória** para os grupos CNES `ST`, `LT` e `SR` nas competências `2024-01`, `2024-06` e `2024-12`, usando a API pública funcional do PySUS:

```python
from pysus import cnes
cnes(state=uf, year=ano, month=mes, group=grupo)
```

A etapa não gera base, não salva dados, não substitui R, não faz join relacional, não cria `CO_UNIDADE`, não valida paridade com R e não aplica classificação de habilitações.

## 2. Contexto herdado
A execução parte da cadeia 5N até 5N.5, que reconheceu a API funcional, isolou o ambiente PySUS/CNES, diagnosticou instabilidade transitória de rede e mapeou estruturalmente ST/LT/SR em competências piloto. A etapa 5N.6 criou o contrato intermediário PySUS→CNES, e a etapa 5N.6R registrou a deliberação humana que autorizou transformação exploratória em memória, sem substituição do R.

## 3. Decisões humanas aplicadas
- O contrato intermediário é mínimo e não exaustivo.
- `CNES` não substitui `CO_UNIDADE`.
- A ausência de `CO_UNIDADE` bloqueia bases finais relacionais, mas permite transformação em memória.
- `CODUFMUN`, `COMPETEN`, `TPGESTAO`, `NAT_JUR` e `CNESTERC` recebem preservação textual quando há DataFrame retornado.
- `QT_*` permanece numérico se já vier numérico; se vier textual, não é coercido.
- Nenhum script R foi substituído ou alterado.

## 4. Ambiente usado
| Item | Valor |
|---|---|
| Branch | `work` |
| Commit de referência antes deste ajuste | `d332e8ba86d5ea676767380c755a771fe5eca88c` |
| Python usado no teste obrigatório | `Python 3.12.3` |
| PySUS | instalado por `requirements-python-poc.txt` |
| Status | apenas arquivos permitidos da etapa Python/documentação foram alterados |

## 5. Arquivos criados/alterados
Arquivos desta etapa e do ajuste 5N.7-8A:
- `docs/migracao_python/05N7_8_transformacao_memoria_multicompetencia_cnes_pysus.md`
- `docs/migracao_python/05N7_8A_validacao_minima_transformacao_memoria_cnes_pysus.md`
- `python/observatorio_sus/transform/transformar_memoria_multicompetencia_cnes_pysus.py`
- `tests/python/test_transformar_memoria_multicompetencia_cnes_pysus_cli.py`

Confirmado por escopo: não houve alteração intencional em scripts R, testes R, `data_raw`, `data_interim`, `data_processed`, metadados existentes, `docs/cnes`, workflows, `.gitignore` ou `.gitattributes`.

## 6. Parâmetros
| Parâmetro | Valor padrão após ajuste |
|---|---:|
| UF | `ES` |
| Ano | `2024` |
| Meses padrão | `1`, `6`, `12` |
| Grupos padrão | `ST`, `LT`, `SR` |
| Tentativas | `5` |
| Backoff | `2` |
| Jitter | `1` |
| Timeout por chamada | `300` segundos |
| Timeout global | `1800` segundos |
| Isolamento | `HOME`, `XDG_CONFIG_HOME` e `XDG_CACHE_HOME` temporários |
| Persistência | ausente |

## 7. Regras de transformação em memória
- Renomeação controlada pelo contrato intermediário quando `status_equivalencia` for `CONFIRMADA_NOMINALMENTE` ou `POTENCIAL_A_CONFIRMAR`, `tipo_equivalencia` não for `AUSENTE_NO_PYSUS`, a coluna existir no DataFrame e o destino não for `CO_UNIDADE`.
- Preservação textual em memória para `CNES`, `CODUFMUN`, `COMPETEN`, `TPGESTAO`, `NAT_JUR`, `CPF_CNPJ`, `CNPJ_MAN`, `CNESTERC`, `COD*`, `CO_*`, `CPF*` e `CNPJ*`.
- `QT_*` não é convertido para texto por regra geral e não é forçado para numérico quando vier textual.
- `competencia_normalizada` pode ser criada apenas em memória quando `COMPETEN` existir.
- É proibido criar `CO_UNIDADE`, renomear `CNES` para `CO_UNIDADE`, executar join relacional ou persistir dados.
- O timeout controlado foi **mantido** como salvaguarda, agora parametrizado por `--timeout-por-chamada` e `--timeout-global`.

## 8. Resultado geral por grupo e competência
A tentativa multi-competência completa anterior retornou `TIMEOUT_CONTROLADO` nas 9 combinações. Isso significa que a transformação multi-competência **não foi avaliada operacionalmente**: nenhum DataFrame retornou a tempo para aplicação e validação da transformação.

| Grupo | Competência | Sucesso? | Linhas antes | Linhas depois | Colunas antes | Colunas depois | Renomeações | Timeout? | Persistiu dados? |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| ST | 2024-01 | Não | - | - | 0 | 0 | 0 | Sim | Não |
| ST | 2024-06 | Não | - | - | 0 | 0 | 0 | Sim | Não |
| ST | 2024-12 | Não | - | - | 0 | 0 | 0 | Sim | Não |
| LT | 2024-01 | Não | - | - | 0 | 0 | 0 | Sim | Não |
| LT | 2024-06 | Não | - | - | 0 | 0 | 0 | Sim | Não |
| LT | 2024-12 | Não | - | - | 0 | 0 | 0 | Sim | Não |
| SR | 2024-01 | Não | - | - | 0 | 0 | 0 | Sim | Não |
| SR | 2024-06 | Não | - | - | 0 | 0 | 0 | Sim | Não |
| SR | 2024-12 | Não | - | - | 0 | 0 | 0 | Sim | Não |

## 9. Colunas renomeadas
| Grupo | Coluna original PySUS | Coluna transformada | Tipo equivalência | Observação |
|---|---|---|---|---|
| ST/LT/SR | - | - | - | Nenhuma renomeação foi validada porque as chamadas operacionais não retornaram DataFrames antes do timeout. |

## 10. Preservação textual
As regras de preservação textual estão implementadas no script, mas não foram validadas operacionalmente na execução multi-competência completa porque todas as combinações retornaram timeout controlado.

## 11. Campos quantitativos QT_*
As regras para `QT_*` estão implementadas no script, mas não foram validadas operacionalmente na execução multi-competência completa porque não houve DataFrame retornado.

## 12. Campos pendentes e não transformados
Permanecem pendentes: `CO_UNIDADE`, equivalências ausentes, campos fora do contrato intermediário e campos mantidos sem renomeação. `CO_UNIDADE` não foi criado artificialmente.

## 13. Validações internas
| Validação | Resultado | Observação |
|---|---|---|
| Linhas antes = depois | Não avaliado | DataFrames não retornaram antes do timeout. |
| `CO_UNIDADE` não criado | Aprovado | Campo não foi criado pelo script. |
| Join não executado | Aprovado | Não há rotina de join. |
| `data_*` não alterado | Aprovado | O script não contém escrita em `data_raw`, `data_interim` ou `data_processed`. |
| R não substituído | Aprovado | Nenhum script R foi alterado. |
| Timeout controlado mantido | Aprovado | O timeout impede travamento indefinido e preserva saída auditável. |

## 14. Testes Python executados
- `python -m pytest tests/python`: suíte Python executada no ambiente Python 3.12.3.
- O modo planejamento não acessou rede.
- Os testes Python não escreveram em `data_*`.
- O ajuste 5N.7-8A executa validação mínima com `LT 2024-01` antes de qualquer nova tentativa multi-competência.

## 15. Perguntas obrigatórias
| Pergunta | Resposta | Evidência | Implicação |
|---|---|---|---|
| A cadeia 5N até 5N.6R existia? | Sim. | `test -f` obrigatório retornou sucesso para todos os arquivos. | Cadeia documental completa. |
| As 9 combinações foram transformadas em memória? | Não. | Todas retornaram `TIMEOUT_CONTROLADO`. | Etapa multi-competência não avaliada operacionalmente. |
| Alguma combinação falhou? | Sim. | 9 timeouts controlados. | Exige validação mínima em escopo reduzido. |
| Linhas antes e depois permaneceram iguais? | Não avaliado. | Não houve DataFrame retornado. | Sem inferência de paridade estrutural. |
| CNES foi preservado como texto? | Não avaliado. | Não houve DataFrame retornado. | Regra implementada, mas não exercida com sucesso. |
| CODUFMUN foi preservado como texto? | Não avaliado. | Não houve DataFrame retornado. | Regra implementada, mas não exercida com sucesso. |
| COMPETEN foi preservado como texto? | Não avaliado. | Não houve DataFrame retornado. | Regra implementada, mas não exercida com sucesso. |
| TPGESTAO/NAT_JUR foram preservados como texto? | Não avaliado. | Não houve DataFrame retornado. | Regra implementada, mas não exercida com sucesso. |
| QT_* permaneceram numéricos quando aplicável? | Não avaliado. | Não houve DataFrame retornado. | Regra implementada, mas não exercida com sucesso. |
| CNESTERC recebeu tratamento textual? | Não avaliado. | Não houve DataFrame retornado. | Regra implementada, mas não exercida com sucesso. |
| CO_UNIDADE foi criado? | Não. | Resultado JSON mantém `co_unidade_criado=false`. | Salvaguarda preservada. |
| Algum join relacional foi executado? | Não. | Resultado JSON mantém `join_relacional_executado=false`. | Salvaguarda preservada. |
| Algum dado foi salvo em data_*? | Não. | Resultado JSON mantém `persistiu_dados=false`. | Sem persistência. |
| Algum script R pode ser substituído agora? | Não. Nenhum script R pode ser substituído nesta etapa. | Deliberação 5N.6R e resultado não avaliado por timeout. | R permanece oráculo. |
| A transformação pode ser revista para comparação com R? | Sim, somente após validação operacional mínima. | Etapa 5N.7-8A. | Comparação futura, não nesta etapa. |

## 16. Classificação da Etapa 5N.7-8
Classificação corrigida: `TRANSFORMACAO_MEMORIA_MULTICOMPETENCIA_NAO_AVALIADA_POR_TIMEOUT`.

Essa classificação substitui qualquer leitura anterior de conclusão: como todos os resultados operacionais foram timeout, a transformação multi-competência não foi avaliada.

## 17. Implicações para próxima etapa
Recomenda-se a etapa 5N.7-8A — validação mínima da transformação em memória PySUS→CNES:
- iniciar com `LT 2024-01`;
- manter timeout controlado parametrizável;
- se `LT 2024-01` funcionar, testar `ST/LT/SR 2024-01`;
- se continuar timeout, investigar desempenho/ambiente PySUS antes de nova transformação.

Não se recomenda ainda geração de base, escrita em `data_interim`, extração histórica, classificação de habilitações ou substituição de R.

## 18. Riscos remanescentes
- `CO_UNIDADE` permanece pendente.
- Equivalências do contrato são mínimas e não exaustivas.
- Campos fora do contrato não foram avaliados.
- Há risco residual de coerção se as regras forem alteradas sem revisão.
- Não houve comparação com R.
- Não houve validação humana pós-transformação efetiva.
- A API/rede PySUS/CNES permanece sujeita a timeout no ambiente atual.

## 19. Critérios de aceite
- [x] Documento criado.
- [x] Script criado.
- [x] Testes criados.
- [x] Testes executados.
- [ ] 9 combinações processadas em memória com sucesso.
- [x] 9 combinações registradas com timeout controlado quando a API não retornou.
- [x] Nenhum dado salvo.
- [ ] Linhas preservadas avaliadas em DataFrames reais.
- [x] `CO_UNIDADE` não criado.
- [x] Join não executado.
- [ ] Identificadores preservados como texto em DataFrames reais.
- [ ] `QT_*` não convertidos indevidamente em DataFrames reais.
- [x] Nenhum script R alterado.
- [x] Nenhum metadado existente alterado.
- [x] Nenhum `docs/cnes` alterado.
- [x] Nenhum workflow alterado.

## 20. Conclusão
O timeout controlado foi mantido e parametrizado. A execução multi-competência completa da 5N.7-8 deve ser classificada como `TRANSFORMACAO_MEMORIA_MULTICOMPETENCIA_NAO_AVALIADA_POR_TIMEOUT`, pois as 9 combinações retornaram timeout e nenhum DataFrame foi transformado. A próxima etapa é a validação mínima 5N.7-8A em escopo reduzido, sem persistência, sem criação de `CO_UNIDADE`, sem join relacional e sem substituição de R.

## Nota pós-5N.7-8E
A etapa 5N.7-8E corrigiu o caminho padrão do modo `transformar_memoria`: a chamada direta sem subprocesso passou a ser o padrão operacional, e o subprocesso permaneceu disponível apenas como proteção opcional via `--usar-subprocesso`. A correção não altera a proibição de persistência, criação de `CO_UNIDADE`, join relacional ou substituição de R.
