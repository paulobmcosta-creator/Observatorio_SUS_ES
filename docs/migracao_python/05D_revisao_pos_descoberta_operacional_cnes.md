# Revisão pós-Etapa 5D — descoberta operacional dos arquivos CNES

## 1. Objetivo da revisão
Esta revisão audita criticamente a Etapa 5D antes de qualquer nova tentativa de download/leitura temporária.

Esta revisão:
- não implementa nova funcionalidade;
- não executa extração real;
- não baixa dados CNES completos;
- não altera dados versionados;
- não altera scripts R;
- apenas audita se a descoberta operacional foi suficiente.

## 2. Insumos verificados

### 2.1 Documentos de migração
- `docs/migracao_python/00_baseline_r_pre_migracao.md`
- `docs/migracao_python/01_classificacao_legado_r.md`
- `docs/migracao_python/02_governanca_arquitetura_hibrida.md`
- `docs/migracao_python/03_poc_pysus_cnes.md`
- `docs/migracao_python/04_contratos_extracao_cnes_python.md`
- `docs/migracao_python/04_revisao_pos_etapa4.md`
- `docs/migracao_python/04_deliberacao_humana_pre_etapa5.md`
- `docs/migracao_python/05R_reinicio_etapa5_recorte_cnes_pos_download.md`
- `docs/migracao_python/05D_descoberta_operacional_arquivos_cnes.md`

### 2.2 Código Python
- `python/observatorio_sus/extract/descobrir_arquivos_cnes.py`
- `python/observatorio_sus/cnes/contratos.py`
- `python/observatorio_sus/io/manifestos.py`
- `python/observatorio_sus/utils/normalizacao.py`

### 2.3 Testes Python
- `tests/python/test_descobrir_arquivos_cnes_cli.py`
- `tests/python/test_contratos_cnes.py`
- `tests/python/test_validar_extracao_cnes_controlada_cli.py`
- `tests/python/test_estrutura_python_minima.py`

### 2.4 Dependências
- `requirements-python-poc.txt`

## 3. Ambiente de revisão
- Branch: `work`
- Commit HEAD (início desta revisão): `9b451ebe2b4ef685f8460efd73cde740ae6a2617`
- Último commit (início desta revisão): `9b451eb Merge pull request #62 from paulobmcosta-creator/codex/remove-etapa-5p-e-cria-5d`
- Status inicial: limpo (sem alterações)
- Python usado: `3.12.3`
- Caminho Python: `.venv-review-5d-cnes/bin/python`
- pip: `26.1.1`
- PySUS: `2.0.4`
- Caminho PySUS: `.venv-review-5d-cnes/lib/python3.12/site-packages/pysus/__init__.py`
- Status final: apenas criação deste documento de revisão

## 4. Verificação da substituição da Etapa 5P

| Item | Resultado | Evidência | Observação |
|---|---|---|---|
| Artefatos da 5P prematura removidos | Sim | `05D_descoberta_operacional_arquivos_cnes.md` descreve remoção/substituição da 5P | Não há reativação da proposta prematura no fluxo atual |
| 5D criada | Sim | Existência de `05D_descoberta_operacional_arquivos_cnes.md` | Condição prévia atendida |
| Justificativa da substituição documentada | Sim | Seções de contexto/conclusão da 5D registram correção metodológica | Alinhado à governança híbrida |
| Premissa de UF pós-download registrada | Sim | Documento 5D e 05R registram recorte UF após leitura temporária | Sem recorte UF pré-download |
| Referências ativas indevidas à 5P prematura | Não identificadas | Conjunto documental da migração analisado | Mantida a sequência 5D -> deliberação humana -> possível nova 5P |

## 5. Verificação do script descobrir_arquivos_cnes.py

| Critério | Resultado | Evidência | Fragilidade | Observação |
|---|---|---|---|---|
| Possui argparse | Sim | `--help` funcional e opções declaradas | Baixa | CLI consistente |
| Possui modos planejamento, inspecao_local, listar_remoto e resumo | Sim | `--modo {planejamento,inspecao_local,listar_remoto,resumo}` | Baixa | Modo `resumo` presente no parser |
| Produz JSON | Sim | Saída dos 3 modos executados em JSON | Baixa | Estrutura padronizada |
| Usa contratos CNES | Sim | Importa `listar_tabelas_obrigatorias` e `obter_contrato_tabela` | Baixa | Acoplamento explícito à Etapa 4 |
| Não baixa dados no planejamento | Sim | Conclusão explicita sem rede/sem download | Baixa | Offline por desenho |
| Não baixa dados no inspecao_local | Sim | Inspeção apenas de módulos locais | Baixa | Sem leitura remota |
| `listar_remoto` restrito a metadados leves | Sim | Conclusão indica HEAD/metadados; sem GET de corpo | Média | Dependência de resposta do servidor a HEAD |
| Não escreve em data_raw/data_interim/data_processed | Sim | Teste dedicado + status git sem alterações em data_* | Baixa | Guardrail explícito |
| Classifica tabelas prioritárias | Sim | `relacao_arquivo_tabela` preenchida por tabela lógica | Baixa | Inclui 4 tabelas exigidas |
| Registra risco de download | Sim | Campo `risco_download` por modo | Baixa | Escala de risco declarada |
| Registra próxima recomendação | Sim | Campo `proxima_recomendacao` presente | Baixa | Bom para decisão de etapa seguinte |

## 6. Verificação dos testes Python
- Comando executado: `python -m pytest tests/python`
- Resultado: sucesso
- Número de testes: 28
- Falhas: 0
- Dependência de rede: não obrigatória para os testes executados
- Download de dados: não evidenciado
- Verificação de planejamento: coberta por `test_descobrir_arquivos_cnes_cli.py`
- Proteção de `data_raw/data_interim/data_processed`: coberta por teste que valida não mutação de mtime

Classificação de cobertura: **suficiente** para a auditoria da Etapa 5D no escopo desta revisão.

## 7. Verificação dos modos CLI

| Modo | Exit code | Rede? | Download? | Escrita? | Resultado | Observação |
|---|---:|---|---|---|---|---|
| `--help` | 0 | Não | Não | Não | Mostrou uso e modos válidos | OK |
| `planejamento` | 0 | Não | Não | Não | JSON com plano offline e risco baixo | Seguro |
| `inspecao_local` | 0 | Não | Não | Não | JSON com inspeção de módulos locais | Seguro |
| `listar_remoto` | 0 | Sim (metadados) | Não | Não | JSON com candidatos e extensão `.dbc` | Tamanho não retornado nesta execução |

## 8. Avaliação dos achados operacionais

| Tabela lógica | Arquivo candidato identificado? | Caminho/fonte identificado? | Extensão identificada? | Competência identificada? | Tamanho identificado? | Classificação da 5D | Implicação para nova 5P |
|---|---|---|---|---|---|---|---|
| tbEstabelecimento | Sim | Sim (`.../Dados/tbEstabelecimento202501.dbc`) | Sim (`.dbc`) | Sim (`202501`) | Não | CANDIDATO_IDENTIFICADO | Requer confirmação de tamanho antes de piloto |
| tbMunicipio | Sim | Sim (`.../Dados/tbMunicipio202501.dbc`) | Sim (`.dbc`) | Sim (`202501`) | Não | CANDIDATO_IDENTIFICADO | Pode ser candidato secundário |
| rlEstabSipac | Sim | Sim (`.../Dados/rlEstabSipac202501.dbc`) | Sim (`.dbc`) | Sim (`202501`) | Não | CANDIDATO_IDENTIFICADO | Dependente de limite de tamanho |
| tbSubGruposHabilitacao | Sim | Sim (`.../Dados/tbSubGruposHabilitacao202501.dbc`) | Sim (`.dbc`) | Sim (`202501`) | Não | CANDIDATO_IDENTIFICADO | Pode apoiar etapa de habilitações depois |

## 9. Avaliação da suficiência da descoberta
Classificação: **PARCIALMENTE_SUFICIENTE_PARA_5P**.

Justificativa: há fonte e arquivos candidatos por tabela, extensão `.dbc` e competência `202501`, porém sem confirmação de tamanho remoto nesta execução.

## 10. Decisão sobre próxima etapa
Decisão recomendada: **2. Etapa 5D.1 — investigação manual complementar da fonte/tamanho.**

Observação complementar: se a decisão humana aceitar risco sem tamanho confirmado, pode ser necessário acionar **3. Etapa 5M** antes de qualquer nova 5P.

## 11. Revisão humana necessária
Sim, recomenda-se revisão humana para deliberar:
- autorização de download temporário quando tamanho permanecer desconhecido;
- limite máximo de tamanho aceitável para piloto;
- tabela piloto inicial (preferência metodológica: `tbEstabelecimento`);
- competência piloto (`202501` ou outra);
- aceitação de arquivo nacional por competência;
- aceitação de biblioteca de conversão DBC/DBF para leitura temporária;
- aceitação de HEAD/listagem remota como evidência suficiente.

## 12. Pendências

### 12.1 Bloqueantes antes de nova 5P
- confirmação de tamanho remoto dos arquivos candidatos;
- definição formal do limite máximo de tamanho para piloto;
- confirmação operacional estável da fonte remota para metadados.

### 12.2 Relevantes, mas não bloqueantes
- priorização final entre tbEstabelecimento e demais tabelas candidatas;
- detalhamento adicional do padrão de nomes para competências futuras;
- validação complementar do caminho remoto em espelho alternativo (se houver).

### 12.3 Melhorias futuras
- catálogo versionado apenas de metadados CNES (sem dados reais);
- tabela de padrões de nomes por tabela/competência;
- matriz tabela lógica x arquivo remoto x extensão x tamanho;
- testes com fixture sintética de respostas HEAD/listagem;
- componente temporário controlado para leitura DBC/DBF sem persistência.

## 13. Perguntas obrigatórias respondidas

| Pergunta | Resposta | Evidência | Implicação |
|---|---|---|---|
| 1. A Etapa 5D foi concluída? | Sim | Documento 5D existente e analisado | Permite auditoria pós-etapa |
| 2. A 5P prematura foi removida? | Sim | Registro documental da substituição 5P -> 5D | Reduz risco metodológico |
| 3. O script de descoberta existe? | Sim | `python/observatorio_sus/extract/descobrir_arquivos_cnes.py` | Habilita descoberta operacional |
| 4. O modo planejamento funciona? | Sim | Execução com exit code 0 e JSON offline | Planejamento seguro |
| 5. O modo listar_remoto baixou dados? | Não | Execução sem escrita e sem conteúdo CNES persistido | Mantém restrição de segurança |
| 6. Foi identificado arquivo candidato para tbEstabelecimento? | Sim | `tbEstabelecimento202501.dbc` em fonte CNES | Candidato piloto possível |
| 7. Foi identificado tamanho? | Não | Campo `tamanhos_detectados` vazio na execução | Exige 5D.1/5M antes de 5P |
| 8. Foi identificada extensão? | Sim | Extensão `.dbc` detectada | Reduz incerteza técnica |
| 9. Há base para nova 5P? | Parcial | Candidatos identificados sem tamanho confirmado | Não iniciar 5P sem complemento |
| 10. Algum dado foi gravado no repositório? | Não | `git status --short` sem alterações em data_* | Conformidade com escopo |
| 11. Algum script R pode ser substituído agora? | **Não. Nenhum script R pode ser substituído nesta etapa.** | Escopo da revisão e ausência de migração funcional | R permanece oráculo metodológico |

## 14. Critérios de aceite da revisão
- [x] Documento de revisão pós-5D criado.
- [x] Documento da 5D analisado.
- [x] Script de descoberta analisado.
- [x] Testes Python executados.
- [x] Modos CLI executados.
- [x] Ausência de download de dados confirmada.
- [x] Ausência de escrita em data_* confirmada.
- [x] Achados por tabela avaliados.
- [x] Suficiência para nova 5P classificada.
- [x] Próxima etapa recomendada.
- [x] Nenhum script R alterado.
- [x] Nenhum dado alterado.
- [x] Nenhum metadado alterado.
- [x] Nenhum docs/cnes alterado.
- [x] Nenhum workflow alterado.

## 15. Conclusão
A Etapa 5D é aprovada como descoberta operacional **parcial**, com mapeamento consistente de fonte/caminho/candidatos/extensão para competência piloto, porém sem confirmação de tamanho remoto nesta revisão.

Assim, há base **parcial** para planejar nova 5P, mas ainda há necessidade de investigação manual complementar (5D.1) e possível deliberação humana (5M) antes de qualquer download/leitura temporária.

Reafirma-se que não houve migração nem substituição de R nesta revisão.

## 16. Conformidade final de arquivos alterados
- `git status --short` final: sem alterações pendentes após commit.
- Arquivo criado nesta revisão: `docs/migracao_python/05D_revisao_pos_descoberta_operacional_cnes.md`.
- Arquivos adicionais editados: nenhum.
- Confirmação de escopo: não houve alteração em scripts R, testes R, `data_raw`, `data_interim`, `data_processed`, `metadata/`, `docs/cnes/`, workflows, `.gitignore` ou `.gitattributes`.
