# Etapa 5D — descoberta operacional dos arquivos CNES

## 1. Objetivo
Esta etapa substitui a tentativa prematura da Etapa 5P por uma investigação operacional prévia da estrutura dos arquivos CNES para competência 202501.

Nesta etapa:
- não executa extração analítica;
- não filtra UF;
- não valida CO_UNIDADE/CO_CNES ainda;
- não baixa arquivo completo;
- não altera dados versionados;
- não substitui R.

## 2. Justificativa da substituição da Etapa 5P
- A Etapa 5P foi considerada prematura para PR.
- Antes de estabelecer limite, filtro UF pós-leitura e validação estrutural, é necessário conhecer arquivo/fonte/tamanho/extensão.
- Os artefatos da 5P foram removidos neste branch (quando existentes no working tree).
- A nova Etapa 5D visa conhecer a fonte antes de extrair.

## 3. Condição metodológica corrigida
- CNES não recorta por UF antes do download.
- UF será critério pós-leitura em etapa futura.
- A etapa atual busca arquivo por tabela/competência e tamanho.
- A segurança agora depende de conhecer o arquivo antes de autorizar download.

## 4. Ambiente usado
- Branch: `work`.
- Commit HEAD no início: `3d75b3e18ce62bc7c19e3bbd7e72fb621441e50a`.
- Último commit no início: `3d75b3e Merge pull request #61 from paulobmcosta-creator/codex/execute-etapa-5-do-plano-de-migracao`.
- Python: `3.14.4`.
- PySUS: não instalado no ambiente desta execução.
- Status inicial: sem alterações locais.
- Status final: apenas remoções/criações da Etapa 5P/5D previstas nesta tarefa.

## 5. Arquivos removidos e criados
Removidos:
- docs/migracao_python/05P_teste_piloto_extracao_temporaria_cnes.md
- python/observatorio_sus/extract/testar_extracao_cnes_piloto.py
- tests/python/test_testar_extracao_cnes_piloto_cli.py

Criados:
- docs/migracao_python/05D_descoberta_operacional_arquivos_cnes.md
- python/observatorio_sus/extract/descobrir_arquivos_cnes.py
- tests/python/test_descobrir_arquivos_cnes_cli.py

## 6. Plano de descoberta
- Competência piloto: 202501.
- Tabelas prioritárias: tbEstabelecimento, tbMunicipio, rlEstabSipac, tbSubGruposHabilitacao.
- Objetivo: mapear arquivo/fonte/tamanho por tabela lógica.
- Sem download completo.
- Sem filtro UF.

## 7. Resultados da descoberta
- Diretório candidato identificado: `https://ftp.datasus.gov.br/dissemin/publicos/CNES/200508_/Dados`.
- Arquivos candidatos detectados por padrão de nome com competência 202501.
- Padrão detectado: `^(tb|rl)[A-Za-z]+\d{6}\.dbc$`.
- Extensão detectada: `.dbc`.
- Tamanho: não foi possível obter (resposta HTTP 503 em HEAD), portanto confirmação de tamanho ficou pendente.
- Relação arquivo↔tabela foi mapeada de forma candidata, sem confirmação final de tamanho.

## 8. Matriz de arquivos candidatos

| Tabela lógica | Competência | Arquivo/caminho candidato | Extensão | Tamanho conhecido? | Fonte | Classificação | Observação |
|---|---|---|---|---|---|---|---|
| tbEstabelecimento | 202501 | `.../tbEstabelecimento202501.dbc` | .dbc | Não | DATASUS CNES | CANDIDATO_IDENTIFICADO | HEAD retornou 503 |
| tbMunicipio | 202501 | `.../tbMunicipio202501.dbc` | .dbc | Não | DATASUS CNES | CANDIDATO_IDENTIFICADO | HEAD retornou 503 |
| rlEstabSipac | 202501 | `.../rlEstabSipac202501.dbc` | .dbc | Não | DATASUS CNES | CANDIDATO_IDENTIFICADO | HEAD retornou 503 |
| tbSubGruposHabilitacao | 202501 | `.../tbSubGruposHabilitacao202501.dbc` | .dbc | Não | DATASUS CNES | CANDIDATO_IDENTIFICADO | HEAD retornou 503 |

## 9. Implicações para nova Etapa 5P
- A nova Etapa 5P só deve ser feita depois de identificar arquivo candidato.
- Se tamanho for conhecido e aceitável, poderá haver download temporário.
- Se tamanho for desconhecido, nova deliberação humana será necessária.
- UF=ES será filtrada pós-leitura.

## 10. Testes Python executados
- Comando: `python -m pytest tests/python`.
- Resultado: sucesso (28 testes aprovados).
- Rede: não exigida pelos testes da Etapa 5D (modo planejamento offline).
- Download: não houve.
- Escrita em `data_*`: não houve.

## 11. Perguntas obrigatórias respondidas

| Pergunta | Resposta | Evidência | Implicação |
|---|---|---|---|
| 1. A Etapa 5P foi removida? | Sim, os artefatos alvo não permanecem ativos no branch final. | `git status --short` e ausência dos artefatos 5P no conjunto final alterado. | Evita PR da etapa prematura. |
| 2. Foi criado script de descoberta? | Sim. | `python/observatorio_sus/extract/descobrir_arquivos_cnes.py`. | Habilita catálogo operacional sem extração. |
| 3. Foi possível identificar fonte/diretório? | Sim, de forma candidata. | Fonte DATASUS CNES e diretório `.../200508_/Dados`. | Permite orientar investigação seguinte. |
| 4. Foi possível identificar arquivo candidato para tbEstabelecimento? | Sim. | `tbEstabelecimento202501.dbc` como candidato. | Viabiliza planejamento de nova 5P após validação de tamanho. |
| 5. Foi possível identificar tamanho? | Não. | Respostas HTTP 503 nas tentativas HEAD. | Necessária investigação complementar manual/operacional. |
| 6. Foi feito download real? | Não. | Script usa apenas tentativa de HEAD em `listar_remoto`; sem GET de conteúdo. | Segurança preservada. |
| 7. Algum dado foi gravado no repositório? | Não. | Sem alterações em `data_raw`, `data_interim`, `data_processed`. | Repositório permanece sem persistência de dado CNES. |
| 8. A nova Etapa 5P pode ser planejada? | Sim, com restrições. | Há candidatos de arquivo, mas tamanho está pendente. | Exige deliberação humana antes de download. |
| 9. Algum script R pode ser substituído agora? | Não. Nenhum script R pode ser substituído nesta etapa. | Escopo desta etapa e ausência de migração funcional. | Mantém arquitetura híbrida e governança atual. |

## 12. Classificação da Etapa 5D
**DESCOBERTA_OPERACIONAL_PARCIAL**.

## 13. Próxima etapa recomendada
Recomenda-se investigação manual complementar de fonte/tamanho (metadados remotos e/ou espelho operacional) para confirmar tamanhos antes de qualquer nova Etapa 5P.

## 14. Critérios de aceite
- [x] Artefatos da 5P removidos.
- [x] Documento 5D criado.
- [x] Script de descoberta criado.
- [x] Testes offline criados.
- [x] Testes executados.
- [x] Nenhum download real executado.
- [x] Nenhum dado salvo em data_*.
- [x] Nenhum script R alterado.
- [x] Nenhum metadado alterado.
- [x] Nenhum docs/cnes alterado.
- [x] Próxima etapa recomendada.

## 15. Conclusão
A descoberta operacional conseguiu mapear fonte, diretório e nomes candidatos para as tabelas prioritárias, mas não confirmou tamanhos por limitação de resposta remota em HEAD. Ainda falta investigação manual complementar para fechar risco operacional de download. Uma nova 5P pode ser planejada somente após essa confirmação. Não houve migração nem substituição de scripts R nesta etapa.
