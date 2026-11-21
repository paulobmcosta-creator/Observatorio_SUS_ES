# Capacidade cadastrada e produção ambulatorial observada

**CNES · Limitação metodológica caracterizada.** B06 e T15 descrevem estoques na competência cadastral. T23 distingue média dos meses válidos, cobertura em meses, média anual de 12 competências e estoque de dezembro. A densidade usa a população do território do estabelecimento. Os 132 esquemas mensais ST examinados documentam cadastro e atributos administrativos. Seus campos não estabelecem abertura diária, escala efetivamente cumprida, disponibilidade de agenda ou realização de um atendimento.

| Conceito | Regra e unidade | Produto |
|---|---|---|
| Estabelecimento cadastrado | CNES distinto registrado na competência | ST_CAD |
| Estabelecimento com vínculo SUS | CNES distinto com VINC_SUS=1 | ST_SUS |
| Serviço, habilitação ou recurso cadastrado | Campo e código do catálogo histórico na competência válida. Um mesmo estabelecimento pode ter mais de uma habilitação. | B06, T05, T15, T17–T19, T23 e M02 |
| Equipe ativa no cadastro | Critério administrativo de vigência da equipe no fim da competência. “Ativa” qualifica a equipe e sua situação cadastral. | EP_ATIVAS e F17 |
| Estabelecimento com produção observada | CNES distinto com quantidade aprovada positiva para os códigos selecionados no território e período. | F23, SIA/PA |
| Funcionamento operacional efetivo | Comprovação de abertura, operação, disponibilidade ou continuidade requer fonte operacional específica. | Sem medida validada |

Códigos profissionais contam vínculos ou horas cadastradas. Leitos previstos para o SUS identificam destinação cadastrada. T23 apresenta cada unidade segundo o ID. A eventual ausência de produção específica de um estabelecimento admite outras atividades assistenciais fora do recorte.

**SIA/PA · Limitação metodológica caracterizada.** PA_QTDPRO é a quantidade apresentada para processamento. PA_QTDAPR é a quantidade aprovada registrada após o processamento. São campos do mesmo universo elegível e podem divergir. T21 discrimina ambos por código. T22 separa modalidades e indicadores contextuais. A quantidade aprovada pode incluir procedimentos repetidos em uma mesma pessoa.

PA_CMP identifica a competência de produção. PA_MVM identifica a competência de movimento, na qual o registro entrou no processamento observado. O estudo reúne movimentos de janeiro de 2014 a dezembro de 2024. No controle de qualidade há registros elegíveis com movimento posterior à competência de produção. Essa observação confirma que as duas datas podem divergir. Produções do fim de 2024 que entraram em movimentos posteriores ao encerramento ficam fora da janela. A quantidade faltante é desconhecida. A falta de linha elegível só admite zero no universo e na janela cuja integridade foi demonstrada.

A densidade de produção localizada por 100 mil usa a quantidade aprovada pelo **local do estabelecimento** no numerador e a população residente nesse território no denominador. Pode haver pacientes de fora. A medida descreve intensidade de produção territorial. Acesso individual, cobertura da população e motivo clínico da consulta exigem dados adicionais.

**Instrumentos e cobertura clínica.** O leitor confere PA_DOCORIG contra o instrumento vigente no SIGTAP de PA_CMP. O recorte elegível observado apresenta C (BPA consolidado, instrumento 01), I (BPA individualizado, 02), P (APAC principal, 06) e S (APAC secundária, 07). O leitor também reconhece A/08 e B/09, sem ocorrências elegíveis desses tipos no recorte verificado. A compatibilidade no SIGTAP e a presença em PA são perguntas distintas.

Cada um dos 11 códigos cardiovasculares específicos homologados tem ao menos uma competência válida e produção aprovada observada em PA. Portanto, nenhum dos 11 se mostrou integralmente dependente de um instrumento ausente do PA processado. O cateterismo cardíaco 0211020010 foi observado em P. O ECG 0211020036 teve registros C, I e S. A fisioterapia na síndrome coronariana aguda 0302040064 teve 37 competências válidas, de dezembro de 2021 a dezembro de 2024. Os meses anteriores guardam a ausência de vigência. Para quantificar produção registrada exclusivamente em outro instrumento ou sistema em um mês específico, seria necessário consultar a fonte correspondente. A conclusão aqui se restringe aos códigos, eventos e instrumentos observados.

As duas cintilografias de perfusão permanecem separadas. Doppler vascular e consultas especializadas com CBO 225120, 225210 ou 225203 compatível no mês são séries contextuais, fora do total específico. AC, fisioterapia vascular periférica e reabilitação pós-COVID conservam recortes próprios sob revisão clínica.

**T29.** Nos 11 anos do comparador residual, 27 colunas de CNES e PA ficam vazias intencionalmente, totalizando 297 células. Índices de prestadores exigem localização conhecida. Os 297 valores estão na linha correspondente do comparador estrito. Essa regra geográfica difere da falta de vigência de um código e da ausência de registro elegível.
