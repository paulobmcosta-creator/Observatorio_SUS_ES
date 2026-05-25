# Etapa 5M — deliberação humana sobre download piloto CNES sem limite prévio de tamanho

## 1. Objetivo
Este documento registra a deliberação humana complementar necessária antes de uma nova Etapa 5P.

A deliberação autoriza, de modo controlado, um download piloto de arquivo CNES mesmo sem tamanho remoto previamente conhecido e sem limite artificial de tamanho, desde que restrito a uma tabela e competência específicas.

Esta etapa:
- não executa download;
- não executa extração;
- não altera dados;
- não altera código;
- não substitui scripts R;
- apenas autoriza e delimita uma futura etapa operacional.

## 2. Contexto metodológico
- A Etapa 5 anterior foi reinicializada porque partia da premissa inadequada de recorte UF antes do download.
- A Etapa 5R corrigiu a política de recorte CNES.
- A Etapa 5D passou a priorizar a descoberta operacional dos arquivos.
- A revisão pós-5D classificou a descoberta como parcialmente suficiente para uma nova 5P.
- A principal pendência era o tamanho remoto não confirmado.
- O pesquisador responsável deliberou que a ausência de tamanho remoto não deve bloquear o piloto.

## 3. Premissa corrigida
Para CNES:
- o recorte por UF não é pré-download;
- o recorte por UF=ES será aplicado após leitura temporária;
- o arquivo pode ser nacional ou amplo para uma competência;
- a segurança operacional será garantida por escopo restrito, diretório temporário, exclusão final, registro de evidências e ausência de persistência em repositório.

## 4. Decisão humana registrada
“Autoriza-se, para fins exclusivamente exploratórios e em etapa piloto, o download temporário de arquivo CNES mesmo quando o tamanho remoto não estiver previamente disponível e sem limite artificial de tamanho pré-definido, desde que:

1. o arquivo corresponda a uma tabela CNES e competência específicas;
2. o piloto inicial seja restrito à tabela tbEstabelecimento e à competência 202501;
3. o download ocorra exclusivamente em diretório temporário;
4. nenhum dado bruto ou recortado seja salvo em data_raw, data_interim ou data_processed;
5. o arquivo temporário seja excluído ao final da execução;
6. o relatório registre nome, origem, competência, tabela, caminho temporário, tamanho efetivamente baixado e confirmação de exclusão;
7. o recorte UF=ES seja aplicado apenas após a leitura temporária;
8. a etapa não aplique transformação R;
9. a etapa não aplique classificação de habilitações;
10. nenhum script R seja substituído.”

## 5. Escopo autorizado para a futura Etapa 5P
- tabela piloto: tbEstabelecimento;
- competência piloto: 202501;
- UF: ES;
- momento do filtro UF: pós-leitura temporária;
- tamanho remoto: pode ser desconhecido;
- limite artificial de tamanho: não haverá;
- diretório: tempfile;
- persistência: nenhuma;
- dados versionados: proibidos;
- habilitações: proibidas;
- classificação de habilitações: proibida;
- transformação R: proibida;
- substituição de scripts R: proibida.

## 6. Condições obrigatórias de segurança
A futura Etapa 5P deve:

1. baixar somente arquivo correspondente à tabela e competência piloto;
2. usar exclusivamente diretório temporário;
3. registrar caminho temporário;
4. registrar tamanho efetivamente baixado;
5. registrar origem/fonte;
6. registrar se o arquivo foi excluído;
7. não salvar arquivo bruto em data_raw;
8. não salvar arquivo transformado em data_interim;
9. não salvar produto final em data_processed;
10. não alterar metadados;
11. não alterar docs/cnes;
12. não alterar scripts R;
13. não aplicar classificação de habilitações.

## 7. Critérios de abortamento
A futura Etapa 5P deve abortar se:

- não conseguir identificar arquivo/fonte da tabela e competência piloto;
- houver erro de rede que impeça download;
- não houver espaço temporário suficiente;
- o arquivo baixado não puder ser lido;
- o arquivo não corresponder à tabela esperada;
- a rotina tentar escrever em diretório versionado;
- a exclusão final do arquivo temporário falhar;
- houver risco de alteração em data_raw, data_interim ou data_processed.

A ausência de tamanho remoto conhecido NÃO deve ser critério de abortamento.

## 8. Critérios de sucesso da futura Etapa 5P
Sucesso mínimo:
- arquivo de tbEstabelecimento/202501 baixado temporariamente;
- arquivo lido temporariamente;
- arquivo excluído ao final;
- colunas identificadas;
- ausência de escrita em diretórios versionados.

Sucesso forte:
- sucesso mínimo +
- filtro UF=ES aplicado pós-leitura;
- CO_UNIDADE identificado;
- CO_CNES identificado;
- evidência de preservação textual dos códigos.

Sucesso ideal:
- sucesso forte +
- comparação estrutural com contratos.py;
- relatório de campos presentes/ausentes;
- tamanho efetivamente baixado registrado;
- recomendação clara para expansão controlada.

## 9. Riscos aceitos
- tamanho remoto desconhecido;
- possibilidade de arquivo nacional por competência;
- tempo de download imprevisível;
- necessidade de leitura DBC/DBF;
- risco de falha de conversão;
- risco de divergência entre nome lógico da tabela e arquivo real;
- necessidade de exclusão rigorosa do arquivo temporário;
- impossibilidade de substituir R após um único piloto.

## 10. Riscos não aceitos
Continuam não autorizados:

- persistir dado CNES no repositório;
- gravar em data_raw;
- gravar em data_interim;
- gravar em data_processed;
- aplicar classificação de habilitações;
- portar scripts R;
- substituir R;
- expandir para 12 competências sem nova decisão;
- incluir habilitações nesta etapa;
- criar pipeline definitivo.

## 11. Implicações para a próxima etapa
A próxima etapa recomendada é:

**Nova Etapa 5P — piloto real de download/leitura temporária de tbEstabelecimento/202501 com UF pós-leitura.**

A futura 5P deve usar a deliberação deste documento como autorização humana para não bloquear por tamanho remoto desconhecido.

## 12. Critérios de aceite desta deliberação
- [x] Documento 05M criado.
- [x] Condição prévia 05R confirmada.
- [x] Condição prévia 05D confirmada.
- [x] Revisão pós-5D confirmada.
- [x] Decisão humana registrada.
- [x] Autorização de download sem tamanho conhecido registrada.
- [x] Ausência de limite artificial registrada.
- [x] Escopo da futura 5P registrado.
- [x] Proibições mantidas registradas.
- [x] Nenhum código alterado.
- [x] Nenhum dado alterado.
- [x] Nenhum metadado alterado.
- [x] Nenhum script R alterado.
- [x] Nenhum workflow alterado.

## 13. Conclusão
A deliberação humana foi registrada e a futura Etapa 5P está autorizada sob escopo estrito, com download piloto sem limite artificial de tamanho, exclusivamente para tbEstabelecimento/202501, com UF=ES filtrada pós-leitura, sem persistência em repositório e sem substituição de R.
