# Plano operacional integral — revisão de 22/10/2026

Este é o planejamento vigente para O1–O6, atualizado sobre as rodadas anteriores. Não substitui o projeto, D1, D2 ou o relatório encerrado. **A execução desta rodada termina na entrega à segunda revisão no ChatGPT com o coordenador (REV01).** O plano abaixo é proposta de execução posterior; aquisição ampla, migração, recálculo em massa, implantação do painel e divulgação de resultados não foram realizados.

A fonte operacional única é [tarefas_operacionais.csv](tarefas_operacionais.csv), agora com **49 tarefas**. IDs anteriores R01–R21 e T01–T10 foram preservados; R22–R38 detalham correções e frentes antes insuficientes; REV01 marca a revisão requerida. Os IDs T01–T10 deste plano designam tarefas cardiovasculares; T01–T06 da matriz de indicadores designam controles técnicos, em domínio distinto. [Inventário](inventario_transicao.csv) registra decisões por 25 produtos/componentes; [matriz](matriz_indicadores_preliminar.csv) e [avaliação](avaliacao_preliminar.csv) registram os candidatos. Não há plano temático paralelo substituindo a agenda institucional.

## Objetivos, entregas e critérios de conclusão

| Objetivo / produto exigido | Situação comprovada e lacuna | Decisão e tarefas | Dependências específicas | Critério de conclusão | Responsabilidade / janela proposta |
|---|---|---|---|---|---|
| O1 — inventário crítico dos produtos anteriores | Acervo local e fontes fornecidas inspecionados; relatório/MVP/produtos externos não reinspecionados | Atualizar decisões sem declarar inexistência; R01, R10, R26, R28, R37 | Pacote documental de cada produto; acesso independente por frente | Cada produto identificado por versão, autoria, fonte, cálculo, unidade, limites e aproveitamento; materiais faltantes explicitados | P1/P2; P3 curadoria supervisionada; M2–M3, conclusão externa condicionada |
| O2 — matriz mínima e fichas validadas | 6 controles técnicos, propostas substantivas e derivados técnicos; validação sanitária incompleta | Propor S03/S04 primeiro, S01 quando norma/localização prontas; R02, R07, R20, R24, R31 e tarefas temáticas | Ficha específica, norma/layout, coorte real, qualidade e interpretação | Evidência documental, cálculo reproduzido e interpretação analítica para cada indicador selecionado; rejeições/reformulações registradas | P1 e coordenação, P2 prova operacional; M2–M4 seleção preliminar, M4–M7 validação; fichas finais M7–M9 |
| O3 — bases atualizadas, recortes, extrações e dicionários | Recuperação CNES202601 e serialização verificadas; não equivalem a atualização de séries | R08/R09/R12/R16/R17/R18/R23/R25/R30/R32; expansão por pergunta | RAW oficial por família, layout, cobertura; população apenas para taxas; relações normativas apenas para filtros que as usam | Fonte/horário/hash/versão, esperado versus obtido, campos/chaves/perdas; segundo período reproduzível; dicionário original→tratado | P2, P1 regras, P3 conferências simples; M3–M6 atualização inicial, M3–M7 padronização |
| O4 — fluxo, conferência, versionamento, ambiente e manual | Contratos, cache, R e Arrow testados; proveniência temporal fixa e localização exigem ajuste | Reutilizar componentes; R11/R16/R19/R22/R23/R25/R36 | Correção pequena antes de outra competência; fonte e contrato da execução; ambiente da ferramenta | Outra pessoa reproduz uma atualização e restaura a versão anterior; hashes e logs conferem; documentação não depende da memória do autor | P2, revisão P1; M3 correções, M4–M8 consistência, M5–M10 documentação/repositório, M8–M11 manual |
| O5 — painel-piloto qualificado | MVP principal e v2 externos; não examinados; nenhuma base para escolher uma reescrita | R10 inspeciona; R33 requisitos; R34 adapta; R35 valida; R36 atualiza/mantém | Requisitos avançam sem acervo; adaptação exige comparação das versões e produto analítico aprovado | Filtros/cartões/mapas reconciliados às tabelas; fonte/período/unidade/limites visíveis; usabilidade e atualização/rollback registrados | P2, P1 coerência, P3 comunicação; M3–M4 requisitos; M6–M9 geral, M7–M10 P2 |
| O6 — nota, manual/guia, resumo, apresentações/divulgação e novo relatório | Guias locais reutilizáveis; modelos externos pendentes; não há novos resultados sanitários | R11/R13/R14/R37; artigos e cooperação R38 como agenda condicionada | Estrutura pode começar sem resultados; redação de achados depende de análise revisada, autoria e enquadramento | Artefatos versionados ligados a fichas/resultados; revisão real registrada; relatório exclusivo 2026–2027, sem editar 2025–2026 | P1 conteúdo, P2 reprodução, P3 comunicação supervisionada; M7–M11 produtos, M10–M12 consolidação |

O projeto (PDF pp. 8, 13–15) exige nota técnica, manual/guia, resumo, materiais e relatório; **não determina automaticamente três notas gerenciais**, meta citada na agenda anterior. A quantidade final de indicadores é resultado da seleção, não uma quota de seis nem a extensão do TCC.

## Agenda herdada e extensões

| Frente | Encaminhamento e resultado esperado | Ordem e limites |
|---|---|---|
| CNES habilitações/serviços | R07 e R23 qualificam S01; R32 amplia LT/EQ/SR; R22 corrige metadado antes de novo mês | 501 registros selecionados não são 501 estabelecimentos; 304 com status interno não são homologações normativas; gestor não é localização física |
| Atualização CNES | R08/R22/R25 demonstram parâmetros, fonte e diferença entre competências; ensaio de oferta por família | O snapshot 202601 é referência técnica, não prioridade universal ou prova de 2014–2024; não somar estoques mensais |
| Oncologia | R26 reconstitui uma tabela herdada e sua definição; R27 amplia oferta por estabelecimento/habilitação/equipamento e produção/fluxos | Preservar denominador e interpretação históricos; mudanças para população total geram nova versão e comparação. Período/coorte definidos após inspeção |
| Cardiovascular | T01–T10 preservam D2 e compartilham fontes, território e engenharia | 2014–2024, quatro regiões e focal Noroeste 1 no escopo D2; padrões e tendência não impostos a todo Observatório; IAM pendente não bloqueia G0–G5 |
| RUE | R28 separa relatório individual e análise municipal final; R29 amplia produção/fluxos | Script municipal não é a trilha PySUS; novo manifesto não prova execução antiga. Distância/tempo, regulação e funcionamento exigem fontes próprias e são aprofundamentos condicionais |
| Força de trabalho | R30 desdobra S09 em pessoas, vínculos e horas; PF e CBO por competência | Sem identificador individual válido não se publica pessoas distintas; recalcular distinct em cada escala; horas cadastradas não provam trabalho efetivo |
| ICSAP | R31 valida lista, residência, AIH e população; S10 é complementar da rede | Contextualiza interface APS-hospital e não desempenho isolado da especializada; proporção e taxa exigem fichas diferentes |
| Painel | R10/R33–R36 cobrem inspeção, escolha, adaptação, validação, atualização e manutenção | Não redesenhar antes de examinar o MVP; v2 não homologada por nome; requisitos independem de todas as bases prontas |
| Comunicação | R37 reaproveita diretrizes/modelo; R13 produz nota/resumo/materiais; R11 manual; R14 relatório novo | Preparar estrutura sem achados fictícios; linguagem e utilidade precisam de avaliação real |
| Artigos e cooperação | R38 registra manuscritos, autoria, revisão, submissão e eventual uso institucional em estados separados | Preparação depende de maturidade; aceite/adoção não são garantidos. Nenhuma mensagem a parceiros ou submissão nesta rodada |

## Núcleo proposto e sequência de expansão

1. **Primeiro percurso S03/S04:** utilização hospitalar e destinos dos residentes ES, uma competência SIH/RD com cobertura nacional. Não depende de CO_UNIDADE, whitelist clínica, população ou padrão 2010. Exige contrato AIH, cobertura de destinos, semântica temporal e regionalização adequada. A [especificação](primeiro_percurso_analitico.md) compara as alternativas e define critérios antes da execução.
2. **Oferta S01 em paralelo quando elegível:** estabelecimentos com habilitação de uma linha de cuidado, com localização física e vigência comprovadas. Reaproveitar o derivado técnico sem promover município gestor a oferta. S02 fica como controle complementar de registros.
3. **Expansão justificada:** capacidade LT/EQ/SR, trabalho PF, produção SIA e módulos herdados; ICSAP e mortalidade entram por pergunta e maturidade. As famílias não são automaticamente aprovadas em bloco. O módulo cardiovascular mantém seus indicadores centrais próprios conforme D2.
4. **Painel e comunicação:** trabalhar requisitos, glossário e estrutura do manual em paralelo; integrar apenas produtos cujas condições de uso estejam documentadas. A análise não espera o painel para existir.

## Marcos verificáveis e portas de avanço

| Marco | Produto verificável | Evidência para concluir | Janela operacional proposta |
|---|---|---|---|
| K1 — acervo e decisões | Inventário atualizado, parecer e decisões da segunda revisão | 25 linhas de inventário com lacunas explícitas; anexos faltantes recebidos por frente; REV01 registrada | M2–M3; parte local entregue, revisão/acervo pendentes |
| K2 — referências suficientes | Ficha SIH, tabela territorial, regra AIH e qualidade do primeiro uso; requisitos do painel/manual | Layout e fontes identificados; regras sem ambiguidades; itens necessários completos; sem esperar SIGTAP/população para uma proporção hospitalar | M3–M4 |
| K3 — primeiro percurso real | Tabelas S03/S04, matriz origem-destino, ficha e interpretação | Cobertura27UF; conciliação de perdas/destinos; cálculo independente; revisão analítica | M4–M5, condicionado a K2 |
| K4 — atualização | Segundo mês 202402 e comparação com 202401 | Mesmos contratos ou mudança explicada; revisão separada de mudança assistencial; reprodução/recuperação verificadas | M5–M6 |
| K5 — expansão | Indicadores/módulos escolhidos com fichas e produtos próprios | Evidência por família, norma, estrato e período; não extrapolar o sucesso de uma família | M5–M8; aprofundamentos M8–M10 se viáveis |
| K6 — painel | MVP qualificado e atualização demonstrada | Comparação com tabelas, filtros/mapas, usabilidade, versão/fonte e rollback | M6–M10, articulando geral e P2 |
| K7 — consolidação | Manual, nota, resumo, materiais, relatório 2026–2027 e continuidade | Reprodução por leitor distinto; autoria/revisão reais; catálogo de entregas e pendências | M8–M12 |

Uma dependência na tabela de tarefas significa **a parte do produto necessária à tarefa consumidora**, não a conclusão de todas as linhas de um sistema. Por exemplo, R06 precisa estar suficiente para o território do primeiro percurso; não precisa resolver todas as malhas nacionais. R08 deve fechar RD/202401 para R09, não todas as famílias CNES e todos os anos. A triagem do acervo é incremental: Oncologia não espera todos os arquivos RUE para começar sua própria revisão.

O caminho antigo R04→R05→R06/R07→R08→R09 misturava recuperação histórica com dependências universais. R04/R05 estão tecnicamente concluídas. R07 não bloqueia SIH todas as causas. R18 é necessário a taxas, não a S04; sua aquisição municipal pode avançar antes de completar agregação regional. LT/ES/202401 deixa de ser requisito geral e permanece ensaio pontual em R32. Não fabricar chaves para adaptar uma biblioteca a uma finalidade que não as exige.

## Três planos formativos e responsabilidade

| Plano | Contribuição própria e verificável | Complementaridade |
|---|---|---|
| P1 — PIBIC/PIVIC, validação metodológica de indicadores regionais | Revisão aplicada, critérios, fichas, seleção e interpretação; conteúdo da nota e resumo | Define regras com coordenação e confere resultados produzidos com P2; oferece conteúdo verificável a P3 |
| P2 — PIBIT/PIVIT, automação e documentação da atualização | Contratos, aquisição/cache, conversão, atualização, conferências, versionamento, painel e manual | Implementa as regras de P1; fornece bases e rastreabilidade para P3; não transforma CI verde em validade sanitária |
| P3 — PIBIC-JR/PIVIC-JR, curadoria e comunicação | Inventário, glossário, conferências simples supervisionadas, títulos/legendas/fontes, materiais e seção formativa | Registra dúvidas para P1/P2; não assume decisão normativa, programação avançada ou estatística complexa |

São responsáveis funcionais a designar. Não se inferem bolsas, horas, estudantes em atividade, reuniões ou participação de COSEMS-RJ/IMS-UERJ. O TCC cardiovascular não substitui P1 nem transfere toda a engenharia à discente. Os campos4–6 do formulário do projeto não constituem planos formativos ativos adicionais.

## Calendário original, ajustes e capacidade

M1=set/2026; M2=out; M3=nov; M4=dez; M5=jan/2027; M6=fev; M7=mar; M8=abr; M9=mai; M10=jun; M11=jul; M12=ago. O [cronograma original](cronograma_proposta.csv) permanece inalterado, com suas páginas e marcações conferidas na primeira rodada. Datas previstas não comprovam execução discente ou aprovação administrativa.

A preparação de requisitos do painel, molde de comunicação e estrutura do manual é proposta para M3–M4; a integração e os produtos finais mantêm as janelas gerais. O projeto geral situa painel em M6–M9, P2 em M7–M10: propõe-se requisitos antes, incremento em M7–M9 e atualização/aceite em M10. P1 seleciona matriz em M5–M7 e fecha fichas em M7–M9; a ficha provisória do primeiro percurso permite testar definições em M4–M5 sem fingir homologação antecipada. P3 prepara comunicação em M7–M10; produtos O6 em M8–M11 e relatório em M10–M12.

A capacidade nominal/efetiva da equipe não foi comprovada. Portanto, não é defensável prometer simultaneamente reconstrução de todos os módulos, toda a série 2014–2024, revisão do painel e todos os aprofundamentos até M12. O encadeamento acima requer P1/P2/P3 em funções complementares e acesso em M3. A carga cresce sobretudo com famílias/competências, revisão normativa e disponibilidade dos artefatos externos, não com o número de scripts.

**Opções para decisão em REV01/R15:**

- **A — foco nos compromissos O1–O6 (recomendada):** núcleo S03/S04 e S01 condicionado; uma atualização demonstrada; painel e produtos de comunicação; todas as frentes com inventário e especificação, expansão empírica por maturidade. O TCC conserva D2 e avança em trilha temática, sem prometer toda sua série antes dos insumos.
- **B — módulos em paralelo:** mesma base comum, com execução empírica adicional de Oncologia/RUE/trabalho/ICSAP e D2. Só pactuar cronograma após comprovar capacidade funcional e acesso; não supor horas disponíveis.
- **C — acesso externo atrasado:** concluir revisão documental, contratos e preparações independentes, receber arquivos oficiais por meio autorizado e reprogramar K3–K6 se necessário. Não declarar O1/O3/O5 concluídos por falta de material nem substituir dados reais por fixtures.

Se K2 não estiver suficiente até M4, o marco de análise e as entregas dependentes devem ser renegociados de modo explícito. Se a primeira atualização não for demonstrada até M6, priorizar correção/reprodutibilidade e reduzir aprofundamentos opcionais, preservando os objetivos contratuais. Nenhuma dessas opções aprova automaticamente exclusão de uma obrigação do projeto.

## Estado para a segunda revisão

Concluídos nesta rodada: revisão local, testes diagnósticos mínimos, conferência de CI/pins, inventário vigente, decisões qualitativas, especificação do primeiro percurso e planejamento integral. Dependências externas e decisões abertas estão no [parecer](parecer_revisao_integral_2026-10-22.md) e na [passagem](segunda_revisao_chatgpt.md).

**Parar em REV01.** Após a segunda revisão, registrar as decisões em R15 e atualizar as tarefas afetadas. Só então executar as correções pequenas R22, completar K2 e iniciar o percurso autorizado. O projeto 2026–2027 não está concluído.
