# Extração mínima temporária CNES/ES/2025 e comparação estrutural com contratos

## 1. Objetivo da Etapa 5
Esta etapa executa **diagnóstico e tentativa de extração mínima temporária controlada** para CNES (UF=ES, competências 202501–202512), comparando estrutura observada com os contratos Python da Etapa 4.

Escopo reafirmado:
- não substitui scripts R;
- não altera `data_raw`, `data_interim` ou `data_processed`;
- não altera `metadata/`;
- não altera `docs/cnes/`;
- não altera workflows;
- não gera produto final;
- não aplica classificação de habilitações;
- R permanece como oráculo metodológico.

## 2. Deliberação humana considerada
A revisão humana pré-Etapa 5 foi considerada conforme `docs/migracao_python/04_deliberacao_humana_pre_etapa5.md`.

Resumo das decisões aplicadas:
- tabelas contratadas da Etapa 4 são suficientes;
- iniciar por estabelecimentos;
- habilitações condicionadas a `CO_UNIDADE` e `CO_CNES` em estabelecimentos;
- ausência de `CO_UNIDADE` bloqueia avanço;
- `CO_CNES` precisa permanecer textual;
- conversão só aceita com evidência de preservação de zeros;
- fallback apenas se PySUS falhar/não expor tabela;
- recorte autorizado UF=ES e ano 2025;
- competências mensais 202501–202512;
- registrar arquivos temporários;
- não escrever em `data_*`;
- não portar scripts R;
- não aplicar classificação de habilitações.

## 3. Ambiente usado
- Branch: `work`
- HEAD: `cd45951ff387f2efeb3b348cffaf9124c96d3449`
- Último commit: `cd45951 Merge pull request #55 from paulobmcosta-creator/codex/registrar-revisao-humana-pre-etapa-5`
- Python: `3.12.3`
- Executável Python: `/workspace/Observatorio_SUS_ES/.venv-etapa5-cnes/bin/python`
- Pip: `26.1.1`
- PySUS: `2.0.4`
- Caminho PySUS: `/workspace/Observatorio_SUS_ES/.venv-etapa5-cnes/lib/python3.12/site-packages/pysus/__init__.py`
- Status inicial: duas adições locais em arquivos da Etapa 5
- Status final: apenas os três arquivos autorizados da Etapa 5 alterados/criados

## 4. Arquivos criados ou alterados
- `docs/migracao_python/05_extracao_minima_temporaria_cnes_2025.md`
- `python/observatorio_sus/extract/extrair_cnes_temporario_2025.py`
- `tests/python/test_extrair_cnes_temporario_2025_cli.py`

Confirmação: não houve alteração em scripts R, dados versionados, `metadata/`, `docs/cnes/`, workflows, `.gitignore` ou `.gitattributes`.

## 5. Plano de execução autorizado
- UF: `ES`
- Ano: `2025`
- Competências: `202501` a `202512`
- Via principal: PySUS
- Fallback: somente se PySUS falhar/não expuser tabela
- Diretório temporário: obrigatório
- Sem escrita em diretórios versionados

## 6. Gate 1 — Estabelecimentos
- `tbEstabelecimento`: não extraída nesta execução (bloqueio de segurança por ausência de recorte seguro confirmado)
- `tbMunicipio`: não extraída nesta execução (mesmo motivo)
- Download: não houve
- Fallback: não acionado
- `CO_UNIDADE`: inconclusivo (sem extração)
- `CO_CNES`: inconclusivo (sem extração)
- `CO_CNES` textual: inconclusivo
- Zeros à esquerda: inconclusivo
- Vínculo territorial mínimo: inconclusivo
- Campos ausentes na validação sem dados: todos os campos críticos contratados
- Cobertura por competência: não executada por segurança em 202501–202512

**Classificação Gate 1: NÃO_EXECUTADO_POR_SEGURANÇA**

## 7. Gate 2 — Habilitações
Gate 2 não foi tentado por decisão metodológica, pois o Gate 1 não foi aprovado.

**Classificação Gate 2: NÃO_EXECUTADO_POR_GATE_1**

## 8. Arquivos temporários
Nenhum arquivo temporário de dados CNES foi criado/baixado.

A etapa executou diagnóstico e tentativa controlada com `TemporaryDirectory`, sem download.

## 9. Cobertura estrutural por tabela
| Tabela lógica | Necessária para | Competências avaliadas | Campos presentes | Campos ausentes | CO_UNIDADE presente? | CO_CNES presente? | Preservação textual validada? | Cobertura | Fallback necessário? | Observação |
|---|---|---|---|---|---|---|---|---|---|---|
| tbEstabelecimento | estabelecimentos | 202501–202512 | nenhum | todos críticos do contrato | inconclusivo | inconclusivo | inconclusivo | não_confirmada | sim | sem extração por segurança |
| tbMunicipio | estabelecimentos | 202501–202512 | nenhum | todos críticos do contrato | não aplicável | não aplicável | inconclusivo | não_confirmada | sim | sem extração por segurança |
| rlEstabSipac | habilitacoes | 202501–202512 | nenhum | todos críticos do contrato | inconclusivo | não aplicável | inconclusivo | não_confirmada | sim | não testada por Gate 1 |
| tbSubGruposHabilitacao | habilitacoes | 202501–202512 | nenhum | todos críticos do contrato | não aplicável | não aplicável | inconclusivo | não_confirmada | sim | não testada por Gate 1 |
| rlEstabSubTipo | estabelecimentos | 202501–202512 | nenhum | todos críticos do contrato | inconclusivo | não aplicável | inconclusivo | não_confirmada | sim | não testada |
| tbSubTipo | estabelecimentos | 202501–202512 | nenhum | todos críticos do contrato | não aplicável | não aplicável | inconclusivo | não_confirmada | sim | não testada |
| rlEstabAtendPrestConv | estabelecimentos | 202501–202512 | nenhum | todos críticos do contrato | inconclusivo | não aplicável | inconclusivo | não_confirmada | sim | não testada |
| tbAtendimentoPrestado | estabelecimentos | 202501–202512 | nenhum | todos críticos do contrato | não aplicável | não aplicável | inconclusivo | não_confirmada | sim | não testada |
| tbConvenio | estabelecimentos | 202501–202512 | nenhum | todos críticos do contrato | não aplicável | não aplicável | inconclusivo | não_confirmada | sim | não testada |
| tbTipoEstabelecimento | estabelecimentos | 202501–202512 | nenhum | todos críticos do contrato | não aplicável | não aplicável | inconclusivo | não_confirmada | sim | não testada |
| tbNaturezaJuridica | estabelecimentos | 202501–202512 | nenhum | todos críticos do contrato | não aplicável | não aplicável | inconclusivo | não_confirmada | sim | não testada |
| tbGestao | estabelecimentos | 202501–202512 | nenhum | todos críticos do contrato | não aplicável | não aplicável | inconclusivo | não_confirmada | sim | não testada |
| base_estabelecimentos | habilitacoes | 202501–202512 | nenhum | todos críticos do contrato | inconclusivo | inconclusivo | inconclusivo | não_confirmada | sim | derivada futura |

## 10. Cobertura por competência
| Competência | Estabelecimentos avaliados? | Habilitações avaliadas? | Gate 1 | Gate 2 | Arquivos temporários | Observação |
|---|---|---|---|---|---|---|
| 202501 | não | não | não_executado_por_seguranca | não_executado_por_gate_1 | 0 | bloqueio de recorte seguro |
| 202502 | não | não | não_executado_por_seguranca | não_executado_por_gate_1 | 0 | bloqueio de recorte seguro |
| 202503 | não | não | não_executado_por_seguranca | não_executado_por_gate_1 | 0 | bloqueio de recorte seguro |
| 202504 | não | não | não_executado_por_seguranca | não_executado_por_gate_1 | 0 | bloqueio de recorte seguro |
| 202505 | não | não | não_executado_por_seguranca | não_executado_por_gate_1 | 0 | bloqueio de recorte seguro |
| 202506 | não | não | não_executado_por_seguranca | não_executado_por_gate_1 | 0 | bloqueio de recorte seguro |
| 202507 | não | não | não_executado_por_seguranca | não_executado_por_gate_1 | 0 | bloqueio de recorte seguro |
| 202508 | não | não | não_executado_por_seguranca | não_executado_por_gate_1 | 0 | bloqueio de recorte seguro |
| 202509 | não | não | não_executado_por_seguranca | não_executado_por_gate_1 | 0 | bloqueio de recorte seguro |
| 202510 | não | não | não_executado_por_seguranca | não_executado_por_gate_1 | 0 | bloqueio de recorte seguro |
| 202511 | não | não | não_executado_por_seguranca | não_executado_por_gate_1 | 0 | bloqueio de recorte seguro |
| 202512 | não | não | não_executado_por_seguranca | não_executado_por_gate_1 | 0 | bloqueio de recorte seguro |

## 11. Preservação textual e zeros à esquerda
Campos avaliados (contratos):
- CO_UNIDADE
- CO_CNES
- CO_MUNICIPIO_GESTOR
- COD_SUB_GRUPO_HABILITACAO
- TP_HABILITACAO
- CMTP_INICIO
- CMTP_FIM

Resultado:
- evidência de tipo textual: inconclusiva;
- evidência de zeros à esquerda: inconclusiva;
- casos reprovados: nenhum observado (não houve extração);
- casos inconclusivos: todos os campos listados.

## 12. Fallback
- PySUS falhou? Não (importação e versão confirmadas).
- Fallback acionado? Não.
- Fallback tentado? Não.
- Havia recorte seguro? Não confirmado.
- Fallback abortado? Sim (política conservadora: sem recorte seguro).
- Tabelas que exigem fallback futuro: todas as tabelas com cobertura não confirmada.
- Limites encontrados: ausência de confirmação objetiva de recorte seguro por UF+competência nesta implementação.

## 13. Pseudocódigo comparativo com R
**Pseudocódigo conceitual (não implementado, não substitui R):**
1. Extrair temporariamente `tbEstabelecimento` e `tbMunicipio` por competência.
2. Validar `CO_UNIDADE` e `CO_CNES` textuais e integridade de zeros.
3. Comparar esquema temporário com contratos Python.
4. Somente se Gate 1 aprovado, extrair `rlEstabSipac` e `tbSubGruposHabilitacao`.
5. Verificar campos para futura classificação (`codigo_habilitacao + tipo_habilitacao`) sem aplicar classificação.
6. Gerar matriz comparativa contra regras de `preparar_estabelecimentos_cnes.R`, `preparar_habilitacoes_cnes.R` e `classificar_habilitacoes_cnes.R` apenas como checklist de paridade futura.

## 14. Testes Python executados
- Comando: `python -m pytest tests/python`
- Resultado: sucesso
- Número de testes: 21
- Dependência de rede: não para testes; rede usada apenas para instalação de dependências
- Escrita em dados: não
- Falhas/limitações: nenhuma falha de teste; limitação operacional de recorte seguro para extração real

## 15. Perguntas obrigatórias respondidas
| Pergunta | Resposta | Evidência | Implicação |
|---|---|---|---|
| 1. Foi possível acessar/extrair tbEstabelecimento para ES/2025? | Não nesta execução. | Modo `extracao_temporaria` encerrou por segurança. | Requer Etapa 5S para recorte seguro. |
| 2. Foi possível acessar/extrair tbMunicipio para ES/2025? | Não nesta execução. | Mesmo bloqueio de segurança do Gate 1. | Requer Etapa 5S. |
| 3. CO_UNIDADE foi encontrado? | Inconclusivo. | Sem dados extraídos. | Gate 1 não aprovado. |
| 4. CO_CNES foi encontrado? | Inconclusivo. | Sem dados extraídos. | Gate 1 não aprovado. |
| 5. CO_CNES foi preservado como texto? | Inconclusivo. | Sem dados extraídos. | Sem evidência empírica ainda. |
| 6. Há evidência de preservação de zeros à esquerda? | Inconclusivo. | Sem dados extraídos. | Não validar conversão por ora. |
| 7. O vínculo municipal foi verificável? | Inconclusivo. | Sem extração de `tbEstabelecimento`/`tbMunicipio`. | Necessita extração controlada posterior. |
| 8. Habilitações foram tentadas? | Não. | Regra de Gate 2 condicionada ao Gate 1. | Decisão metodológica respeitada. |
| 9. rlEstabSipac foi acessada/extraída? | Não. | Gate 2 não executado. | Sem validação de habilitações. |
| 10. tbSubGruposHabilitacao foi acessada/extraída? | Não. | Gate 2 não executado. | Sem validação de domínio de habilitação. |
| 11. Campos para futura classificação de habilitações existem? | Apenas no contrato, sem comprovação em dados. | `contratos.py` contém campos críticos. | Evidência empírica pendente. |
| 12. Fallback foi necessário? | Potencialmente sim, condicional. | Saída registra necessidade potencial por ausência de recorte seguro. | Planejar fallback controlado na Etapa 5S. |
| 13. Fallback foi testado? | Não. | Política: não acionar sem falha operacional de PySUS + recorte seguro. | Mantém segurança e escopo. |
| 14. Algum dado foi gravado no repositório? | Não. | Não houve escrita em `data_*` nem arquivos adicionais. | Governança de dados preservada. |
| 15. Algum script R pode ser substituído agora? | **Não. Nenhum script R pode ser substituído nesta etapa.** | Deliberação humana e resultado dos gates. | R permanece oráculo. |

## 16. Classificação da Etapa 5
**EXTRACAO_NAO_EXECUTADA_POR_SEGURANCA**

Justificativa:
- não houve extração por ausência de recorte seguro confirmado;
- Gate 1 não executado por segurança;
- Gate 2 não executado por dependência metodológica do Gate 1.

## 17. Implicações para próxima etapa
Recomendação: **Etapa 5S — investigação de recorte seguro e fallback**.

Proibições mantidas:
- não substituir scripts R;
- não escrever em `data_interim`;
- não aplicar classificação de habilitações;
- não alterar metadados.

## 18. Riscos remanescentes
- cobertura estrutural parcial (apenas contrato, sem evidência em dados);
- dependência de rede e de API/fonte CNES;
- risco de download amplo sem recorte seguro;
- fallback ainda não operacionalizado;
- risco de coerção de códigos não testado em dados reais;
- ausência de confirmação de tabelas reais no fluxo da etapa;
- possível divergência entre nomes reais e contratos;
- impossibilidade de comparação empírica com R nesta execução;
- manutenção de R como oráculo necessária.

## 19. Critérios de aceite
- [x] Documento da Etapa 5 criado.
- [x] Script de extração temporária criado.
- [x] Testes Python criados.
- [x] Testes Python executados.
- [x] Python 3.12 usado.
- [x] PySUS 2.x usado.
- [x] Competências 202501–202512 consideradas.
- [x] Gate 1 executado ou bloqueio registrado.
- [x] Gate 2 executado apenas se Gate 1 aprovado.
- [x] Arquivos temporários registrados.
- [x] Arquivos temporários excluídos.
- [x] Nenhum dado gravado no repositório.
- [x] Nenhum script R alterado.
- [x] Nenhum teste R alterado.
- [x] Nenhum metadado alterado.
- [x] Nenhum docs/cnes alterado.
- [x] Nenhum workflow alterado.
- [x] Nenhuma base data_raw/data_interim/data_processed alterada.
- [x] Classificação final registrada.
- [x] Próxima etapa recomendada.

## 20. Conclusão
A Etapa 5 foi executada com sucesso operacional **sem erro inesperado**, porém com bloqueio de segurança para extração remota (sem recorte seguro confirmado). Portanto:
- não houve extração real de dados CNES;
- Gate 1: `NÃO_EXECUTADO_POR_SEGURANÇA`;
- Gate 2: `NÃO_EXECUTADO_POR_GATE_1`;
- classificação final: `EXTRACAO_NAO_EXECUTADA_POR_SEGURANCA`;
- fallback permanece tema para investigação controlada (Etapa 5S);
- não é possível avançar diretamente para Etapa 6 sem tratar recorte seguro/fallback;
- não houve migração, substituição de R, nem escrita em dados versionados.
