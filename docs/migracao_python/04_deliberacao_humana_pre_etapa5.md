# Deliberação humana pré-Etapa 5 — extração mínima temporária CNES/ES/2025

## 1. Objetivo da deliberação
Este documento registra formalmente a revisão humana exigida pela revisão pós-Etapa 4 antes de qualquer avanço para a Etapa 5.

Fica explicitado que:
- a revisão humana foi realizada;
- a Etapa 5 está autorizada apenas sob escopo estrito;
- esta deliberação não executa extração;
- esta deliberação não altera código;
- esta deliberação não altera dados;
- esta deliberação não altera metadados;
- esta deliberação não substitui scripts R.

## 2. Contexto
- A Etapa 4 classificou os contratos como `CONTRATOS_DEFINIDOS_E_VALIDACAO_OPERACIONAL_PARCIAL`.
- A revisão pós-Etapa 4 aprovou avanço para Etapa 5 com revisão humana prévia.
- A revisão humana prévia agora foi concluída.
- A próxima etapa poderá ser planejada como extração mínima temporária, e não como migração plena.

## 3. Decisões humanas registradas

| Item | Decisão humana | Implicação para Etapa 5 |
|---|---|---|
| 1. Suficiência das tabelas CNES contratadas | As tabelas contratadas na Etapa 4 são suficientes para a Etapa 5. | Não é necessário ampliar contratos antes da Etapa 5. |
| 2. Ordem da Etapa 5 | Começar por estabelecimentos e só tentar habilitações se `CO_UNIDADE` e `CO_CNES` forem confirmados. | Habilitações ficam condicionadas a uma porta interna de validação. |
| 3. CO_UNIDADE | Ausência de `CO_UNIDADE` bloqueia avanço. | Se `CO_UNIDADE` não for encontrado/preservado, a Etapa 5 deve registrar falha estrutural crítica e não avançar para habilitações. |
| 4. CO_CNES | `CO_CNES` precisa ser preservado como texto. | Ausência, truncamento ou conversão indevida de `CO_CNES` deve ser tratada como falha crítica para estabelecimentos. |
| 5. Preservação textual de códigos | Aceitar conversão apenas se houver evidência de que zeros à esquerda não foram perdidos. | A Etapa 5 deve documentar evidência de preservação de zeros à esquerda para códigos críticos. |
| 6. Fallback | Fallback pode ser testado somente se PySUS falhar. | PySUS é a via principal; fallback é condicionado e deve ser justificado. |
| 7. Recorte autorizado | Permitir download temporário apenas se houver recorte por UF=ES e competência=2025 inteiro. | O ano de 2025 deve ser operacionalizado preferencialmente por competências mensais de 202501 a 202512, evitando download amplo. |
| 8. Diretório temporário | Autorizar uso de diretório temporário, desde que registre nome, tamanho, origem e exclusão no relatório. | Qualquer arquivo temporário deve ser rastreado e removido ao final. |
| 9. Escrita em dados versionados | É totalmente proibido escrever em `data_raw`, `data_interim` e `data_processed`. | Toda saída de dados deve permanecer em diretório temporário e não versionado. |
| 10. Scripts R | Pode gerar pseudocódigo comparativo, mas não código funcional de transformação. | `preparar_estabelecimentos_cnes.R`, `preparar_habilitacoes_cnes.R` e `classificar_habilitacoes_cnes.R` não podem ser portados nem substituídos. |
| 11. Classificação de habilitações | Apenas verificar se os campos necessários existem. | `metadata/cnes/classificacao_habilitacoes_cnes.csv` não deve ser aplicada na Etapa 5. |
| 12. Prioridade substantiva | Primeiro `CO_UNIDADE` e `CO_CNES`; depois identificação dos estabelecimentos e vínculo municipal; por fim habilitações e relação estabelecimento-habilitação. | A Etapa 5 deve organizar seus critérios de sucesso nessa ordem. |
| 13. Critério de sucesso | Sucesso mínimo = `tbEstabelecimento` + `tbMunicipio`; sucesso forte = incluir `rlEstabSipac`; sucesso ideal = todas as tabelas contratadas. | A Etapa 5 deve reportar resultado em três níveis: mínimo, forte e ideal. |
| 14. Diretriz geral | Aprovada. | A Etapa 5 está autorizada sob as restrições registradas. |

## 4. Competências autorizadas
O recorte temporal autorizado é o ano de 2025 inteiro, operacionalizado como:

- 202501
- 202502
- 202503
- 202504
- 202505
- 202506
- 202507
- 202508
- 202509
- 202510
- 202511
- 202512

A Etapa 5 não deve fazer download amplo do ano inteiro se isso impedir controle por competência. A execução deve ser mensal, controlada e auditável.

## 5. Porta interna de decisão da Etapa 5

Gate 1 — Estabelecimentos:
- tentar validar `tbEstabelecimento` e `tbMunicipio` para UF=ES e competências 202501–202512;
- verificar `CO_UNIDADE`;
- verificar `CO_CNES`;
- verificar preservação textual de códigos;
- verificar vínculo municipal.

Se Gate 1 for aprovado:
- habilitações poderão ser tentadas.

Se Gate 1 falhar:
- habilitações não devem ser tentadas;
- registrar falha estrutural;
- recomendar investigação de fallback.

Gate 2 — Habilitações:
- tentar validar `rlEstabSipac` e `tbSubGruposHabilitacao` apenas se Gate 1 for aprovado;
- verificar presença de `CO_UNIDADE`;
- verificar `COD_SUB_GRUPO_HABILITACAO` ou equivalente;
- verificar `TP_HABILITACAO`;
- verificar campos necessários para futura aplicação da classificação;
- não aplicar classificação de habilitações.

## 6. Política de fallback autorizada
- PySUS deve ser tentado primeiro;
- fallback só pode ser testado se PySUS falhar ou não expuser tabela necessária;
- fallback deve usar diretório temporário;
- fallback deve respeitar UF=ES e competências mensais de 2025, se tecnicamente possível;
- fallback deve registrar nome do arquivo, tamanho, origem, caminho temporário e exclusão;
- fallback não pode persistir dados no repositório;
- se não houver recorte seguro, abortar e registrar fallback necessário.

## 7. Proibições mantidas para a Etapa 5
- não escrever em `data_raw`;
- não escrever em `data_interim`;
- não escrever em `data_processed`;
- não alterar `metadata`;
- não alterar `docs/cnes`;
- não alterar scripts R;
- não alterar testes R;
- não alterar workflows;
- não aplicar classificação de habilitações;
- não portar `preparar_estabelecimentos_cnes.R`;
- não portar `preparar_habilitacoes_cnes.R`;
- não portar `classificar_habilitacoes_cnes.R`;
- não criar dashboard;
- não criar indicador final;
- não gerar base versionada.

## 8. Critérios de sucesso da Etapa 5

Sucesso mínimo:
- `tbEstabelecimento` e `tbMunicipio` acessadas ou extraídas temporariamente;
- `CO_UNIDADE` presente e preservado;
- `CO_CNES` presente e preservado como texto;
- vínculo territorial minimamente verificável.

Sucesso forte:
- sucesso mínimo +
- `rlEstabSipac` acessada ou extraída temporariamente;
- `CO_UNIDADE` presente em habilitações;
- campos de habilitação necessários identificados.

Sucesso ideal:
- sucesso forte +
- todas as tabelas contratadas validadas estruturalmente;
- campos críticos conferidos;
- fallback definido para ausências;
- relatório de cobertura completo.

Falha crítica:
- ausência de `CO_UNIDADE`;
- ausência crítica de `CO_CNES` em estabelecimentos;
- perda irreversível de zeros à esquerda em códigos críticos;
- impossibilidade de recorte seguro;
- tentativa de escrita em diretórios versionados.

## 9. Implicações para o prompt da Etapa 5
O prompt da Etapa 5 deve:
- usar Python 3.12;
- usar PySUS 2.x;
- usar UF=ES;
- usar competências 202501–202512;
- usar diretório temporário;
- gerar relatório;
- comparar colunas encontradas com `contratos.py`;
- registrar arquivos temporários, tamanhos, origem e exclusão;
- não gravar dados no repositório;
- não substituir R;
- não aplicar transformação sensível.

## 10. Decisão final
A revisão humana pré-Etapa 5 foi realizada e a Etapa 5 está autorizada, desde que:
- comece por estabelecimentos;
- condicione habilitações à confirmação de `CO_UNIDADE` e `CO_CNES`;
- use recorte UF=ES e competências mensais de 2025;
- utilize somente diretório temporário;
- não escreva dados versionados;
- não substitua scripts R;
- não aplique classificação de habilitações.
