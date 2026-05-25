# Revisão pós-Etapa 4 — Contratos CNES e validação operacional controlada

## 1. Objetivo da revisão
Esta revisão audita criticamente a Etapa 4 antes de qualquer avanço para a Etapa 5.

Esta revisão:
- não implementa nova funcionalidade;
- não executa migração;
- não altera dados;
- não altera metadados;
- não altera scripts R;
- não altera `docs/cnes`;
- apenas avalia consistência de contratos, script, testes, documentação e decisão de avanço.

## 2. Insumos verificados

### Documentos de migração
- `docs/migracao_python/00_baseline_r_pre_migracao.md`
- `docs/migracao_python/01_classificacao_legado_r.md`
- `docs/migracao_python/02_governanca_arquitetura_hibrida.md`
- `docs/migracao_python/03_poc_pysus_cnes.md`
- `docs/migracao_python/04_contratos_extracao_cnes_python.md`

### Código Python
- `python/observatorio_sus/cnes/__init__.py`
- `python/observatorio_sus/cnes/contratos.py`
- `python/observatorio_sus/extract/validar_extracao_cnes_controlada.py`
- `python/observatorio_sus/extract/avaliar_pysus_cnes.py`
- `python/observatorio_sus/io/manifestos.py`
- `python/observatorio_sus/utils/normalizacao.py`

### Testes Python
- `tests/python/test_contratos_cnes.py`
- `tests/python/test_validar_extracao_cnes_controlada_cli.py`
- `tests/python/test_estrutura_python_minima.py`
- `tests/python/test_avaliar_pysus_cnes_cli.py` (não existe no snapshot analisado)

### Dependências
- `requirements-python-poc.txt`

### Documentação geral
- `README.md`
- `docs/convensoes_metodologicas.md`
- `docs/governanca_codigo.md`

### Documentação CNES
- `docs/cnes/decisoes_metodologicas_cnes.md`
- `docs/cnes/base_estabelecimentos_cnes.md`
- `docs/cnes/base_habilitacoes_cnes.md`
- `docs/cnes/classificacao_habilitacoes_cnes.md`
- `docs/cnes/README.md`

### Metadados CNES
- `metadata/cnes/schema_estabelecimentos_cnes.csv`
- `metadata/cnes/schema_habilitacoes_cnes.csv`
- `metadata/cnes/dicionario_estabelecimentos_cnes.csv`
- `metadata/cnes/dicionario_habilitacoes_cnes.csv`
- `metadata/cnes/classificacao_habilitacoes_cnes.csv`

## 3. Ambiente de revisão
- Branch: `work`
- HEAD: `2689ff852265dd43011d1375124e729c5c7e579f`
- Último commit: `2689ff8 feat(migracao): contratos CNES e validação operacional controlada (Etapa 4)`
- Status inicial: limpo.
- Python usado: `3.12.3`
- Caminho Python: `/workspace/Observatorio_SUS_ES/.venv-review-etapa4-cnes/bin/python`
- Pip: `26.1.1`
- PySUS: `2.0.4`
- Caminho PySUS: `/workspace/Observatorio_SUS_ES/.venv-review-etapa4-cnes/lib/python3.12/site-packages/pysus/__init__.py`
- Status final: apenas criação deste documento de revisão.

## 4. Verificação dos contratos Python CNES

| Item verificado | Resultado | Evidência | Necessita revisão por IA? | Necessita revisão humana? | Observação |
|---|---|---|---|---|---|
| Tabelas obrigatórias de estabelecimentos | OK | `TABELAS_OBRIGATORIAS["estabelecimentos"]` contém 10 tabelas esperadas | Sim | Sim | Revisão humana para suficiência substantiva |
| Tabelas obrigatórias de habilitações | OK | `TABELAS_OBRIGATORIAS["habilitacoes"]` contém `rlEstabSipac`, `tbSubGruposHabilitacao`, `base_estabelecimentos` | Sim | Sim | Dependência derivada explicitada |
| Contempla `tbEstabelecimento` | OK | Entrada dedicada em `CONTRATOS_TABELAS` | Sim | Não |  |
| Contempla `tbMunicipio` | OK | Entrada dedicada em `CONTRATOS_TABELAS` | Sim | Não |  |
| Contempla `rlEstabSipac` | OK | Entrada dedicada em `CONTRATOS_TABELAS` | Sim | Não |  |
| Contempla `tbSubGruposHabilitacao` | OK | Entrada dedicada em `CONTRATOS_TABELAS` | Sim | Não |  |
| Contempla tabelas `rl*` necessárias | PARCIAL | Inclui `rlEstabSubTipo`, `rlEstabAtendPrestConv`, `rlEstabSipac`; suficiência depende de validação humana | Sim | Sim | Pode haver outras RL em fallback futuro |
| Lista campos críticos por tabela | OK | atributo `campos_criticos` por tabela | Sim | Sim | Revisão humana para semântica final |
| Lista campos textuais a preservar | OK | `CAMPOS_TEXTUAIS_OBRIGATORIOS` | Sim | Sim | Ampliável na Etapa 5 |
| `validar_presenca_campos` case-insensitive | OK | normalização em lowercase e comparação | Sim | Não | Testado em `test_contratos_cnes.py` |
| Independência de PySUS | OK | não há import de `pysus` em `contratos.py` | Sim | Não |  |
| Não lê dados reais | OK | ausência de IO de dados | Sim | Não |  |
| Não altera arquivos | OK | módulo declarativo/funções puras | Sim | Não |  |

## 5. Aderência dos contratos Python aos documentos e metadados CNES

| Regra metodológica | Fonte documental/metadado | Representação em contratos.py | Situação | Revisão por IA | Revisão humana | Observação |
|---|---|---|---|---|---|---|
| `co_unidade` é chave operacional | docs/cnes/decisoes_metodologicas_cnes.md + schemas/dicionários | `CO_UNIDADE` em campos críticos de `tbEstabelecimento` e `rlEstabSipac`; `base_estabelecimentos.co_unidade` | Aderente | Sim | Sim | Humano valida suficiência em todas tabelas de join |
| `cnes`/`CO_CNES` é código público | decisões + schema_estabelecimentos | `CO_CNES` em `tbEstabelecimento`; `cnes` em base derivada | Aderente | Sim | Sim |  |
| Joins relacionais por `co_unidade` | decisões + base_estabelecimentos | RLs contratadas com `CO_UNIDADE` | Aderente (parcial operacional) | Sim | Sim | Implementação real ainda não testada |
| Habilitações integradas por `co_unidade` | base_habilitacoes + schema_habilitacoes | `rlEstabSipac.CO_UNIDADE` + `base_estabelecimentos.co_unidade` | Aderente | Sim | Sim |  |
| Chave composta `codigo_habilitacao + tipo_habilitacao` | decisões + classificação + schema_habilitacoes | `COD_SUB_GRUPO_HABILITACAO` + `TP_HABILITACAO` em `rlEstabSipac` | Aderente | Sim | Sim | Nome lógico da chave composto está implícito |
| Preservação textual de códigos | schemas/dicionários | lista de campos textuais obrigatórios | Aderente parcial | Sim | Sim | Pode exigir ampliação futura |
| `data_interim` é produto gerável | decisões/base docs | não há dependência de `data_interim` nos contratos | Aderente | Sim | Não |  |
| Não usar CSV histórico sem `co_unidade` como contrato | baseline + decisões | contratos não referenciam CSV histórico | Aderente | Sim | Não |  |
| `atende_sus` classificação conservadora | decisões + dicionários | não modelado como regra analítica em contratos | Neutro/compatível | Sim | Sim | Correto não implementar classificação nesta etapa |

## 6. Verificação do script validar_extracao_cnes_controlada.py

| Item | Resultado | Evidência | Risco | Revisão por IA | Revisão humana | Observação |
|---|---|---|---|---|---|---|
| Usa argparse | OK | `argparse.ArgumentParser` | Baixo | Sim | Não |  |
| Modos `diagnostico/contratos/tentativa_controlada` | OK | `choices=[...]` | Baixo | Sim | Não |  |
| Modo padrão seguro | OK | default `diagnostico` | Baixo | Sim | Não |  |
| Registra ambiente | OK | bloco `ambiente` no JSON | Baixo | Sim | Não |  |
| Registra PySUS | OK | bloco `pysus` | Baixo | Sim | Não |  |
| Usa tempfile | OK | `tempfile.gettempdir()` | Baixo | Sim | Não |  |
| Não grava dados no repositório | OK | ausência de escrita de arquivo | Baixo | Sim | Não |  |
| Ignora `.tests` do PySUS | OK | filtro `if ".tests" in mod.name: continue` | Baixo | Sim | Não |  |
| Não usa `pysus.tests` como evidência | OK | diagnóstico restrito a módulos relevantes sem `.tests` | Baixo | Sim | Não |  |
| Gera JSON textual | OK | `json.dumps(..., ensure_ascii=False, indent=2)` | Baixo | Sim | Não |  |
| Retorna 0 em diagnóstico controlado | OK | execução CLI com código 0 | Baixo | Sim | Não |  |
| Retorna 2 em erro inesperado | OK (por inspeção) | `except Exception: return 2` | Médio | Sim | Não | Falta teste negativo dedicado |
| Não executa download massivo em diagnóstico | OK | fluxo diagnóstico não chama download | Médio | Sim | Sim | Humano valida risco residual do ecossistema |
| Aborta tentativa controlada sem recorte seguro | PARCIAL | modo marca fallback/requer_fallback, mas não há tentativa remota real implementada | Médio | Sim | Sim | Não bloqueante para revisão; exigir regra explícita na Etapa 5 |
| Informa fallback necessário | OK | campo `fallback_necessario` | Baixo | Sim | Não |  |

## 7. Verificação dos testes Python
- Comando executado: `python -m pytest tests/python`
- Resultado geral: aprovado.
- Número de testes: 17.
- Falhas: nenhuma.
- Dependência de rede: não para execução dos testes; rede usada apenas na instalação de dependências.
- Escrita de dados reais: não observada.
- Cobertura de contratos: sim (`test_contratos_cnes.py`).
- Cobertura de CLI: sim (`test_validar_extracao_cnes_controlada_cli.py` e `test_estrutura_python_minima.py`).
- Cobertura normalização/manifestos: sim (`test_estrutura_python_minima.py`).
- Lacunas: ausência de teste para caminho de erro (exit 2), ausência de teste dirigido a `tentativa_controlada`.

| Teste/arquivo | Cobertura | Resultado | Lacuna | Revisão por IA | Revisão humana | Observação |
|---|---|---|---|---|---|---|
| `test_contratos_cnes.py` | contratos e case-insensitive | Passou | não valida completude metodológica de todos campos | Sim | Sim | Humano valida mérito dos contratos |
| `test_validar_extracao_cnes_controlada_cli.py` | CLI help + modo contratos | Passou | não cobre erro 2 / tentativa_controlada | Sim | Não |  |
| `test_estrutura_python_minima.py` | importações, normalização, manifesto, CLI antiga | Passou | não cobre novo parser JSON | Sim | Não |  |
| `test_avaliar_pysus_cnes_cli.py` | N/A (ausente) | N/A | não existe | Sim | Não | lacuna não bloqueante |

## 8. Verificação dos modos CLI

| Modo | Resultado | Rede/download | Escrita em disco | Evidência | Revisão por IA | Revisão humana | Observação |
|---|---|---|---|---|---|---|---|
| `--help` | exit 0, ajuda exibida | sem download | sem escrita | saída de uso do argparse | Sim | Não | OK |
| `--modo contratos` | exit 0, JSON legível | sem download | sem escrita | JSON com `diagnostico_pysus.nao_executado=true` | Sim | Não | OK para execução offline |
| `--modo diagnostico` | exit 0, JSON legível | sem download massivo observado | sem escrita | JSON com módulos/objetos PySUS e fallback | Sim | Sim | validação humana da interpretação de cobertura |

## 9. Verificação do relatório da Etapa 4

| Seção esperada | Presente? | Adequada? | Revisão por IA | Revisão humana | Observação |
|---|---|---|---|---|---|
| Objetivo | Sim | Sim | Sim | Não |  |
| Contexto herdado | Sim | Sim | Sim | Não |  |
| Ambiente usado | Sim | Sim | Sim | Não |  |
| Arquivos criados/alterados | Sim | Sim | Sim | Não |  |
| Contratos definidos | Sim | Sim | Sim | Sim | mérito metodológico humano |
| Relação com metadados/documentação | Sim | Sim | Sim | Sim |  |
| Validação operacional controlada | Sim | Sim | Sim | Sim |  |
| Cobertura tabelas/campos | Sim | Sim | Sim | Sim |  |
| Fallback planejado | Sim | Sim | Sim | Sim | decisão institucional humana |
| Testes executados | Sim | Sim | Sim | Não |  |
| Perguntas obrigatórias | Sim | Sim | Sim | Sim | pergunta 13 correta |
| Classificação Etapa 4 | Sim | Sim | Sim | Sim |  |
| Implicações Etapa 5 | Sim | Sim | Sim | Sim |  |
| Riscos remanescentes | Sim | Sim | Sim | Sim |  |
| Critérios de aceite | Sim | Sim | Sim | Não |  |
| Conclusão | Sim | Sim | Sim | Não |  |

## 10. Validação da classificação da Etapa 4
Classificação avaliada: **CONTRATOS_DEFINIDOS_E_VALIDACAO_OPERACIONAL_PARCIAL**.

Avaliação dos critérios:
- contratos estão definidos: sim;
- testes Python passaram: sim;
- validação operacional foi executada: sim;
- cobertura PySUS ainda parcial: sim;
- fallback permanece necessário: sim;
- ainda não houve extração real validada: sim;
- ainda não há autorização para substituir R: sim.

**Conclusão:** classificação deve ser **mantida**, com ressalva explícita de revisão humana prévia antes da Etapa 5.

## 11. Matriz de revisão por IA versus revisão humana

| Item ou decisão | Tipo de revisão necessária | Pode ser revisado por IA? | Exige revisão humana? | Perfil humano recomendado | Justificativa | Prioridade | Bloqueia Etapa 5? |
|---|---|---|---|---|---|---|---|
| Consistência de nomes de campos contratos vs schemas | IA | Sim | Não | N/A | checagem sintática/estrutural | Alta | Não |
| Presença de campos críticos | IA | Sim | Não | N/A | verificação automatizável | Alta | Não |
| Ausência de alterações fora do escopo | IA | Sim | Não | N/A | `git status` e diff | Alta | Sim |
| Validade JSON do script | IA | Sim | Não | N/A | parseável por automação | Alta | Não |
| Coerência relatório vs comandos executados | IA | Sim | Não | N/A | auditoria textual/comandos | Média | Não |
| Execução de testes Python | IA | Sim | Não | N/A | automatizável | Alta | Sim |
| Aderência textual à governança híbrida | IA | Sim | Não | N/A | comparação documental | Média | Não |
| Detecção de imports inadequados | IA | Sim | Não | N/A | lint estático | Baixa | Não |
| Detecção de escrita indevida em data_* | IA | Sim | Não | N/A | varredura estática/dinâmica | Alta | Sim |
| Consistência do requirements | IA | Sim | Não | N/A | comparação literal | Alta | Sim |
| Conferência de ignorar `.tests` do PySUS | IA | Sim | Não | N/A | inspeção de código/log | Média | Não |
| Suficiência substantiva das tabelas CNES contratadas | Humana | Parcial | Sim | especialista CNES/DATASUS + curador metadados | mérito metodológico | Alta | Sim |
| Suficiência para representar estabelecimentos/habilitações | Humana | Parcial | Sim | pesquisador responsável + especialista CNES | decisão analítica | Alta | Sim |
| Adequação metodológica de `atende_sus` | Humana | Não | Sim | saúde coletiva/atenção especializada | interpretação sanitária | Média | Não |
| Interpretação da limitação de `gestao` | Humana | Parcial | Sim | especialista CNES + curador metadados | risco de inferência indevida | Média | Não |
| Preservação da classificação como patrimônio metodológico | Humana | Parcial | Sim | pesquisador responsável | governança científica | Alta | Sim |
| Aceitabilidade institucional de fallback FTP/DATASUS | Humana | Não | Sim | responsável técnico infra + pesquisador | risco operacional e compliance | Alta | Sim |
| Decisão de avanço para extração mínima real | Humana | Parcial | Sim | pesquisador responsável | gate de etapa | Alta | Sim |
| Priorização Etapa 5 (estab/hab/ambas) | Humana | Parcial | Sim | pesquisador + especialista CNES | estratégia de execução | Alta | Sim |
| Comparação contratos Python vs metadata/cnes | Mista IA+Humano | Sim | Sim | curador metadados | IA prepara evidência, humano valida mérito | Alta | Sim |
| Matriz de cobertura por tabela | Mista IA+Humano | Sim | Sim | especialista CNES | IA resume; humano interpreta suficiência | Alta | Sim |
| Definição final de campos textuais | Mista IA+Humano | Sim | Sim | curador metadados | risco de coerção numérica | Alta | Sim |
| Desenho preliminar de fallback | Mista IA+Humano | Sim | Sim | infra + CNES | decisão técnica/institucional conjunta | Alta | Sim |
| Interpretação da cobertura PySUS | Mista IA+Humano | Sim | Sim | especialista CNES/DATASUS | IA aponta sinais; humano valida | Alta | Sim |
| Critérios de aceite da Etapa 5 | Mista IA+Humano | Sim | Sim | pesquisador responsável | governança de avanço | Alta | Sim |
| Planejamento de manifestos/rastreabilidade | Mista IA+Humano | Sim | Sim | curador metadados + infra | técnica + conformidade | Média | Não |

### 11.1 Itens adequados para revisão por IA
Conforme matriz: consistência de campos, presença de campos críticos, escopo de alteração, JSON, coerência documental/comandos, testes Python, governança textual, imports, escrita indevida em dados, requirements e ignorar `.tests`.

### 11.2 Itens que exigem revisão humana
Conforme matriz: suficiência substantiva das tabelas, suficiência para representar bases, regras `atende_sus`, limitação de `gestao`, patrimônio metodológico de classificação, aceitabilidade institucional do fallback, risco de controle de download/dados, decisão de avanço e priorização de escopo da Etapa 5.

### 11.3 Itens mistos IA + humano
Conforme matriz: comparação contratos vs metadata, cobertura por tabela, campos textuais, fallback preliminar, interpretação de cobertura PySUS, critérios de aceite da Etapa 5, risco de coerção numérica e planejamento de manifestos.

## 12. Pendências classificadas

### 12.1 Pendências bloqueantes antes da Etapa 5
- Deliberação humana formal sobre suficiência metodológica da lista de tabelas/campos contratados.
- Deliberação humana sobre escopo inicial da Etapa 5 (estabelecimentos, habilitações ou ambas).
- Definição institucional de política de fallback e limites de rede/download em tentativa controlada.

### 12.2 Pendências relevantes, mas não bloqueantes
- Manifesto Python ainda minimalista para rastreabilidade avançada.
- Cobertura PySUS permanece parcial e baseada em diagnóstico, não em extração real.
- README global ainda majoritariamente centrado no piloto R (compatível com fase atual, mas incompleto para trilha Python).
- Documentação de fallback ainda preliminar.
- Testes ainda não incluem cenário de extração real temporária.

### 12.3 Melhorias futuras
- Ampliar manifesto (hash, origem, parâmetros operacionais detalhados).
- Adicionar validação formal de schema JSON de saída.
- Criar schema programático de contratos com tipagem mais forte.
- Criar fixture sintética CNES Python para validações de cobertura de campos.
- Preparar trilha de CI Python futura para etapas de migração.
- Documentar fallback com matriz de decisão mais detalhada.

## 13. Revisão humana recomendada antes da Etapa 5
1. Conferir se a lista de tabelas CNES contratadas é metodologicamente suficiente.
2. Conferir se os campos críticos por tabela estão corretos.
3. Conferir se a Etapa 5 deve iniciar por estabelecimentos, por habilitações ou por ambos.
4. Conferir se o fallback planejado é aceitável.
5. Conferir se a classificação `CONTRATOS_DEFINIDOS_E_VALIDACAO_OPERACIONAL_PARCIAL` é adequada.
6. Conferir risco ético, institucional e operacional da extração real temporária.
7. Conferir se a Etapa 5 deve permitir `tentativa_controlada` com rede.
8. Conferir se a preservação textual de códigos está suficientemente protegida.

Perfis humanos recomendados:
- pesquisador responsável;
- especialista em CNES/DATASUS;
- curador de metadados;
- responsável técnico por infraestrutura;
- especialista em saúde coletiva/atenção especializada (quando envolver mérito substantivo de linhas de cuidado).

## 14. Revisão por IA recomendada antes da Etapa 5
1. Gerar checklist técnico da Etapa 5.
2. Gerar matriz de comparação entre `contratos.py` e `metadata/cnes`.
3. Gerar plano de testes Python para extração temporária.
4. Gerar esqueleto de manifesto de execução.
5. Gerar validações de tipos textuais.
6. Gerar parser de saída JSON para relatórios.
7. Gerar validação automática de não escrita em `data_interim`.
8. Gerar relatório de cobertura PySUS/fallback.
9. Gerar prompts de execução controlada para Codex.
10. Preparar documentação operacional sem decisão metodológica substantiva.

## 15. Decisão sobre avanço para Etapa 5
**Decisão:** **2. Aprovada para Etapa 5 com revisão humana prévia.**

Justificativa:
- contratos: definidos e aderentes em nível estrutural;
- testes: aprovados (17/17);
- cobertura PySUS/fallback: parcial, com fallback necessário;
- pendências humanas: ainda existem e são críticas para governança;
- risco de escopo: controlável se Etapa 5 for estritamente temporária e sem escrita em dados versionados.

Escopo recomendado para a Etapa 5: **extração mínima temporária de ambas (estabelecimentos e habilitações), por recorte pequeno e controlado, com possibilidade de recuar para apenas estabelecimentos se risco operacional aumentar.**

## 16. Recomendação de escopo para a Etapa 5
Escopo controlado proposto (sem implementação nesta revisão):
- uso obrigatório de diretório temporário;
- nenhuma escrita em `data_raw`/`data_interim`/`data_processed`;
- nenhuma substituição de R;
- nenhuma alteração de `metadata`;
- comparação estrutural dos resultados com `contratos.py`;
- registro de manifesto temporário de execução;
- relatório de colunas encontradas/ausentes por tabela;
- classificação de cobertura por tabela e por campo;
- decisão posterior sobre fallback apenas após evidência da extração mínima real.

## 17. Critérios de aceite da revisão
- [x] Todos os arquivos obrigatórios foram verificados.
- [x] Contratos Python foram comparados com docs/cnes e metadata/cnes.
- [x] Script de validação operacional foi auditado.
- [x] Testes Python foram executados ou limitação registrada.
- [x] Modos CLI foram verificados.
- [x] Relatório da Etapa 4 foi avaliado.
- [x] Classificação da Etapa 4 foi validada ou qualificada.
- [x] Matriz IA versus humano foi criada.
- [x] Pendências bloqueantes foram identificadas.
- [x] Pendências não bloqueantes foram identificadas.
- [x] Revisão humana recomendada foi explicitada.
- [x] Revisão por IA recomendada foi explicitada.
- [x] Decisão sobre Etapa 5 foi registrada.
- [x] Nenhum script R foi alterado.
- [x] Nenhum dado foi alterado.
- [x] Nenhum metadado foi alterado.
- [x] Nenhum docs/cnes foi alterado.
- [x] Nenhum workflow foi alterado.

## 18. Conclusão
Status da revisão: **concluída com aprovação condicionada para avanço**.

Avaliação da Etapa 4: consistente com escopo de contratos e diagnóstico controlado.

Classificação da Etapa 4: **mantida** como `CONTRATOS_DEFINIDOS_E_VALIDACAO_OPERACIONAL_PARCIAL`.

Necessidade de revisão humana: permanece mandatória para mérito metodológico e decisão institucional de fallback/rede.

Revisão por IA: adequada para auditoria técnica, consistência estrutural, checklist e preparação de evidências.

Decisão sobre Etapa 5: **aprovar com revisão humana prévia**, mantendo escopo estrito, sem migração plena e sem substituição de R.

Ressalva final: nenhuma migração de pipeline foi realizada nesta revisão.
