# Investigação de recorte seguro e fallback CNES/DATASUS/FTP

## 1. Objetivo da Etapa 5S
Esta etapa investiga caminhos seguros de fonte/fallback para CNES/ES/2025 após a Etapa 5 ter sido bloqueada por ausência de recorte seguro confirmado.

Escopo:
- não executa extração real;
- não baixa dados CNES completos;
- não substitui scripts R;
- não altera `data_raw`/`data_interim`/`data_processed`;
- não altera `metadata`;
- não altera `docs/cnes`;
- não aplica classificação de habilitações.

## 2. Contexto herdado
- Etapa 4 definiu contratos mínimos CNES.
- Deliberação humana autorizou Etapa 5 com escopo estrito.
- Etapa 5 tentou extração temporária.
- O bloqueio hardcoded foi removido na correção posterior.
- A checagem dinâmica não identificou assinatura operacional com UF+competência.
- Etapa 5 foi classificada como `EXTRACAO_NAO_EXECUTADA_POR_SEGURANCA`.
- Portanto, a Etapa 5S investiga recorte seguro/fallback antes de nova tentativa de extração.

## 3. Ambiente usado
- Branch: `work`
- HEAD: `466cc277ece7b1e63b1de2fb7335b4c288edcc5c`
- Último commit: `466cc27 Add Etapa 5 temporary CNES extraction (ES/2025) with safety gating, docs and tests`
- Python: `3.12.3`
- Executável Python: `/workspace/Observatorio_SUS_ES/.venv-etapa5s-cnes/bin/python`
- Pip: `26.1.1`
- PySUS: `2.0.4`
- Caminho PySUS: `/workspace/Observatorio_SUS_ES/.venv-etapa5s-cnes/lib/python3.12/site-packages/pysus/__init__.py`
- Status inicial: somente novos arquivos da Etapa 5S
- Status final: somente arquivos permitidos da Etapa 5S

## 4. Arquivos criados ou alterados
- `docs/migracao_python/05S_investigacao_recorte_fallback_cnes.md`
- `python/observatorio_sus/extract/investigar_fallback_cnes.py`
- `tests/python/test_investigar_fallback_cnes_cli.py`

Confirmação: não houve alteração em scripts R, dados, metadados, `docs/cnes`, workflows, `.gitignore` ou `.gitattributes`.

## 5. Plano de investigação
- UF=ES
- ano=2025
- competências 202501–202512
- tabelas prioritárias: `tbEstabelecimento`, `tbMunicipio`, `rlEstabSipac`, `tbSubGruposHabilitacao`
- PySUS como via principal de inspeção
- DATASUS/FTP como fallback investigado conceitualmente
- sem download real
- sem escrita em dados versionados

## 6. Inspeção PySUS
Resumo da inspeção local do pacote instalado:
- módulos relevantes encontrados: 4 (com termos CNES/FTP/DATASUS)
- classes/funções relevantes encontradas: sim
- candidatos com assinatura simultânea UF+competência: 0
- evidência de listagem sem download: parcial, não conclusiva para todas as tabelas
- método de tamanho/metadata antes de download: não confirmado

Limitações:
- assinatura operacional inequívoca por tabela+competência+UF não identificada;
- metadados de tamanho pré-download não confirmados para cenário de extração controlada.

## 7. Fontes e arquivos candidatos
| Tabela lógica | Competência | Fonte candidata | Nome/caminho remoto candidato | UF explícita? | Competência explícita? | Tamanho conhecido? | Exige download? | Recorte seguro | Observação |
|---|---|---|---|---|---|---|---|---|---|
| tbEstabelecimento | 2025MM | PySUS/DATASUS-FTP (inspeção) | não_confirmado_sem_listagem_dedicada | Não | Não | Não | Sim | RECORTE_NAO_CONFIRMADO | Apenas inspeção/listagem leve sem download |
| tbMunicipio | 2025MM | PySUS/DATASUS-FTP (inspeção) | não_confirmado_sem_listagem_dedicada | Não | Não | Não | Sim | RECORTE_NAO_CONFIRMADO | Apenas inspeção/listagem leve sem download |
| rlEstabSipac | 2025MM | PySUS/DATASUS-FTP (inspeção) | não_confirmado_sem_listagem_dedicada | Não | Não | Não | Sim | RECORTE_NAO_CONFIRMADO | Apenas inspeção/listagem leve sem download |
| tbSubGruposHabilitacao | 2025MM | PySUS/DATASUS-FTP (inspeção) | não_confirmado_sem_listagem_dedicada | Não | Não | Não | Sim | RECORTE_NAO_CONFIRMADO | Apenas inspeção/listagem leve sem download |

## 8. Matriz de recorte seguro
| Tabela lógica | Recorte por tabela | Recorte por competência | Recorte por UF | Tamanho antes do download | Classificação do recorte | Implicação |
|---|---|---|---|---|---|---|
| tbEstabelecimento | parcial | não_confirmado | não_confirmado | não | RECORTE_NAO_CONFIRMADO | Não avançar para extração real |
| tbMunicipio | parcial | não_confirmado | não_confirmado | não | RECORTE_NAO_CONFIRMADO | Não avançar para extração real |
| rlEstabSipac | parcial | não_confirmado | não_confirmado | não | RECORTE_NAO_CONFIRMADO | Exige fallback planejado |
| tbSubGruposHabilitacao | parcial | não_confirmado | não_confirmado | não | RECORTE_NAO_CONFIRMADO | Exige fallback planejado |

## 9. Matriz de fallback
| Tabela lógica | PySUS suficiente? | Fallback necessário? | Tipo de fallback | Segurança operacional | Próxima ação recomendada |
|---|---|---|---|---|---|
| tbEstabelecimento | Não | Sim | Fallback obrigatório | Controlada, com limite pré-aprovado | Etapa 5F piloto por competência |
| tbMunicipio | Não | Sim | Fallback obrigatório | Controlada, com limite pré-aprovado | Etapa 5F piloto por competência |
| rlEstabSipac | Não | Sim | Fallback obrigatório | Controlada, com limite pré-aprovado | Etapa 5F piloto por competência |
| tbSubGruposHabilitacao | Não | Sim | Fallback obrigatório | Controlada, com limite pré-aprovado | Etapa 5F piloto por competência |

## 10. Risco de download e limites operacionais
- Há risco de download amplo/nacional em fontes CNES sem recorte explícito por UF.
- Tamanho pré-download não foi confirmado nesta investigação.
- Há risco de arquivos grandes caso fallback seja acionado sem metadado prévio.
- Limitação por competência pode ser possível, mas não confirmada para todos os caminhos.
- Limitação por UF não foi confirmada.

Política recomendada para próxima etapa:
1. escolher competência piloto única (ex.: 202501);
2. definir limite máximo de tamanho antes de qualquer download;
3. abortar automaticamente se só houver caminho nacional amplo;
4. registrar manifesto operacional do fallback.

## 11. Testes Python executados
- Comando: `python -m pytest tests/python`
- Resultado: sucesso
- Número de testes: 25
- Dependência de rede: não para os testes; rede usada na instalação de dependências
- Escrita em dados versionados: não
- Falhas e limitações: nenhuma falha; cobertura de listagem remota real permanece fora do escopo dos testes offline

## 12. Perguntas obrigatórias respondidas
| Pergunta | Resposta | Evidência | Implicação |
|---|---|---|---|
| 1. PySUS permite identificar fonte CNES? | Sim, parcialmente. | Módulos CNES/FTP/DATASUS detectados na inspeção. | Útil para mapeamento, não suficiente para extração segura. |
| 2. PySUS permite listar arquivos CNES sem download? | Parcial/inconclusivo. | Há sinais de objetos de listagem, sem confirmação operacional completa. | Não autoriza extração real ainda. |
| 3. Há recorte por competência? | Não confirmado. | Zero candidatos com assinatura UF+competência. | Precisa fallback controlado. |
| 4. Há recorte por UF? | Não confirmado. | Zero candidatos com assinatura UF+competência. | Precisa fallback controlado. |
| 5. Há tamanho de arquivo antes do download? | Não confirmado. | `tamanho_conhecido=false` nas tabelas prioritárias. | Sem tamanho, risco operacional aumenta. |
| 6. Há fonte candidata para tbEstabelecimento? | Sim, em nível de fonte genérica. | PySUS/DATASUS-FTP identificado sem caminho remoto conclusivo. | Ainda sem recorte seguro confirmado. |
| 7. Há fonte candidata para tbMunicipio? | Sim, em nível de fonte genérica. | PySUS/DATASUS-FTP identificado sem caminho remoto conclusivo. | Ainda sem recorte seguro confirmado. |
| 8. Há fonte candidata para rlEstabSipac? | Sim, em nível de fonte genérica. | PySUS/DATASUS-FTP identificado sem caminho remoto conclusivo. | Ainda sem recorte seguro confirmado. |
| 9. Há fonte candidata para tbSubGruposHabilitacao? | Sim, em nível de fonte genérica. | PySUS/DATASUS-FTP identificado sem caminho remoto conclusivo. | Ainda sem recorte seguro confirmado. |
| 10. O fallback por DATASUS/FTP é viável? | Potencialmente viável. | Fontes detectadas + necessidade operacional registrada. | Requer governança e limites formais. |
| 11. O fallback é seguro para Etapa 5F? | Ainda não totalmente; depende de controles. | Risco de download amplo e tamanho não confirmado. | Só com competência piloto e limite máximo. |
| 12. Algum download real foi executado? | Não. | Execução em modo conservador. | Escopo de segurança respeitado. |
| 13. Algum dado foi gravado no repositório? | Não. | Sem escrita em `data_*`. | Governança preservada. |
| 14. Algum script R pode ser substituído agora? | **Não. Nenhum script R pode ser substituído nesta etapa.** | Etapa 5S é somente investigação. | R permanece oráculo. |

## 13. Classificação da Etapa 5S
**RECORTE_NAO_CONFIRMADO**

Justificativa:
- não foi possível confirmar recorte seguro por UF+competência com metadado/tamanho pré-download;
- fontes candidatas existem, mas sem caminho operacional inequívoco para extração segura nesta etapa.

## 14. Implicações para próxima etapa
Recomendação: **Etapa 5M — investigação manual da fonte DATASUS/CNES fora do Codex, ou revisão de estratégia**.

Observação: Etapa 5F só deve ocorrer após deliberação humana explícita de limites operacionais (tamanho, competência piloto e abortos automáticos).

## 15. Revisão humana necessária
**Sim, necessária** antes de qualquer etapa com tentativa de download temporário.

Deliberações necessárias:
- autorização para download temporário de arquivo específico;
- limite máximo de tamanho aceitável;
- competência piloto;
- tabela piloto;
- aceitabilidade de fallback direto DATASUS/FTP;
- riscos operacionais/institucionais.

## 16. Riscos remanescentes
- ausência de recorte por UF confirmado;
- possíveis arquivos nacionais por competência;
- tamanho desconhecido antes de download;
- mudança de API PySUS;
- FTP potencialmente instável;
- conversão futura DBC/DBF;
- possível necessidade de biblioteca adicional;
- risco operacional de dados reais temporários;
- ausência de validação empírica de `CO_UNIDADE`/`CO_CNES`.

## 17. Critérios de aceite
- [x] Documento da Etapa 5S criado.
- [x] Script de investigação criado.
- [x] Testes Python criados.
- [x] Testes Python executados.
- [x] Competências 202501–202512 consideradas.
- [x] PySUS inspecionado.
- [x] Fontes/fallback investigados.
- [x] Nenhum dado baixado integralmente.
- [x] Nenhum dado gravado no repositório.
- [x] Nenhum script R alterado.
- [x] Nenhum teste R alterado.
- [x] Nenhum metadado alterado.
- [x] Nenhum docs/cnes alterado.
- [x] Nenhum workflow alterado.
- [x] Classificação final registrada.
- [x] Próxima etapa recomendada.

## 18. Conclusão
Não foi identificado recorte seguro confirmado para CNES/ES/2025 nesta investigação. O fallback é potencialmente viável, mas sem segurança operacional plena sem deliberação humana adicional. Não há tabela/competência piloto automaticamente autorizada nesta etapa; isso deve ser definido em revisão humana prévia. A recomendação é seguir para decisão metodológica (Etapa 5M) e somente então, se aprovado, executar uma Etapa 5F controlada. Reafirma-se que não houve migração, extração real nem substituição de R.
