# Etapa 5N.6R — deliberação humana sobre o contrato intermediário PySUS→CNES

## 1. Objetivo
Registrar a deliberação humana posterior à criação do contrato intermediário PySUS→CNES.

Esta etapa:
- não executa PySUS;
- não baixa dados;
- não gera base;
- não transforma dados;
- não substitui R;
- apenas formaliza decisões metodológicas.

## 2. Contexto herdado da 5N.6
A Etapa 5N.6:
- criou o contrato intermediário PySUS→CNES;
- cobriu ST, LT e SR;
- criou documento, módulo declarativo, CSV e testes;
- classificou CO_UNIDADE como inconclusivo;
- classificou a etapa como **CONTRATO_INTERMEDIARIO_CRIADO_COM_RESSALVAS**.

## 3. Síntese da revisão metodológica humana
O pesquisador responsável aprovou o contrato intermediário como **contrato mínimo** e **não exaustivo**. Também autorizou o avanço apenas para **transformação em memória exploratória**, com **reforço/ampliação controlada** do contrato intermediário.

## 4. Decisões registradas

| Tema | Decisão humana | Implicação |
|---|---|---|
| Escopo mínimo do contrato | Aprovado como contrato mínimo, com ressalva de não exaustividade. | A 5N.7 pode avançar com reforço contratual, sem tratar o contrato como dicionário final completo. |
| CNES como código público | CNES permanece identificador público válido. | Pode ser utilizado como chave potencial de análise exploratória, sem assumir equivalência automática com CO_UNIDADE. |
| CO_UNIDADE inconclusivo | Equivalência com chaves finais permanece inconclusiva. | Join relacional final por CO_UNIDADE segue bloqueado até investigação específica. |
| CODUFMUN como território potencial | Pode ser equivalência territorial potencial. | Exige validação de formato e preservação textual antes de inferência relacional. |
| COMPETEN como competência | Pode ser normalizada apenas em memória. | Sem persistência nesta fase e sem alteração de bases. |
| TPGESTAO/NAT_JUR como equivalências nominais potenciais | Aceitos como potenciais equivalências nominais. | Manter texto original, sem conversão de tipo nesta etapa. |
| Campos de leitos (LT) | Entram na transformação exploratória. | Campos de quantidade permanecem numéricos apenas se PySUS já os entregar como numéricos. |
| Campos de serviços (SR) | Entram na transformação exploratória com ressalva para CNESTERC. | CNESTERC recebe tratamento de identificador textual conservador. |
| Preservação textual | Aplicar preservação textual conservadora para identificadores. | Evita perda de zeros à esquerda e distorções semânticas em códigos públicos. |
| R como oráculo | Nenhum script R será substituído agora. | Paridade deve ser avaliada em etapa comparativa posterior. |
| Sequência pós-5N.7 | Prioridades: 3 competências, CO_UNIDADE e comparação com R/oráculo. | Estrutura de continuidade metodológica para 5N.8, 5N.9 e 5N.10. |

## 5. Regras aprovadas para a 5N.7
1. A 5N.7 pode executar transformação em memória para ST/LT/SR.
2. A 5N.7 não pode salvar dados.
3. A 5N.7 não pode escrever em `data_raw`/`data_interim`/`data_processed`.
4. A 5N.7 não pode substituir R.
5. A 5N.7 deve aplicar preservação textual conservadora para:
   - CNES;
   - COD*;
   - CO_*;
   - CPF*;
   - CNPJ*;
   - COMPETEN;
   - TPGESTAO;
   - NAT_JUR;
   - CNESTERC.
6. Campos QT_* podem permanecer numéricos se o PySUS já retornar tipo numérico.
7. CNES não pode ser tratado como CO_UNIDADE.
8. Qualquer join relacional por CO_UNIDADE permanece bloqueado.
9. A transformação deve ser exploratória e em memória.
10. O contrato intermediário pode ser reforçado, mas não deve ser tratado como exaustivo.

## 6. Pendências bloqueantes
- CO_UNIDADE permanece pendência bloqueante para bases finais relacionais;
- paridade com R não foi avaliada;
- habilitações não foram resolvidas;
- o contrato intermediário ainda não é dicionário completo;
- nenhuma base pode ser gerada nesta fase.

## 7. Sequência recomendada
- **5N.7** — protótipo de transformação em memória em uma competência, com reforço contratual;
- **5N.8** — teste da transformação em memória em três competências;
- **5N.9** — investigação específica de CO_UNIDADE;
- **5N.10** — comparação com R/oráculo.

## 8. Perguntas obrigatórias

| Pergunta | Resposta | Implicação |
|---|---|---|
| 1. O contrato intermediário foi aprovado? | Sim, com ressalvas. | Pode orientar a 5N.7 como contrato mínimo. |
| 2. Ele é exaustivo? | Não. | Exige reforço controlado e impede uso como dicionário definitivo. |
| 3. CNES pode substituir CO_UNIDADE? | Não. | Proibido assumir equivalência estrutural entre as chaves. |
| 4. A ausência de CO_UNIDADE bloqueia toda transformação? | Não; bloqueia bases finais relacionais, mas permite transformação exploratória em memória. | A 5N.7 pode avançar sem persistência. |
| 5. A 5N.7 pode transformar em memória? | Sim. | Etapa autorizada no escopo exploratório. |
| 6. A 5N.7 pode salvar dados? | Não. | Sem escrita em camadas de dados do repositório. |
| 7. R pode ser substituído agora? | Não. | Scripts R permanecem referência/oráculo até comparação formal. |
| 8. Habilitações foram resolvidas? | Não. | Tema permanece pendente para etapas futuras. |
| 9. O contrato pode ser reforçado na 5N.7? | Sim. | Ampliação controlada é permitida, mantendo caráter não exaustivo. |
| 10. Qual é a próxima etapa? | 5N.7. | Próximo passo é protótipo em memória com governança contratual. |

## 9. Classificação da 5N.6R
**DELIBERACAO_HUMANA_REGISTRADA_COM_RESSALVAS.**

## 10. Conclusão
A Etapa 5N.7 está autorizada como transformação em memória exploratória, com reforço do contrato intermediário, sem persistência, sem substituição do R e sem resolver CO_UNIDADE artificialmente.
