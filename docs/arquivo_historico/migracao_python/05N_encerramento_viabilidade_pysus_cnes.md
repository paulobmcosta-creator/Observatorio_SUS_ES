# Etapa 5N — encerramento da prova de viabilidade PySUS/CNES

## 1. Objetivo do documento

Este documento encerra a Etapa 5N como prova de viabilidade técnico-metodológica do uso de Python/PySUS para o caminho CNES. O encerramento consolida os achados, as decisões, os limites, as pendências e os critérios mínimos que devem orientar uma eventual Etapa 6 de consolidação estratégica da migração controlada CNES R–Python/PySUS.

Este documento também delimita explicitamente o que a Etapa 5N não autoriza:

* não é etapa de extração histórica;
* não é etapa de geração de base;
* não é etapa de substituição do R;
* não é validação final de paridade;
* não resolve CO_UNIDADE;
* não libera escrita em data_interim.

## 2. Pergunta orientadora da Etapa 5

A Etapa 5 buscou responder à seguinte pergunta orientadora:

> “É tecnicamente e metodologicamente viável iniciar a migração controlada do caminho CNES do R para Python/PySUS, sem gerar base final, sem perder chaves/códigos e sem substituir prematuramente o R?”

A resposta consolidada ao fim da etapa é positiva apenas com ressalvas: há viabilidade para acesso, mapeamento estrutural e construção de contrato intermediário, mas ainda não há autorização metodológica para geração de base materializada, substituição de scripts R ou uso relacional final enquanto CO_UNIDADE permanecer não resolvido.

## 3. Linha do tempo sintética da Etapa 5N

| Subetapa | Produto principal | Resultado | Classificação/Decisão |
| -------- | ----------------- | --------- | --------------------- |
| 5N | Reinício do caminho CNES Python com API PySUS funcional | Identificação de `from pysus import cnes` como forma operacional de acesso | ACESSO_PYSUS_CNES_APROVADO_COM_RESSALVAS |
| 5N.1 | Isolamento PySUS/DuckDB no contexto CNES | Separação do problema de acesso PySUS de interferências do ambiente DuckDB | DIAGNOSTICO_AMBIENTAL_CONCLUIDO |
| 5N.2 | Diagnóstico pós-isolamento de falha CNES | Caracterização de falhas após isolamento e delimitação do escopo de investigação | DIAGNOSTICO_OPERACIONAL_CONCLUIDO |
| 5N.3 | Inventário inicial de grupos CNES no PySUS | Identificação de ST, LT e SR como grupos operacionais iniciais | GRUPOS_ST_LT_SR_IDENTIFICADOS |
| 5N.3R | Reteste controlado de ST | Confirmação de que ST exigia observação adicional e não deveria ser descartado prematuramente | ST_MANTIDO_EM_INVESTIGACAO |
| 5N.4 | Mapeamento estrutural dos grupos CNES/PySUS | ST, LT e SR retornaram DataFrame em etapa de mapeamento | MAPEAMENTO_ST_LT_SR_APROVADO |
| Revisão corretiva da 5N.4 | Ajuste interpretativo do mapeamento estrutural | Prevenção de leitura excessiva dos resultados estruturais | INTERPRETACAO_CORRIGIDA |
| 5N.5 | Mapeamento multi-competência CNES/PySUS | Estabilidade estrutural observada em competências-piloto de 2024 | ESTABILIDADE_ESTRUTURAL_APROVADA_COM_RESSALVAS |
| 5N.6 | Contrato intermediário PySUS→CNES | Criação de contrato intermediário para preservar campos, códigos e equivalências | CONTRATO_INTERMEDIARIO_APROVADO_COM_RESSALVAS |
| 5N.6R | Deliberação humana sobre contrato intermediário | Registro de decisão humana mantendo cautela metodológica | DELIBERACAO_HUMANA_REGISTRADA |
| 5N.7-8 | Transformação multi-competência em memória | Protótipo diagnóstico de transformação em memória sem persistência de dados | TRANSFORMACAO_MEMORIA_PARCIAL |
| 5N.7-8A | Validação mínima da transformação em memória | Validação parcial sem autorização de base final | VALIDACAO_MINIMA_PARCIAL |
| 5N.7-8D | Diagnóstico de timeout na transformação em memória | Identificação de limitações operacionais no caminho com subprocesso | DIAGNOSTICO_TIMEOUT_CONCLUIDO |
| 5N.7-8E | Correção do caminho padrão da transformação em memória | Caminho direto sem subprocesso definido como padrão diagnóstico | CAMINHO_DIRETO_APROVADO_COM_RESSALVAS |
| 5N.7-8F | Diagnóstico específico de ST na transformação em memória | ST apresentou comportamento instável/intermitente | ST_INSTAVEL_INTERMITENTE |
| 5N.7-8G | Diagnóstico de acesso ST PySUS/CNES | Reforço da necessidade de tratamento específico para ST | ST_BLOQUEIO_OPERACIONAL_PENDENTE |

## 4. Achados consolidados

1. A API funcional é `from pysus import cnes`.
2. Os grupos operacionais iniciais são ST, LT e SR.
3. ST, LT e SR retornaram DataFrame em etapas de mapeamento.
4. Houve estabilidade estrutural em competências-piloto.
5. Foi criado contrato intermediário PySUS→CNES.
6. Foi criada deliberação humana sobre o contrato.
7. A transformação em memória é viável parcialmente.
8. LT e SR transformam em memória no caminho direto.
9. ST apresenta instabilidade/intermitência.
10. CO_UNIDADE permanece não resolvido.
11. R permanece oráculo metodológico.

## 5. Estado final por componente

| Componente | Estado final | Implicação |
| ---------- | ------------ | ---------- |
| Acesso PySUS/CNES | APROVADO_COM_RESSALVAS | O acesso pode continuar sendo investigado em Python/PySUS, desde que sem materialização de base e com rastreabilidade metodológica. |
| Grupos ST/LT/SR | APROVADO | ST, LT e SR ficam reconhecidos como grupos operacionais iniciais para investigação controlada. |
| Mapeamento estrutural | APROVADO | A etapa demonstrou capacidade de inventariar estruturas retornadas por PySUS. |
| Estabilidade multi-competência | APROVADO_COM_RESSALVAS | Competências-piloto indicaram estabilidade estrutural, mas não equivalem a validação histórica 2008–2024. |
| Contrato intermediário | APROVADO_COM_RESSALVAS | O contrato pode orientar análises futuras, mas ainda depende de revisão, paridade com R e decisão sobre campos críticos. |
| Transformação em memória | PARCIAL | Há viabilidade exploratória, especialmente para LT/SR, mas sem validação plena e sem persistência. |
| ST | BLOQUEADO | O comportamento instável/intermitente exige estratégia própria antes de qualquer avanço materializado. |
| LT | APROVADO_COM_RESSALVAS | Pode seguir em transformação exploratória em memória, sem autorização de base final. |
| SR | APROVADO_COM_RESSALVAS | Pode seguir em transformação exploratória em memória, sem autorização de base final. |
| CO_UNIDADE | PENDENTE | Permanece bloqueante para bases finais relacionais e para joins que dependam de chave operacional correta. |
| R/oráculo | APROVADO | R permanece como referência metodológica obrigatória para comparação e validação. |
| Persistência de dados | NAO_AUTORIZADO | Nenhum dado deve ser escrito em data_raw, data_interim ou data_processed nesta fase. |
| Geração de base | NAO_AUTORIZADO | Nenhuma base intermediária ou final pode ser gerada ao término da Etapa 5. |

## 6. Decisões metodológicas consolidadas

1. Python/PySUS é viável para acesso e mapeamento estrutural inicial do CNES.
2. Python/PySUS pode continuar em investigação para transformação em memória.
3. LT e SR podem ser considerados transformáveis em memória em caráter exploratório.
4. ST requer tratamento específico por instabilidade/intermitência.
5. CNES não pode ser tratado como CO_UNIDADE.
6. CO_UNIDADE permanece bloqueante para bases finais relacionais.
7. Nenhum script R pode ser substituído agora.
8. Nenhuma base pode ser gerada agora.
9. Nenhum dado deve ser escrito em data_raw, data_interim ou data_processed nesta fase.
10. A comparação com R/oráculo permanece obrigatória antes de qualquer depreciação.

## 7. Limites da Etapa 5

A Etapa 5 não resolveu:

* extração histórica 2008–2024;
* geração de base intermediária;
* base final de estabelecimentos;
* base final de habilitações;
* CO_UNIDADE;
* joins relacionais;
* paridade com R;
* estabilidade operacional plena de ST;
* classificação de habilitações;
* substituição de scripts R.

## 8. Riscos remanescentes

| Risco | Severidade | Tratamento recomendado |
| ----- | ---------- | ---------------------- |
| Instabilidade de ST | Alta | Definir estratégia específica para ST antes de qualquer materialização ou comparação ampla. |
| Ausência de CO_UNIDADE | Crítica | Manter bloqueio de bases relacionais até decisão metodológica documentada e validada. |
| Equivalências ainda intermediárias | Alta | Revisar o contrato intermediário contra o R/oráculo e contra documentação de referência antes de uso final. |
| Coerção de códigos | Alta | Preservar códigos como texto, auditar perdas de zeros à esquerda e documentar transformações de tipo. |
| Dependência de PySUS/DATASUS | Média | Registrar versões, comportamento operacional e eventuais indisponibilidades antes de ampliar escopo. |
| Risco de assumir CNES como chave operacional | Crítica | Proibir o uso de CNES como substituto de CO_UNIDADE sem deliberação metodológica explícita. |
| Ausência de comparação com R | Crítica | Exigir testes de paridade com o R antes de qualquer substituição ou geração de base final. |
| Tentação de gerar base antes da paridade | Crítica | Manter geração de base como não autorizada até que critérios bloqueantes sejam superados. |

## 9. Critérios que bloqueiam geração de base

Fica proibido gerar base materializada enquanto não houver:

* decisão sobre CO_UNIDADE;
* comparação com R/oráculo;
* validação dos campos críticos;
* preservação textual auditada;
* validação de ST ou estratégia alternativa para ST;
* decisão documentada sobre escopo de dados que pode ser materializado;
* revisão humana posterior.

## 10. Classificação final da Etapa 5

Classificação final:

**ETAPA_5_CONCLUIDA_COM_RESSALVAS**

Substatus:

* ACESSO_PYSUS_CNES_APROVADO_COM_RESSALVAS;
* MAPEAMENTO_ST_LT_SR_APROVADO;
* CONTRATO_INTERMEDIARIO_APROVADO_COM_RESSALVAS;
* TRANSFORMACAO_MEMORIA_PARCIAL;
* ST_INSTAVEL_INTERMITENTE;
* CO_UNIDADE_NAO_RESOLVIDO;
* R_MANTIDO_COMO_ORACULO;
* GERACAO_DE_BASE_NAO_AUTORIZADA.

## 11. Recomendação para Etapa 6

Nome sugerido:

**Etapa 6 — consolidação da estratégia de migração controlada CNES R–Python/PySUS**

Objetivo sugerido:

Definir o que permanece em R, o que pode avançar em Python, o que fica bloqueado por CO_UNIDADE, como tratar ST instável, quais comparações com R serão obrigatórias e em que condições poderá haver primeira materialização controlada.

A Etapa 6 deve decidir:

* o papel do Python no acesso/mapeamento;
* o papel do Python na transformação em memória;
* o papel do R como oráculo;
* se ST exige estratégia especial;
* se LT/SR podem seguir em transformação exploratória;
* como tratar CO_UNIDADE;
* quando, se algum dia, permitir data_interim;
* quais testes de paridade serão exigidos.

## 12. O que não deve ser feito imediatamente

Não deve ser feito imediatamente:

* não continuar abrindo subetapas 5N.7-8H/I/J;
* não insistir em depuração operacional infinita na Etapa 5;
* não rodar 2008–2024;
* não gerar data_interim;
* não substituir scripts R;
* não criar CO_UNIDADE artificial;
* não fazer join relacional;
* não tratar CNES como CO_UNIDADE.

## 13. Checklist de encerramento

* [ ] API PySUS identificada.
* [ ] Grupos ST/LT/SR identificados.
* [ ] Mapeamento estrutural executado.
* [ ] Mapeamento multi-competência executado.
* [ ] Contrato intermediário criado.
* [ ] Deliberação humana registrada.
* [ ] Transformação em memória testada parcialmente.
* [ ] ST classificado como instável/intermitente.
* [ ] CO_UNIDADE mantido como pendência.
* [ ] R mantido como oráculo.
* [ ] Geração de base não autorizada.
* [ ] Etapa 6 recomendada.

## 14. Conclusão

A Etapa 5 demonstrou viabilidade técnico-metodológica do uso de Python/PySUS para acesso, mapeamento e contrato intermediário do CNES, mas não autorizou geração de base nem substituição do R.

“A Etapa 5 deve ser encerrada como concluída com ressalvas. Ela demonstrou viabilidade de uso do PySUS para acesso e mapeamento estrutural do CNES, confirmou ST/LT/SR como grupos operacionais iniciais e permitiu construir um contrato intermediário PySUS→CNES. Contudo, a transformação em memória permanece parcialmente validada, com funcionamento para LT/SR e instabilidade operacional em ST. CO_UNIDADE continua não resolvido e bloqueia bases finais relacionais. O R permanece oráculo metodológico. A continuidade deve ocorrer na Etapa 6, como consolidação estratégica da migração controlada, e não como nova depuração incremental da Etapa 5.”
