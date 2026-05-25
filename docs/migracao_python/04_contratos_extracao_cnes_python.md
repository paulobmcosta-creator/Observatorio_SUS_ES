# Contratos de dados e validação operacional controlada da extração CNES em Python/PySUS

## 1. Objetivo da Etapa 4
Esta etapa transforma os achados da POC PySUS/CNES em contratos explícitos e validação operacional controlada, sem migração plena. Não substitui scripts R, não altera `data_raw`/`data_interim`/`data_processed`, não altera `metadata`, não altera workflows, não gera produto final, não aplica classificação de habilitações e mantém R como oráculo metodológico.

## 2. Contexto herdado das etapas anteriores
- Etapa 0: baseline do legado R e risco de Git LFS, incluindo histórico de `data_interim` sem `co_unidade` como contrato estrutural inválido.
- Etapa 1: classificação formal do legado R por criticidade metodológica.
- Etapa 2: governança da arquitetura híbrida R–Python/PySUS.
- Etapa 3: POC inicial insuficiente (Python 3.14 + PySUS 0.11).
- Etapa 3.2: POC corrigida (Python 3.12 + PySUS 2.x), classificada como parcialmente suficiente.
- Revisão pós-Etapa 3.2: autorização para avançar com validação operacional controlada e fallback planejado.

## 3. Ambiente usado
- Branch: `work`
- Commit HEAD: `b97c12e9a161a811795f917a94897940141e064d`
- Último commit: `b97c12e Merge pull request #52 from paulobmcosta-creator/codex/conduct-post-execution-review-for-step-3.2`
- Python usado: `3.12.3`
- Caminho do Python: `/workspace/Observatorio_SUS_ES/.venv-etapa4-cnes/bin/python`
- Pip: `pip 26.1.1`
- PySUS: `2.0.4`
- Caminho PySUS: `/workspace/Observatorio_SUS_ES/.venv-etapa4-cnes/lib/python3.12/site-packages/pysus/__init__.py`
- Status inicial do repositório: limpo.
- Status final do repositório: apenas arquivos permitidos alterados/criados nesta etapa.

## 4. Arquivos criados ou alterados
- `docs/migracao_python/04_contratos_extracao_cnes_python.md`
- `python/observatorio_sus/cnes/__init__.py`
- `python/observatorio_sus/cnes/contratos.py`
- `python/observatorio_sus/extract/validar_extracao_cnes_controlada.py`
- `tests/python/test_contratos_cnes.py`
- `tests/python/test_validar_extracao_cnes_controlada_cli.py`

Confirmado: não houve alteração de scripts R, dados, metadados, `docs/cnes`, workflows, `.gitignore` ou `.gitattributes`.

## 5. Contratos CNES definidos
Foram definidos contratos mínimos para:
- Tabelas de estabelecimentos: `tbEstabelecimento`, `tbMunicipio`, `rlEstabSubTipo`, `tbSubTipo`, `rlEstabAtendPrestConv`, `tbAtendimentoPrestado`, `tbConvenio`, `tbTipoEstabelecimento`, `tbNaturezaJuridica`, `tbGestao`.
- Tabelas de habilitações: `rlEstabSipac`, `tbSubGruposHabilitacao`, `base_estabelecimentos` (dependência derivada futura).

Campos críticos por tabela foram explicitados, incluindo obrigatoriamente `CO_UNIDADE`, `CO_CNES`, componentes da chave composta de habilitação e campos temporais de vigência. Campos textuais obrigatórios foram definidos para preservar códigos e evitar coerção numérica indevida.

Chaves e regras preservadas:
- chave operacional CNES: `co_unidade`/`CO_UNIDADE`;
- código público: `cnes`/`CO_CNES`;
- integração de habilitações por `co_unidade`;
- chave de habilitação composta: `codigo_habilitacao` + `tipo_habilitacao`.

Relação com `metadata/cnes`: os contratos Python refletem os schemas e dicionários já estabelecidos sem substituí-los.

## 6. Relação entre contratos Python e contratos metodológicos existentes
- `metadata/cnes` continua sendo fonte normativa.
- `docs/cnes` continua sendo fonte metodológica.
- Contratos Python são camada experimental derivada para validação operacional.
- Em caso de divergência, prevalecem documentação e metadados oficiais até revisão formal.

## 7. Validação operacional controlada com PySUS 2.x
Comando executado:
- `python python/observatorio_sus/extract/validar_extracao_cnes_controlada.py --uf ES --competencia 202601 --modo diagnostico`

Resultado:
- Modo executado: `diagnostico`.
- Não houve tentativa remota de extração.
- Não houve download de dados.
- Não houve gravação de artefatos em diretórios do repositório.
- Módulos/objetos relevantes identificados no PySUS incluem `pysus.api.ftp`, `pysus.api.ftp.client`, `pysus.api.ftp.databases`, com classes `CNES`, `FTPClient` etc.

## 8. Cobertura de tabelas e campos

| Tabela lógica | Necessária para | Campos críticos | Cobertura PySUS 2.x | Evidência | Fallback necessário? | Observação |
|---|---|---|---|---|---|---|
| tbEstabelecimento | estabelecimentos | CO_UNIDADE, CO_CNES, CO_MUNICIPIO_GESTOR, NO_FANTASIA, NO_RAZAO_SOCIAL, TP_GESTAO | parcialmente_confirmado | diagnóstico por módulos/objetos CNES | Sim | sem extração real nesta etapa |
| tbMunicipio | estabelecimentos | CO_MUNICIPIO, NO_MUNICIPIO, CO_UF | parcialmente_confirmado | diagnóstico por módulos/objetos CNES | Sim | sem validação empírica de linhas |
| rlEstabSubTipo | estabelecimentos | CO_UNIDADE | nao_confirmado | ausência de confirmação específica | Sim | fallback provável |
| tbSubTipo | estabelecimentos | CO_SUB_TIPO, NO_SUB_TIPO | nao_confirmado | ausência de confirmação específica | Sim | fallback provável |
| rlEstabAtendPrestConv | estabelecimentos | CO_UNIDADE | nao_confirmado | ausência de confirmação específica | Sim | fallback provável |
| tbAtendimentoPrestado | estabelecimentos | CO_ATENDIMENTO, NO_ATENDIMENTO | nao_confirmado | ausência de confirmação específica | Sim | fallback provável |
| tbConvenio | estabelecimentos | CO_CONVENIO, NO_CONVENIO | nao_confirmado | ausência de confirmação específica | Sim | fallback provável |
| tbTipoEstabelecimento | estabelecimentos | CO_TIPO_ESTABELECIMENTO, NO_TIPO_ESTABELECIMENTO | nao_confirmado | ausência de confirmação específica | Sim | fallback provável |
| tbNaturezaJuridica | estabelecimentos | CO_NATUREZA_JURIDICA, NO_NATUREZA_JURIDICA | nao_confirmado | ausência de confirmação específica | Sim | fallback provável |
| tbGestao | estabelecimentos | CO_GESTAO, NO_GESTAO | nao_confirmado | ausência de confirmação específica | Sim | limitação metodológica mantida |
| rlEstabSipac | habilitações | CO_UNIDADE, COD_SUB_GRUPO_HABILITACAO, TP_HABILITACAO, CMTP_INICIO, CMTP_FIM, NU_LEITOS, NO_PORTARIA, DT_ATUALIZACAO | parcialmente_confirmado | diagnóstico por palavras-chave e objetos CNES | Sim | sem extração controlada nesta etapa |
| tbSubGruposHabilitacao | habilitações | CO_CODIGO_GRUPO, TP_HABILITACAO, NO_DESCRICAO_GRUPO, TP_ORIGEM | parcialmente_confirmado | diagnóstico por palavras-chave e objetos CNES | Sim | sem extração controlada nesta etapa |

## 9. Fallback planejado
Classificação preliminar:
- fallback não necessário: nenhum confirmado nesta etapa.
- fallback provável: tabelas não confirmadas em diagnóstico (`rlEstabSubTipo`, `tbSubTipo`, `rlEstabAtendPrestConv`, `tbAtendimentoPrestado`, `tbConvenio`, `tbTipoEstabelecimento`, `tbNaturezaJuridica`, `tbGestao`, `base_estabelecimentos`).
- fallback obrigatório: inconclusivo nesta etapa, depende da Etapa 5.
- inconclusivo: cobertura por API pública de tabela a tabela.

Estratégia permitida para próximas etapas:
- PySUS como camada principal quando suportar tabela com recorte seguro.
- fallback controlado em DATASUS/FTP quando PySUS não expuser tabela.
- leitor DBC/DBF próprio apenas se necessário.
- preservação de manifestos, hash, origem, competência, UF e parâmetros.
- sem implementação plena de fallback nesta etapa.

## 10. Testes Python executados
- `python -m pytest tests/python`
- Resultado: 17 testes aprovados.
- Novos testes: `test_contratos_cnes.py` e `test_validar_extracao_cnes_controlada_cli.py`.
- Dependência de rede: não para testes unitários/CLI; instalação de dependências ocorreu na preparação do ambiente.
- Falhas: nenhuma.
- Limitações: cobertura operacional ainda diagnóstica, sem validação empírica de extração remota nesta etapa.

## 11. Perguntas obrigatórias respondidas

| Pergunta | Resposta | Evidência | Implicação |
|---|---|---|---|
| 1. Existem contratos programáticos mínimos para CNES? | Sim. | `contratos.py` e testes de contratos. | Base mínima para evolução controlada. |
| 2. Os contratos contemplam co_unidade? | Sim. | Campos críticos e textuais definidos. | Preserva chave operacional. |
| 3. Os contratos contemplam cnes/CO_CNES? | Sim. | Campos críticos e textuais definidos. | Preserva código público. |
| 4. Os contratos contemplam rlEstabSipac? | Sim. | Tabela e campos críticos incluídos. | Habilitações podem ser validadas estruturalmente. |
| 5. Os contratos contemplam tbSubGruposHabilitacao? | Sim. | Tabela e campos críticos incluídos. | Permite chave composta com tipo. |
| 6. O script de validação controlada executa sem gravar dados? | Sim. | Modo diagnóstico com JSON e `tempfile`. | Evita poluir repositório. |
| 7. PySUS 2.x confirma alguma cobertura operacional CNES? | Sim, parcial. | Módulos/objetos CNES no diagnóstico. | Viabilidade inicial, sem cobertura total. |
| 8. Quais tabelas permanecem sem cobertura confirmada? | `rlEstabSubTipo`, `tbSubTipo`, `rlEstabAtendPrestConv`, `tbAtendimentoPrestado`, `tbConvenio`, `tbTipoEstabelecimento`, `tbNaturezaJuridica`, `tbGestao`, `base_estabelecimentos`. | JSON de diagnóstico. | Necessidade de fallback planejado. |
| 9. Quais campos permanecem sem cobertura confirmada? | Campos de tabelas não confirmadas; cobertura de `CO_UNIDADE`/`CO_CNES` apenas parcial nesta etapa. | JSON de diagnóstico e contratos. | Exige validação empírica na Etapa 5. |
| 10. Fallback será necessário? | Sim, provavelmente. | Classificação de cobertura e lista de fallback. | Planejamento operacional obrigatório. |
| 11. A dependência de Git LFS pode ser reduzida? | Potencialmente, sim, no médio prazo. | Extração controlada em Python + contratos. | Depende de cobertura real na Etapa 5. |
| 12. A Etapa 5 pode avançar para extração mínima real? | Sim, com salvaguardas estritas. | Classificação desta etapa como parcial suficiente. | Avançar sem substituir R. |
| 13. Algum script R pode ser substituído agora? | **Não. Nenhum script R sensível pode ser substituído nesta etapa.** | Escopo e conclusões da Etapa 4. | R permanece oráculo. |

## 12. Classificação da Etapa 4
**CONTRATOS_DEFINIDOS_E_VALIDACAO_OPERACIONAL_PARCIAL**.

Critério: contratos mínimos foram definidos e validados por testes; cobertura operacional via PySUS permanece incompleta, com fallback necessário.

## 13. Implicações para a Etapa 5
Recomendação: **Etapa 5 — Extração mínima real CNES em diretório temporário e comparação estrutural com contratos**.

Restrições mandatórias para Etapa 5:
- proibido substituir scripts R;
- proibido escrever em `data_interim`;
- proibido alterar metadados;
- proibido alterar classificação de habilitações.

## 14. Riscos remanescentes
- cobertura parcial do PySUS;
- ausência de API pública estável para todas as tabelas;
- necessidade de fallback;
- risco de download massivo involuntário;
- coerção numérica de códigos;
- divergência entre contratos Python e `metadata/cnes`;
- duplicação R/Python;
- dependência de rede;
- persistência parcial do risco Git LFS;
- risco de avançar transformação antes da extração validada.

## 15. Critérios de aceite
- [x] Documento da Etapa 4 criado.
- [x] Contratos Python mínimos criados.
- [x] Script de validação operacional controlada criado.
- [x] requirements conferido para PySUS 2.x.
- [x] Testes Python de contratos criados.
- [x] Testes Python de CLI criados.
- [x] Testes Python executados.
- [x] Diagnóstico controlado executado.
- [x] Cobertura de tabelas registrada.
- [x] Fallback planejado registrado.
- [x] Nenhum script R alterado.
- [x] Nenhum teste R alterado.
- [x] Nenhum dado alterado.
- [x] Nenhum metadado alterado.
- [x] Nenhum docs/cnes alterado.
- [x] Nenhum workflow alterado.
- [x] Nenhum arquivo de configuração Git alterado.
- [x] Ambiente virtual removido ou não versionado.

## 16. Conclusão
A Etapa 4 definiu contratos programáticos mínimos CNES, validou a execução controlada do diagnóstico em Python 3.12 com PySUS 2.0.4 e explicitou cobertura parcial por tabela/campo. A validação operacional não substituiu pipeline R, não gerou produtos finais e não alterou dados ou metadados oficiais. O avanço para Etapa 5 é possível sob controle estrito, com fallback planejado e manutenção de R como oráculo metodológico.
