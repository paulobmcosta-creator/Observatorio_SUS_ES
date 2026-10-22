# Prompt para o Codex — continuidade do Observatório SUS-ES, ciclo 2026–2027

Você dará continuidade ao desenvolvimento científico, metodológico e tecnológico do Observatório SUS-ES, tomando como referência principal o projeto de pesquisa **“Consolidação metodológica do Observatório SUS-ES: validação e atualização de indicadores da atenção especializada no Espírito Santo”**, com vigência de **01/09/2026 a 31/08/2027**.

Leia integralmente este comando e o PDF do projeto antes de executar alterações. Trabalhe em português brasileiro, com precisão acadêmica e documentação compreensível para estudantes e pesquisadores.

## 1. Instrução prioritária: preservar o relatório encerrado

**Não faça nenhuma nova alteração no relatório 2025–2026.** Não modifique texto, tabelas, imagens, legendas, links, referências ou formatação. Não produza uma nova versão desse relatório para substituir a existente.

O relatório poderá ser consultado somente como fonte histórica:
https://docs.google.com/document/d/1gmVyMUhK3o2CtsTEaeqVgk4lj08es5TlWbklIQGekWQ/edit

O objetivo desta tarefa é iniciar a execução organizada do novo ciclo, usando os produtos existentes como ponto de partida. Registre descobertas, divergências e decisões em documentos próprios de 2026–2027. Preserve também o PDF da proposta submetida.

## 2. Fontes, acesso e precedência

Utilize:

1. **PDF anexado: “Projeto de Pesquisa (2).pdf”** — referência principal para escopo, objetivos, metodologia, produtos esperados, cronograma e planos de trabalho de 2026–2027.
2. **Repositório:** https://github.com/paulobmcosta-creator/Observatorio_SUS_ES
3. **Acervo do primeiro ciclo:** https://drive.google.com/drive/folders/1mi6rvQeHxuCfcMJfOJtGmWRKL358WjZD
4. **Relatório encerrado**, apenas para consulta.
5. Arquivo de contexto do relatório, se estiver disponível: `CONTEXTO_OBSERVATORIO_SUS_ES_RELATORIO_2025_2026_21-10-2026(1).md`.

O arquivo de contexto é um registro de transição e pode estar desatualizado quanto às últimas edições. Na conferência realizada em 22/10/2026, vários itens nele descritos como pendentes já estavam no Google Docs; foram acrescentados outros seis hiperlinks e esclarecimentos pontuais. **Não reabra a auditoria editorial do relatório.**

Para definir o trabalho futuro, prevalece a proposta 2026–2027. Para afirmar o que já foi implementado, prevalecem arquivos, código, dados, testes e evidências efetivamente inspecionados. Uma expectativa escrita no projeto não prova uma entrega realizada.

Use os conectores disponíveis. Se estiver no Codex associado ao GitHub, examine primeiro o checkout e o estado da árvore de trabalho. Leia o `AGENTS.md` e as instruções aplicáveis aos caminhos em que trabalhará. Não descarte alterações existentes.

Caso o Drive ou algum documento não esteja acessível, registre a limitação e prossiga com as fontes disponíveis. Não invente conteúdo, caminhos, URLs, resultados de testes ou evidências. Só peça um arquivo quando sua ausência bloquear concretamente a próxima entrega.

## 3. Finalidade e escopo do novo ciclo

O problema central é transformar os produtos preliminares do Observatório em instrumentos mais estáveis, verificáveis, documentados, atualizáveis e úteis ao planejamento regional da atenção especializada.

Organize o trabalho pelos seis objetivos específicos:

1. Sistematizar os produtos técnico-científicos da primeira etapa.
2. Selecionar e validar uma matriz mínima de indicadores regionais.
3. Atualizar e padronizar bases oficiais, especialmente CNES e SIH/SUS e, quando pertinente, SIM; considerar SIA/SUS conforme o recorte de procedimentos especializados.
4. Aprimorar tratamento, conferência, documentação e versionamento dos dados.
5. Qualificar o painel-piloto quanto à coerência analítica, clareza, usabilidade e consistência entre bases e visualizações.
6. Produzir nota técnica, manual ou guia de atualização, relatório final do novo ciclo, resumo científico e materiais de comunicação.

Não transforme a consolidação em expansão indiscriminada de fontes, indicadores, especialidades ou funcionalidades. A prioridade é um núcleo mínimo metodologicamente defensável e reprodutível. A proposta não fixa um número obrigatório de indicadores: justifique a seleção, sem inventar uma meta quantitativa.

## 4. Ponto de partida conhecido — conferir uma vez

As informações abaixo são referências do encerramento do primeiro ciclo, e não resultados a serem novamente produzidos:

- O pipeline CNES em **R permanece a referência operacional e metodológica**.
- A trilha **Python/PySUS é experimental**, com limitações relacionadas à estabilidade de ST, equivalência de `CO_UNIDADE`, transformação e paridade. Sua existência não autoriza substituir o pipeline R.
- Existem duas bases intermediárias CNES de janeiro de 2026: estabelecimentos, com **12.548 linhas e 78 municípios**; habilitações, com **1.963 linhas e 1.283 CNES distintos**.
- A classificação de referência reúne **555 combinações código/tipo**, das quais **203** estão no escopo analítico.
- Na aplicação à base real, **501 registros** foram selecionados: **304 com validação interna** e **197 sob revisão**; **1.462** ficaram fora do escopo. Combinações de classificação, registros de habilitação e estabelecimentos são unidades diferentes.
- Existem **seis indicadores técnicos básicos em R**; isso não equivale à matriz mínima regional validada do novo projeto nem às seis famílias analíticas futuras.
- Os ciclos CNES 1–3 e a correção 3C foram executados. Os ciclos 4–12 eram planejamento; não os execute automaticamente como se fossem a programação obrigatória de 2026–2027.
- O MVP principal e a variante `v2_HARDENED_NAO_HOMOLOGADO.zip` são produtos distintos. A variante permanece não homologada até que haja evidência de revisão e decisão correspondentes.
- A análise municipal da RUE dispõe de script Python próprio, que utiliza bases intermediárias já consolidadas. Essa rotina é distinta da migração experimental Python/PySUS.
- O manifesto JSON com os hashes da execução histórica da RUE não foi localizado na pasta auditada. Um manifesto regenerado deverá ser identificado como **nova execução**, sem ser apresentado como prova retrospectiva da execução antiga.
- Há cinco relatórios individuais substantivos. Produtos coletivos e análises de encerramento não devem ser atribuídos retroativamente aos estudantes. Não atribua produtos futuros aos participantes do primeiro ciclo sem evidência de vinculação ao novo.
- ICSAP e força de trabalho não possuem, pelo diagnóstico anterior, séries empíricas finais implementadas. Não as trate como entregas prontas.
- Não há comprovação suficiente, no acervo examinado, dos artigos e das notas gerenciais originalmente previstos nem de adoção institucional dos produtos pela gestão estadual.

Se encontrar diferenças no repositório atual, registre versão/commit, arquivo e evidência. Não restaure o estado antigo apenas para fazê-lo coincidir com esse resumo.

Documentos úteis para a leitura inicial, cujos caminhos devem ser conferidos no checkout:
- `docs/cnes/resumo_executivo_cnes.md`
- `docs/cnes/revisao_geral_observatorio_pre_novos_ciclos.md`
- `docs/cnes/contrato_dados_cnes_piloto.md`
- `docs/cnes/indicadores_cnes_oferta.md`
- `docs/cnes/roadmap_tecnico_cnes.md`
- `docs/cnes/setup_execucao_local_r.md`
- `docs/migracao_python/README.md`
- `docs/arquivo_historico/migracao_python/05N_encerramento_viabilidade_pysus_cnes.md`
- `docs/guias_aluno/README.md`
- `docs/matriz_manutencao.md`

O README geral contém afirmações amplas sobre pipeline completo e preferência por Python/PySUS que precisam ser confrontadas com os documentos técnicos. Não utilize essas afirmações isoladamente como comprovação de maturidade.

## 5. Primeira execução: diagnóstico delimitado e entrega concreta

Realize uma primeira rodada com começo, fim e critérios de conclusão:

### A. Inventário e diagnóstico de transição

Identifique os ativos necessários ao novo ciclo. Reutilize inventários existentes e complemente suas lacunas; não recomece toda a pesquisa.

Para cada produto relevante, registre:
- identificação, tipo, localização e versão/commit;
- fonte de dados, competência/período e unidade territorial;
- unidade de observação, variáveis e cálculo, quando aplicáveis;
- estado de implementação, atualização, documentação e validação;
- autoria/proveniência comprovada: individual, coletiva ou análise de encerramento;
- limitações e dependências;
- decisão proposta: reutilizar, revisar, atualizar, reformular ou manter apenas como histórico;
- objetivo e plano de trabalho de 2026–2027 ao qual se vincula.

Não trate cada arquivo auxiliar como uma entrega científica independente. Diferencie produto, insumo, documentação, teste e especificação.

### B. Matriz preliminar de indicadores e protocolo de validação

Construa uma matriz inicial a partir de medidas existentes e candidatos justificados pelo projeto. Distinga indicadores de qualidade do processamento de indicadores substantivos da atenção especializada.

Para cada candidato, registre:
- nome, dimensão analítica e pergunta de planejamento;
- justificativa e relação com os objetivos;
- fonte e versão, campos necessários e disponibilidade verificada;
- numerador, denominador quando aplicável, fórmula, unidade, filtros e exclusões;
- unidade de contagem, território, período e regra de agregação;
- distinção entre residência, atendimento e município gestor, conforme a fonte;
- situação de cálculo e de validação;
- limitações, evidências e pendências.

Aplique as dimensões previstas no projeto: relevância sanitária, aderência aos objetivos, clareza operacional, estabilidade conceitual, disponibilidade, completude, consistência, comparabilidade territorial e temporal, periodicidade, sensibilidade às desigualdades, inteligibilidade e utilidade potencial para a gestão.

Diferencie validação **documental, operacional e analítica**. Não considere um indicador validado apenas porque o script executou ou porque os campos foram preenchidos.

Não invente pesos, notas de corte ou percentuais de qualidade supostamente aprovados. Se sugerir uma escala ou limiar, identifique-o como proposta, fundamente-o e mantenha explícito o que depende de deliberação metodológica.

Use estados claros, por exemplo: candidato; especificado; calculável com evidência; testado; em revisão metodológica; validado no escopo documentado; excluído com justificativa. Não use “homologado” sem decisão formal comprovada.

### C. Plano de execução e primeiro incremento

Monte uma lista priorizada de tarefas vinculada aos seis objetivos e aos três planos de trabalho. Para cada tarefa, defina dependências, produto, critérios de aceite, evidências exigidas, responsável funcional e período previsto.

Depois, **implemente um primeiro incremento pequeno, útil e verificável**, compatível com os dados disponíveis e as instruções vigentes do repositório. Não encerre apenas com um plano genérico.

Selecione o incremento após o diagnóstico. Exemplos possíveis: uma rotina de conferência de contrato; registro reprodutível de execução; validação territorial; cálculo documentado de um indicador já viável; ou teste de consistência entre saída e regra metodológica. Escolha apenas o que tiver fundamento nos arquivos examinados.

Preferencialmente, use a competência histórica e fixtures existentes para verificar o comportamento antes de atualizar bases. Se regras aplicáveis impedirem execução ou escrita em áreas específicas, conclua as entregas permitidas e descreva a dependência precisa, sem contornar o controle.

Preserve snapshots anteriores. Não sobrescreva dados históricos, não execute migração geral de linguagem e não altere classificações clínicas/normativas silenciosamente.

## 6. Regras metodológicas e técnicas

- Preserve códigos CNES e IBGE como identificadores textuais, inclusive zeros à esquerda. Distinga CNES público de `CO_UNIDADE`.
- Verifique os formatos territoriais usados por cada fonte; não converta códigos apenas por truncamento ou preenchimento sem regra documentada.
- Para regiões de saúde, obtenha correspondência oficial e versionada município–região, com fonte, vigência e regra temporal. Não escolha uma regionalização com base apenas em memória ou em mapas anteriores.
- Registre competências disponíveis, defasagem e situação preliminar/final. Não escolha automaticamente a competência mais recente quando isso prejudicar a comparação entre fontes.
- Diferencie estoques cadastrais de fluxos de produção: não some estoques mensais como se fossem produção anual.
- Nas agregações, recalcule numeradores e denominadores; não faça média simples de taxas municipais sem justificativa.
- Não transforme ausência de registro em zero observado, nem denominador zero em taxa zero. Documente valores ausentes, não aplicáveis e suprimidos.
- Distinga pessoas, internações, autorizações, procedimentos, estabelecimentos, habilitações e vínculos profissionais.
- Cadastro de oferta não demonstra funcionamento, acesso, qualidade, suficiência ou vazio assistencial. Não faça inferências causais a partir de comparações descritivas.
- Não imponha junções individuais entre sistemas que não disponham de chaves válidas. Integrações territoriais e temporais devem explicitar granularidade e cardinalidade.
- Registre fonte oficial, URL, data/hora de extração, competência, filtros, campos, contagens, versão, responsável real pela execução e hashes dos insumos e produtos.
- Verifique documentação oficial para novos layouts, fontes, normas e regras territoriais; registre divergências e incertezas.
- Conserve camadas bruta, intermediária e final; documente mudanças de schema, perdas, duplicidades, divergências de totais e cobertura territorial.
- Trabalhe com o escopo de dados públicos e agregados previsto na proposta. Não introduza dados restritos, identificação individual ou coleta primária como extensão tácita.
- Não afirme validação por gestores, parceiros ou especialistas sem registro. COSEMS-RJ e IMS/UERJ são referências/parcerias previstas no projeto; isso não prova revisão de cada produto.

## 7. Três planos de trabalho — preservar independência e complementaridade

**Plano 1 — PIBIC/PIVIC:** “Validação metodológica de indicadores regionais da atenção especializada no âmbito do Observatório SUS-ES”.
Atribuições: revisão bibliográfica/normativa, inventário analítico, critérios de validação, seleção dos indicadores, fichas metodológicas, interpretação territorial, nota técnica e resumo científico.

**Plano 2 — PIBIT/PIVIT:** “Automação e documentação de fluxo reprodutível de atualização de indicadores do Observatório SUS-ES”.
Atribuições: arquitetura dos arquivos, atualização e padronização das bases, rotinas, logs, dicionários, versionamento, testes, painel-piloto e manual técnico.

**Plano 3 — PIBIC-JR/PIVIC-JR:** “Curadoria de dados e comunicação científica de indicadores do Observatório SUS-ES”.
Atribuições: formação inicial, inventário documental, conferências supervisionadas de nomes/códigos/períodos, glossário, quadros simples e revisão de títulos, legendas, fontes e materiais de comunicação.

Não atribua ao estudante júnior responsabilidade autônoma por programação avançada, validação clínica/normativa ou análise estatística complexa. Não invente nomes, bolsas concedidas, horas executadas ou participação comprovada. Os campos não preenchidos para estudantes 4–6 no formulário são remanescentes do modelo, não novos planos ativos.

## 8. Cronograma

Mapeie os meses do projeto: M1 = setembro/2026; M2 = outubro/2026; M3 = novembro/2026; ...; M12 = agosto/2027.

Consulte o cronograma geral e os cronogramas individuais no PDF. Se a extração textual deslocar os “X” da tabela, confira visualmente a página antes de atribuir meses exatos.

Preserve a lógica da proposta:
- início: inventário, revisão aplicada e critérios;
- atualização de bases preferencialmente a partir de M3, com dependências metodológicas definidas;
- meses intermediários: padronização, consistência, documentação, cálculo e painel;
- etapa posterior: nota técnica, manual, comunicação e resumo científico;
- encerramento: consolidação dos produtos e relatório exclusivo de 2026–2027.

Distinga cronograma aprovado, situação comprovada e reprogramação proposta. Não marque atividades como concluídas porque a data prevista passou; não retrodate execuções.

## 9. Organização das entregas e limites de alteração

Produza arquivos novos do ciclo 2026–2027 em local coerente com a arquitetura existente. Como sugestão, use `docs/ciclo_2026_2027/` e subpastas pertinentes para matrizes e fichas; adapte após inspecionar o repositório, sem duplicar estruturas equivalentes.

Na primeira rodada, entregue:
1. Diagnóstico de transição com inventário verificável.
2. Matriz preliminar de indicadores e protocolo de validação.
3. Plano operacional com tarefas, dependências, critérios de aceite e articulação dos três planos.
4. Primeiro incremento implementado e sua verificação, ou impedimento específico quando houver bloqueio real.
5. Registro de continuidade com o ponto exato de retomada.

Pode consolidar documentos relacionados para evitar dispersão. Matrizes operacionais devem ser legíveis e reutilizáveis, preferencialmente em CSV UTF-8 e documentação Markdown.

Trabalhe em branch própria quando houver checkout Git. Preserve mudanças de terceiros e o histórico. Prepare alterações revisáveis; não faça merge na branch principal, não publique painel, não altere permissões e não envie mensagens a parceiros ou estudantes nesta tarefa. Não modifique instruções de governança para liberar operações bloqueadas.

Não gere nota técnica, resumo ou relatório final com resultados ainda inexistentes. Modelos podem ser preparados, mas devem estar identificados como modelos e conter pendências visíveis.

## 10. Verificação, conclusão e continuidade

Verifique apenas o necessário ao incremento:
- consistência dos arquivos e esquemas produzidos;
- testes pertinentes às regras implementadas;
- preservação dos dados históricos;
- rastreabilidade entre fonte, transformação e saída;
- coerência dos números e unidades;
- ausência de alterações no relatório 2025–2026.

Não declare teste executado quando apenas leu seu código. Não confunda sucesso de build com validade metodológica. Não recompute todo o acervo sem necessidade.

Evite ciclos repetitivos de leitura e planejamento. Faça um inventário delimitado, uma síntese das lacunas, uma implementação e uma conferência final. Se uma fonte falhar, registre a limitação e continue com as tarefas independentes.

Na resposta final, informe:
- diagnóstico em poucas linhas;
- arquivos e alterações efetivamente entregues;
- verificações realizadas e seus resultados;
- indicadores ainda candidatos e questões metodológicas pendentes;
- próximo incremento concreto e suas dependências.

Finalize com um ponto de retomada suficiente para outra sessão continuar sem refazer o inventário. **Comece agora pela leitura do projeto e do repositório; em seguida, execute a primeira rodada descrita acima.**

