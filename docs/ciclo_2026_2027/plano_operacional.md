# Plano operacional — reconciliado com os dossiês em 22/10/2026

## Problema, escopo e aceite da primeira rodada

Tarefa interna autorizada pelo pedido do usuário: iniciar a continuidade do novo ciclo, preservar o relatório encerrado e entregar documentação mais um incremento verificável. Esta tarefa é o registro prévio de escopo requerido pelo fluxo do repositório. Não houve atribuição de trabalho a estudantes, decisão clínica ou mudança de norma.

O aceite desta rodada compreende inventário verificável, matriz preliminar e protocolo, plano vinculado aos seis objetivos/três planos, código R com testes e nova conferência rastreável, além de ponto de retomada. Ele não exige eliminar a divergência histórica pela alteração dos dados nem validar indicadores antes da revisão metodológica.

As [tarefas CSV](tarefas_operacionais.csv) contêm dependências, produto, critérios de aceite, evidências, responsável funcional, período da proposta, período operacional proposto e situação comprovada. P0 identifica o que bloqueia uso dos dados; P1 indica trabalho necessário ao núcleo; P2 identifica entregas posteriores/condicionais. Essa prioridade de trabalho não é pontuação de qualidade de indicador.

## Articulação dos três planos

| Plano | Responsabilidade independente | Complementaridade e limite |
|---|---|---|
| P1 — PIBIC/PIVIC: Validação metodológica de indicadores regionais da atenção especializada no âmbito do Observatório SUS-ES | Revisão bibliográfica/normativa; inventário analítico; critérios; seleção; fichas; interpretação; nota e resumo | Define regras que P2 implementa e fornece conteúdos que P3 comunica; coordenação revisa decisões metodológicas |
| P2 — PIBIT/PIVIT: Automação e documentação de fluxo reprodutível de atualização de indicadores do Observatório SUS-ES | Arquitetura; atualização/padronização; logs; dicionários; versionamento; testes; painel e manual | Não converte sucesso técnico em aprovação sanitária; implementa recortes definidos com P1 |
| P3 — PIBIC-JR/PIVIC-JR: Curadoria de dados e comunicação científica de indicadores do Observatório SUS-ES | Formação inicial; inventário documental; conferências simples supervisionadas; glossário; quadros; títulos/legendas/fontes | Não responde autonomamente por programação avançada, normas clínicas ou estatística complexa; dúvidas voltam a P1/P2/coordenação |

Os responsáveis são **papéis funcionais a designar**, não pessoas ou bolsas concedidas. A execução automatizada desta rodada é atribuída a Codex sob solicitação do usuário; não é participação discente comprovada. Os campos de estudantes 4–6, pp. 33–35 do PDF, são remanescentes não preenchidos do formulário, não planos ativos. COSEMS-RJ e IMS/UERJ são parcerias previstas; nenhuma revisão deles foi presumida ou solicitada nesta tarefa.

## Calendário e separação entre previsão e realização

| Mês do projeto | Mês civil |
|---|---|
| M1 | setembro/2026 |
| M2 | outubro/2026 |
| M3 | novembro/2026 |
| M4 | dezembro/2026 |
| M5 | janeiro/2027 |
| M6 | fevereiro/2027 |
| M7 | março/2027 |
| M8 | abril/2027 |
| M9 | maio/2027 |
| M10 | junho/2027 |
| M11 | julho/2027 |
| M12 | agosto/2027 |

O [cronograma da proposta](cronograma_proposta.csv) registra os X conferidos visualmente nas páginas 20–21, 26, 28 e 31. A orientação contínua de P2 consta também da p. 29. Trata-se do **cronograma apresentado na proposta**; o anexo, sozinho, não comprova aprovação administrativa ou concessão de bolsas.

No geral, inventário M1–M2; revisão aplicada M1–M3; critérios M2–M4; aplicação M4–M6; atualização M3–M6; padronização M3–M7; consistência M4–M8; documentação M5–M9; repositório M5–M10; painel M6–M9; nota/manual/comunicação/resumo M8–M11; consolidação e relatório M10–M12.

Os planos individuais não têm janelas idênticas. P1 mantém inventário até M3, seleciona a matriz em M5–M7 e prepara fichas em M7–M9. P2 programa painel em M7–M10, enquanto o geral indica M6–M9. P3 prepara comunicação em M7–M10 e seção formativa do relatório em M11–M12. Esses intervalos foram preservados; harmonização das entregas deverá ser documentada, não corrigida silenciosamente no PDF.

**Situação comprovada:** em M2 foram produzidos os arquivos desta rodada, a avaliação preliminar e a conferência de contrato. Não há prova local de atividades executadas em M1 por estudantes. Nenhuma atividade foi dada como concluída por sua data prevista ter passado.

**Ajuste operacional proposto:** antecipar para M2 a conferência mínima de contrato, como suporte ao inventário e à arquitetura de P2. As tarefas de consistência ampla continuam nas janelas da proposta. Recuperação do objeto LFS, correção pontual do schema e revisão das fixtures em M2–M3 são prioridades decorrentes do diagnóstico; não alteram o cronograma original nem significam atualização de bases já realizada.

## Sequência de retomada e entregas futuras

R04 → R05 → R06/R07 → R08 → R09 é o caminho proposto até um primeiro cálculo substantivo. R04 recupera e inspeciona o objeto bruto; R05 corrige a serialização do schema e alinha fixtures sem inventar chaves; R06 resolve território e R07 o recorte normativo; R08 seleciona janela comparável; R09 materializa versão separada sob escopo definido e submete-a aos três eixos de validação.

R10 depende do acesso ao MVP e à variante, que serão inventariados separadamente. R11 aproveita glossário existente e documenta comandos testados. R12 incorpora progressivamente a infraestrutura SIA/SIM, como fontes estruturantes de D1 Q7; a escolha dos indicadores da matriz mínima permanece metodológica. R13/R14 produzem comunicação, nota, resumo e relatório **apenas depois de resultados comprovados**. Não foram gerados textos finais fictícios ou nova versão do relatório encerrado.

## Atualização vinculante após incorporação de D1/D2

As seções acima preservam escopo e cronograma da primeira rodada. O estado atual e as dependências estão nas mesmas [tarefas operacionais](tarefas_operacionais.csv), agora com coluna `escopo`; não existe plano paralelo. R04/R05 concluídas; R06/R07 avançadas tecnicamente e pendentes de fontes primárias. R16–R21 explicitam manifestos, SIGTAP, população, paridade, qualidade/publicação e ética. T01–T10 detalham somente o módulo cardiovascular, reutilizando esses componentes comuns. A cópia anterior está no arquivo `referencias/estado_pre_reconciliacao.zip`.

O nome de Camila Moreira dos Santos identifica a autora do protocolo fornecido (D2 Q1), não comprova execução técnica, bolsas, horas ou participação nas rodadas automatizadas. A engenharia completa e o painel institucional não são condição de conclusão do TCC nem atribuição presumida da discente.

O caminho imediato é T01/R06/R18 (referências congeladas), R08 (cobertura por família) e R17 (SIGTAP histórico). A pendência de IAM em T02 bloqueia apenas traçadores IAM; G0–G5 podem avançar quando suas próprias fontes/regras estiverem verificadas. T03/T04 condicionam SIA/AC e recursos CNES temáticos; não bloqueiam indiscriminadamente todo o módulo. Os campos vazios de fonte/versão continuam bloqueios explícitos, sem valores fabricados.

As [21 pendências transcritas](pendencias_dossies.csv) vinculam D1 Q18/D2 Q25 a essas tarefas. Há ainda pendências operacionais do complemento, como AIH/continuidade e variante de mortalidade prematura para tendência, explicitadas no perfil e em T05/T06/T09. A [matriz de impacto](matriz_impacto_dossies.csv) e o [registro de reconciliação](reconciliacao_dossies.md) fundamentam as adequações e os limites dos recálculos.

## Avaliação de ferramentas incorporada a R08/R19

A [matriz de decisão](matriz_decisao_ferramentas.csv), a [cobertura por família](cobertura_ferramentas_por_familia.csv) e a [PoC documentada](avaliacao_ferramentas_2026-10-22.md) completam a comparação tecnológica solicitada. Não há novo plano paralelo. R19 entrega agora a serialização conservadora com PyArrow e a auditoria DuckDB, preservando preparadores R; aquisição PySUS permanece condicional por família. R08 exige esperado versus obtido e confronto com RAW oficial, sem equiparar catálogo nominal a cobertura histórica. [DataHub Brasil foi identificado pelo usuário e avaliado](avaliacao_datahub_2026-10-22.md), com código pinado e seis casos locais. Catálogo/partição mensal são referências; download Kaggle é alternativa condicionada à proveniência e paridade; adoção integral não justificada. Retrato CNES corrente, população total e macrorregião corrente não encerram R08/R18/T01; SIGTAP continua em R17. Read.dbc/healthbR permanecem alternativas, não novas dependências obrigatórias. Nenhum pipeline de aquisição ou decoder adicional foi desenvolvido; a próxima prova continua no RAW oficial por família.

Próximo incremento R08/R19: um LT/ES/202401 oficial e dois leitores, após acesso autorizado; ST/CO_UNIDADE é contrato separado. Mantêm-se T01/R06/R18 e R17 e o cronograma institucional. A PoC não autoriza aquisição ampla, uso de SIGTAB corrente como histórico, remoção de RAW/LFS antigo, troca de R ou cálculo sem denominadores/território oficiais. A aquisição desta rodada foi bloqueada pelo proxy e nenhum ajuste de rede foi feito.
