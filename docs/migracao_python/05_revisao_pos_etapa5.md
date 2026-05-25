# Revisão pós-Etapa 5 — extração temporária CNES/ES/2025 e bloqueio por segurança

## 1. Objetivo da revisão
Esta revisão avalia criticamente a Etapa 5 antes de qualquer avanço de etapa.

Escopo desta revisão:
- não implementa funcionalidade;
- não executa migração;
- não realiza download real;
- não altera dados;
- não altera metadados;
- não altera scripts R;
- apenas audita resultado, segurança, documentação e próxima decisão.

## 2. Insumos verificados
### 2.1 Documentos de migração
- `docs/migracao_python/00_baseline_r_pre_migracao.md`
- `docs/migracao_python/01_classificacao_legado_r.md`
- `docs/migracao_python/02_governanca_arquitetura_hibrida.md`
- `docs/migracao_python/03_poc_pysus_cnes.md`
- `docs/migracao_python/04_contratos_extracao_cnes_python.md`
- `docs/migracao_python/04_revisao_pos_etapa4.md`
- `docs/migracao_python/04_deliberacao_humana_pre_etapa5.md`
- `docs/migracao_python/05_extracao_minima_temporaria_cnes_2025.md`

### 2.2 Código Python
- `python/observatorio_sus/extract/extrair_cnes_temporario_2025.py`
- `python/observatorio_sus/extract/validar_extracao_cnes_controlada.py`
- `python/observatorio_sus/cnes/contratos.py`
- `python/observatorio_sus/io/manifestos.py`
- `python/observatorio_sus/utils/normalizacao.py`

### 2.3 Testes Python
- `tests/python/test_extrair_cnes_temporario_2025_cli.py`
- `tests/python/test_contratos_cnes.py`
- `tests/python/test_validar_extracao_cnes_controlada_cli.py`
- `tests/python/test_estrutura_python_minima.py`

### 2.4 Dependências
- `requirements-python-poc.txt`

### 2.5 Documentação geral
- `README.md`
- `docs/convensoes_metodologicas.md`
- `docs/governanca_codigo.md`

## 3. Ambiente de revisão
- Branch: `work`
- HEAD: `bfec0a84a3e60f0eb5913d62e367e9553965286f`
- Último commit: `bfec0a8 Add Etapa 5 temporary CNES extraction (ES/2025) with safety gating, docs and tests`
- Status inicial: limpo
- Python usado: `3.12.3`
- Caminho Python: `/workspace/Observatorio_SUS_ES/.venv-review-etapa5-cnes/bin/python`
- Pip: `26.1.1`
- PySUS: `2.0.4`
- Caminho PySUS: `/workspace/Observatorio_SUS_ES/.venv-review-etapa5-cnes/lib/python3.12/site-packages/pysus/__init__.py`
- Status final: apenas criação deste relatório

## 4. Verificação da correção do bloqueio hardcoded
| Item | Resultado | Evidência | Observação |
|---|---|---|---|
| removeu `safe_recorte_confirmado=False` fixo | Sim | `safe_recorte_confirmado = bool(diag.get("recorte_seguro_confirmado", False))` | bloqueio deixou de ser valor fixo |
| usa checagem dinâmica | Sim | função `_diagnostico_pysus()` inspeciona módulos e assinaturas | decisão depende do diagnóstico |
| registra evidências da inspeção | Sim | campos `modulos_cnes`, `candidatos_com_recorte` | auditabilidade aumentada |
| registra `motivo_recorte` | Sim | campo `motivo_recorte` no diagnóstico | valor observado: `nenhuma_assinatura_com_uf_e_competencia_identificada` |
| bloqueia somente sem recorte seguro | Sim | condição `if not safe_recorte_confirmado:` no modo `extracao_temporaria` | comportamento alinhado ao objetivo de segurança |

## 5. Verificação da checagem dinâmica de recorte seguro
| Critério | Resultado | Evidência | Fragilidade | Observação |
|---|---|---|---|---|
| inspeciona módulos PySUS relevantes | Sim | varredura `pkgutil.walk_packages` com filtro `"cnes" in nome` | Média | pode perder módulos com nomenclatura distinta |
| ignora `.tests` | Não | não há filtro explícito de `.tests` nesta implementação | Média | risco baixo prático, mas critério não está explícito |
| examina assinaturas de funções/classes | Sim | uso de `inspect.signature(obj)` | Baixa | adequado para diagnóstico estático |
| procura parâmetros de UF/state | Sim | critérios `uf` ou `state` | Baixa | alinhado ao recorte territorial |
| procura parâmetros competência/competence/year | Sim | critérios `competencia`, `competence` ou `year` | Média | pode não cobrir outros nomes de parâmetro |
| exige simultaneamente UF e competência | Sim | só adiciona candidato quando `aceita_uf and aceita_comp` | Baixa | evita falso positivo simples |
| registra resultado no JSON | Sim | `recorte_seguro_confirmado`, `motivo_recorte`, `candidatos_com_recorte`, `checagem_recorte_seguro` | Baixa | boa rastreabilidade |
| evita download sem assinatura | Sim | fluxo bloqueia e retorna `NAO_EXECUTADO_POR_SEGURANCA` | Baixa | não houve download nesta revisão |

## 6. Verificação dos modos CLI
| Modo | Exit code | Executou download? | Escreveu arquivo versionado? | Retornou JSON? | Classificação/resultado |
|---|---:|---|---|---|---|
| `--help` | 0 | não | não | N/A (ajuda) | correto |
| `planejamento` | 0 | não | não | sim | Gate 1 `PLANEJADO`, Gate 2 `CONDICIONADO` |
| `diagnostico` | 0 | não | não | sim | `NAO_EXECUTADO_POR_SEGURANCA` sem download |
| `extracao_temporaria` | 0 | não | não | sim | `recorte_seguro_confirmado=false`, `motivo_recorte=nenhuma_assinatura_com_uf_e_competencia_identificada`, Gate 1 bloqueado por segurança |

## 7. Verificação dos testes Python
- Comando executado: `python -m pytest tests/python`
- Resultado: sucesso
- Número de testes: 21
- Falhas: 0
- Dependência de rede: não para execução dos testes (rede apenas na instalação de dependências)
- Cobertura de modo planejamento: sim
- Cobertura de competências 202501–202512: sim
- Cobertura de ausência de escrita em `data_raw`/`data_interim`/`data_processed`: sim
- Cobertura de checagem dinâmica de recorte seguro: não há teste específico dedicado

Classificação da cobertura dos testes: **parcial**.

## 8. Verificação do relatório da Etapa 5
Avaliação de `docs/migracao_python/05_extracao_minima_temporaria_cnes_2025.md`:
- registra a correção da checagem dinâmica: **sim**;
- explica por que a extração não foi executada: **sim**;
- registra `recorte_seguro_confirmado=false`: **indireto/incompleto** (descrição textual presente, campo literal não tabelado no relatório);
- registra `motivo_recorte`: **indireto/incompleto** (motivo textual descrito, mas sem reprodução explícita do valor técnico no corpo principal);
- registra que não houve download: **sim**;
- registra que não houve escrita em dados: **sim**;
- mantém classificação `EXTRACAO_NAO_EXECUTADA_POR_SEGURANCA`: **sim**;
- não afirma indevidamente extração real: **sim**.

Conclusão desta verificação: relatório está **majoritariamente aderente**, com oportunidade de explicitar melhor os campos literais do JSON (`recorte_seguro_confirmado` e `motivo_recorte`).

## 9. Validação da classificação da Etapa 5
Classificação avaliada: `EXTRACAO_NAO_EXECUTADA_POR_SEGURANCA`.

Decisão: **manter**.

Justificativa:
- não houve download real;
- o bloqueio ocorreu por ausência de recorte seguro confirmado na checagem dinâmica;
- não houve falha crítica de dados oriunda de extração real;
- portanto não cabe `REPROVADA`;
- a checagem tem fragilidades, mas não invalida a conclusão de segurança operacional, logo não exige reclassificar para `INCONCLUSIVA` nesta revisão.

## 10. Implicações metodológicas
- Gate 1 não foi executado empiricamente;
- Gate 2 não foi tentado por dependência do Gate 1;
- não houve validação real de `CO_UNIDADE`;
- não houve validação real de `CO_CNES`;
- não houve comparação empírica de colunas com dados temporários;
- não há base para substituir R;
- não há base para avançar para extração regenerável ainda.

## 11. Decisão sobre próxima etapa
Recomendação: **Etapa 5S — Investigação de recorte seguro e fallback CNES/DATASUS/FTP**.

Motivo: a etapa atual confirmou bloqueio por segurança com justificativa dinâmica, mas sem extração empírica mínima.

## 12. Revisão humana necessária
**Sim, necessária antes da próxima etapa.**

Pontos que exigem decisão humana:
- autorização para investigar fallback direto DATASUS/FTP;
- limites aceitáveis de download temporário;
- escopo de teste com arquivos CNES específicos por competência;
- aceitação de arquivos temporários maiores;
- decisão sobre PySUS como via principal versus camada auxiliar.

## 13. Pendências
### 13.1 Bloqueantes antes de Etapa 6
- ausência de extração real temporária;
- ausência de validação empírica de `CO_UNIDADE`;
- ausência de validação empírica de `CO_CNES`;
- ausência de comparação real de colunas;
- ausência de política operacional de fallback testada.

### 13.2 Relevantes, mas não bloqueantes para Etapa 5S
- testes ainda não cobrem caminho completo de fallback;
- relatório não contém comparação empírica;
- PySUS permanece parcialmente útil;
- manifestação de fallback ainda preliminar.

### 13.3 Melhorias futuras
- teste unitário para checagem dinâmica de recorte;
- parser estruturado de assinaturas PySUS;
- matriz de fontes DATASUS/FTP por tabela;
- fixture sintética de retorno PySUS;
- manifesto expandido.

## 14. Critérios de aceite da revisão
- [x] Script da Etapa 5 revisado.
- [x] Correção do bloqueio hardcoded verificada.
- [x] Checagem dinâmica de recorte seguro avaliada.
- [x] Modos CLI executados.
- [x] Testes Python executados.
- [x] Relatório da Etapa 5 avaliado.
- [x] Classificação final validada ou ajustada.
- [x] Próxima etapa recomendada.
- [x] Nenhum script R alterado.
- [x] Nenhum dado alterado.
- [x] Nenhum metadado alterado.
- [x] Nenhum docs/cnes alterado.
- [x] Nenhum workflow alterado.

## 15. Conclusão
A Etapa 5 é considerada **aprovada com ressalvas operacionais** para fins de governança da migração: a classificação `EXTRACAO_NAO_EXECUTADA_POR_SEGURANCA` foi mantida, a correção removeu o bloqueio hardcoded e passou a justificar o bloqueio com diagnóstico dinâmico. Ainda assim, não houve extração empírica mínima e, portanto, a próxima etapa adequada é **Etapa 5S** com revisão humana prévia. Reafirma-se que nenhuma migração foi realizada nesta revisão.
