# Uma dimensão histórica da RUE foi reproduzida; o novo percurso hospitalar exige fontes validadas

Observatório SUS-ES — ciclo 2026–2027. Versão 0.1, 16/11/2026. **Rascunho técnico para revisão interna; não aprovado para divulgação institucional.** Responsabilidade institucional e revisão humana pendentes. Elaboração técnica assistida pelo Codex; autoria dos produtos históricos preservada.

Estrutura reaproveitada do template de nota técnica (Drive `1ovXyxGtf7Y5oq_mpHjrVcUc4DgRLDt4l`, SHA-256 `1731778ad314463d0de44fc883ae8c9cc44b521d2bbd8a1d8766f2ce23a1a108`) e das diretrizes de comunicação consolidadas (Drive `18qYakvWEBcfC7DM0NP4ULp38ocxuvPIK`, SHA-256 `2466fcdf9b63a67df54080630f674829bfd63cb291db256e532835abfcfcfe16`). Diretrizes formativas de Henrique e consolidação coletiva segundo o acervo Work; não se cria identidade visual oficial.

## Pergunta e mensagem principal

É possível conservar e reproduzir o conhecimento cadastral anterior enquanto se prepara uma análise nacional de utilização hospitalar dos residentes do Espírito Santo?

Uma dimensão histórica de urgência ao SUS foi reproduzida em todos os 78 municípios comparados. O novo código de custódia conserva versões e impede promoção de conjuntos parciais nos cenários testados. Esses resultados permitem continuidade técnica; não medem funcionamento, acesso efetivo ou suficiência da rede.

## 1. Escopo e fonte

O resultado RUE refere-se à competência cadastral 202601, ao campo municipal legado e a valores distintos da chave histórica `cnes`, selecionando `atende_sus=Sim` e token literal `URGENCIA`. A interpretação e a autoria antecedente estão na [ficha RUE](FICHA_RUE.md). Data da coleta primária CNES: não documentada; recuperação atual dos arquivos: 16/11/2026. Essas datas não são intercambiáveis.

O percurso SIH proposto refere-se à competência de processamento 202401, cobertura nacional RD e residentes ES. S03 conta registros elegíveis; S04 descreve atendimentos fora da região entre origens regionalizadas e destinos conhecidos. Não há resultado empírico SIH nesta nota.

## 2. Método resumido

A tabela e o script históricos RUE foram recuperados em bytes e identificados por SHA-256. Uma rotina independente em R reproduziu a dimensão e comparou cada célula. A recuperação operacional restaurou snapshot, ambiente Python mínimo e sentinela em diretório vazio. Testes sintéticos verificaram identidade multipartes, falhas, revisão de mesmo tamanho, esquema, zeros textuais, recuperação e cálculo SIH/SQL. Nenhuma linha SIH real foi simulada nos produtos empíricos.

## 3. Resultados verificáveis

| Resultado | Evidência | Alcance |
|---|---|---|
| 78/78 células RUE iguais; zero divergências | `evidencias/rue_resultado_real.csv` | Uma dimensão histórica; outras quatro sem novo ensaio |
| Sentinela real reconstruída em diretório vazio | `evidencias/restauracao_operacional_rue.json` | Ensaio pelo agente; ambiente stdlib; segundo operador pendente |
| 99 testes Python e 19 scripts R aprovados na integração registrada | `evidencias/integracao_v1/execucao.json` | Validação técnica local; não CI remoto ou validação sanitária |
| Layout, PDR e catálogo RD inacessíveis | `evidencias/acessos_oficiais.json` | CONNECT 403 do proxy; S03/S04 reais não calculados |

## 4. Interpretação

A igualdade das células demonstra reprodução da regra histórica selecionada. A restauração acrescenta uma prova operacional ao simples cotejo de bytes de um backup. Nenhuma delas resolve a localização física do cadastro, a vigência de uma habilitação ou o funcionamento do serviço. O próximo ganho científico depende de coorte e território adequados à edição SIH, não da expansão indiscriminada de infraestrutura.

## 5. Limitações

O campo `cnes` histórico não foi convertido em código público. Município gestor não foi tratado como localização física. A custódia não foi ensaiada sob queda de energia, e o transporte oficial/DBC real permanece por validar. A aritmética de uma célula oncológica foi conferida separadamente, sem reconstrução da consulta original. Dois meses de atualização ainda não foram executados; não há inferência de tendência.

## 6. Uso gerencial e próximo passo

O produto cadastral pode apoiar curadoria e formação com seu rótulo histórico. Não deve sustentar ranking de desempenho, vazio assistencial ou cobertura SAMU. Para utilização/fluxos, a prioridade é obter legitimamente layout e catálogo RD/202401, validar um arquivo e sua coorte e fechar a geografia histórica quando necessária. O painel consome resultados aprovados e não bloqueia a saída tabular.

## 7. Referências e validação

Mandato integrado v1.0; Work CP09 E025/E040/E051–E057; D1/D2 preservados; código e comandos do guia local. Conferências técnicas executadas constam das evidências. Revisão científica humana, política de pequenas células, autoria institucional final e decisão de divulgação: **pendentes**. Não houve publicação, submissão ou contato com parceiros.
