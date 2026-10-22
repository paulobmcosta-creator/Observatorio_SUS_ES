# Matriz preliminar e protocolo de validação

Versão de trabalho atualizada na revisão integral de 22/10/2026; incorpora D1/D2 v1.0 (03/10/2026) e o [parecer vigente](parecer_revisao_integral_2026-10-22.md). Base: proposta pp. 12–16, especialmente a definição da validação documental, operacional e analítica nas pp. 13–14. Não há homologação nesta rodada.

## Seleção proposta e organização dos arquivos

A [matriz](matriz_indicadores_preliminar.csv) funciona como ficha por candidato: fonte/versão, campos, disponibilidade, numerador/denominador, fórmula, unidade, filtros, contagem, território, período, agregação, validação e pendências. O CSV é UTF-8, separado por vírgulas, com campos citados quando contêm vírgulas. `Não aplicável`, `não localizado` e `não avaliado` são informações distintas; não devem ser substituídas por zero.

| Grupo | Itens | Decisão preliminar |
|---|---|---|
| T01–T06 | Seis medidas existentes do piloto R | Manter como diagnóstico de processamento e descrição cadastral; não contar como matriz substantiva regional validada |
| S01 | Estabelecimentos com habilitação selecionada por linha de cuidado | Núcleo de oferta condicionado: saída isolada tecnicamente conferida; localização física e normas ainda em revisão |
| S02 | Registros de habilitação selecionados | Controle complementar de registros, proposto como apoio a S01; não compõe automaticamente o núcleo substantivo |
| S03 | AIH normais aprovadas de residentes por território | Primeiro percurso proposto, após verificar layout, competência de processamento e regra AIH |
| S04 | Proporção de internações fora da região de residência | Primeiro percurso com S03: cobertura nacional, correspondência oficial, destinos conhecidos e ignorados explícitos |
| S05–S06 | Produção ambulatorial selecionada e óbitos por causas selecionadas | Expansão por pergunta: produção requer seleção/quantidade e mortalidade é complementar institucional; D2 mantém suas prioridades. Fontes estruturantes não tornam toda medida parte do núcleo |
| S07–S08 | Leitos e equipamentos | Expansão da oferta: estoques mensais, existentes/em uso/SUS separados e cobertura anual explícita |
| S09 | Pessoas profissionais, vínculos e horas | Família a desdobrar em três fichas; identificador válido para pessoas, sem soma territorial de distinct |
| S10 | ICSAP | Complementar da rede APS-hospital; lista, residência, regra AIH e população verificadas; taxa/proporção distintas |

O número de linhas é uma escolha operacional desta proposta preliminar, **não uma meta quantitativa do projeto**. A primeira matriz candidata concentrou-se em oferta cadastrada, utilização e fluxo. Isso não limita a infraestrutura comum: SIM/SIA, SIGTAP, população e território devem ser incorporados progressivamente (D1 Q7), sem tornar cada indicador temático obrigatório no núcleo institucional. S02 é proposto como apoio de S01, com justificativa registrada. A ordem atual é S03/S04, S01 quando elegível e expansão conforme [plano](plano_operacional.md); não houve homologação dos candidatos.

As seis medidas do piloto também não são as seis famílias analíticas futuras do roadmap. Elas podem excluir `NA` mas contar strings vazias; T02/T06 não impõem recorte mensal e podem reunir competências. Esses limites constam da matriz; não houve mudança no código histórico para fazê-lo coincidir com uma definição futura.

## Dimensões e evidências

A [avaliação preliminar](avaliacao_preliminar.csv) aplica qualitativamente as dimensões abaixo a cada uma das 16 linhas da matriz. As células descrevem evidência ou lacuna, sem pontuações. A leitura territorial e temporal foi separada para não ocultar que uma única competência não comprova comparabilidade temporal.

| Dimensão | Pergunta de avaliação | Evidência exigida |
|---|---|---|
| Relevância sanitária | O fenômeno é pertinente à atenção especializada? | Justificativa vinculada ao problema e ao recorte selecionado |
| Aderência aos objetivos | A medida responde a um dos seis objetivos? | Objetivo e pergunta de planejamento explícitos |
| Clareza operacional | Outra pessoa consegue aplicar a mesma regra? | Fórmula, filtros, campos, unidade e tratamento de ausentes |
| Estabilidade conceitual | Definição e classificação persistem no tempo? | Layouts/normas versionados e tabela de mudanças |
| Disponibilidade | Fonte pública acessível contém os campos necessários? | Fonte oficial, versão, extração e amostra inspecionada |
| Completude | Quais campos/territórios/períodos faltam? | Contagens absolutas, denominadores e padrão de ausência |
| Consistência | Chaves, vínculos e totais são coerentes? | Testes negativos, reconciliação e registro de divergências |
| Comparabilidade territorial | Os territórios e papéis das variáveis são equivalentes? | Correspondência oficial versionada, vigência e cardinalidade |
| Comparabilidade temporal | Os períodos representam o mesmo fenômeno? | Competências disponíveis, defasagem e situação preliminar/final |
| Periodicidade | É possível atualizar mantendo a definição? | Frequência da fonte, procedimento e registro de atualização |
| Sensibilidade às desigualdades | A medida permite leitura territorial pertinente? | Distribuições, cobertura e análise de artefatos de registro |
| Inteligibilidade | Título, unidade e limites são compreendidos? | Revisão documentada dos rótulos e teste de leitura supervisionado |
| Utilidade potencial para gestão | Que decisão/discussão pode subsidiar? | Pergunta concreta e registro de apreciação quando houver; não presumir adoção |

Não há pesos, notas de corte nem percentuais de qualidade aprovados. Uma futura proposta de escala deverá ser explicitamente proposta, fundamentada e deliberada antes de usada como critério de exclusão. Os requisitos de chave e estrutura de CSV são verificações técnicas, não limiares de qualidade assistencial.

## Três eixos de validação

1. **Documental — P1 com curadoria P3 supervisionada:** conferir definição, literatura, fonte oficial, manual, classificação, norma e vigência; registrar URL, versão e data de consulta. As referências da proposta (por exemplo OPAS 2018, WHO 2010 e Guerra et al. 2023) orientam a revisão, mas não foram consultadas externamente nesta rodada. S04 não é declarado reprodução do índice publicado de dependência regional. A aprovação documental requer justificativa e decisão registrada do responsável metodológico.
2. **Operacional — P2:** congelar insumos, preservar tipos textuais, verificar schemas, chaves e cardinalidades, executar casos válidos e inválidos e conciliar totais. Registrar código, ambiente, comando, resultado e SHA-256 de insumos/produtos. Script que retorna zero sem avaliar campos não é comprovação suficiente. Neste incremento a saída 1 sobre o snapshot é a detecção correta de incompatibilidade; não é aprovação do dado.
3. **Analítica — P1/coordenação:** verificar se a medida expressa o fenômeno definido, se permite comparação territorial/temporal e se variações podem ser artefatos de fonte. Analisar ausências, regras de contagem, denominadores, vigência, pequenos números e limites de interpretação. Registrar revisão e decisão; os testes automatizados não substituem essa etapa.

O formulário de decisão de cada candidato deve conter: ID/versão; evidências por dimensão; parecer documental/operacional/analítico; limitações; escopo aceito; pendências; responsável efetivo; data e referência da decisão. Enquanto não houver pessoas designadas, registrar **responsável funcional a designar**, sem atribuir participação a alunos do ciclo anterior.

## Estados e transições

- `candidato`: pertinência sugerida; definição e dados ainda incompletos.
- `especificado`: regra operacional completa, com pendências de dados explícitas.
- `calculável com evidência`: insumos e campos conferidos; regra aplicável, sem pressupor validade analítica.
- `testado`: comportamento verificado em escopo declarado (fixtures ou dados), com resultados e limitações.
- `em revisão metodológica`: divergência ou decisão substantiva pendente; não publicar como validado.
- `validado no escopo documentado`: três eixos apreciados e decisão identificável, com território/período/fonte explícitos.
- `excluído com justificativa`: critério e alternativa registrados; ausência de dados pode motivar adiamento, sem irrelevância sanitária presumida.

Os estados não são automaticamente uma escala crescente: uma mudança de layout, norma, território ou período reabre a revisão. O status interno `validado` da classificação de habilitações não promove S01/S02 para `validado no escopo documentado`. Não usar `homologado` sem decisão formal comprovada.

## Regras transversais de cálculo

CNES público, `CO_UNIDADE` e códigos municipais são textos e conceitos distintos. Não recompor identificadores por truncamento, concatenação ou preenchimento. Obter correspondência oficial município–região com fonte, vigência e regra temporal; exigir unicidade por período e registrar municípios não associados. Não chamar gestor de município de atendimento ou residência.

Estoques CNES mensais não se somam como produção anual. Fluxos SIH/SIA exigem regra de eventos/procedimentos e competência; internações, AIHs, pessoas e procedimentos não são equivalentes. Agregações de razões recalculam numerador e denominador, sem média simples de taxas municipais. Denominador zero produz valor não calculável/NA, nunca taxa zero; ausência de registro não vira zero observado. Registros sem território ficam explicitamente não classificados. Política de supressão de pequenos números deve ser deliberada antes da comunicação, sem limiar inventado nesta rodada.

Cadastro não comprova funcionamento, acesso, suficiência, qualidade ou vazio assistencial. Comparações são descritivas; não há inferência causal nem junções individuais entre sistemas sem chaves válidas. A análise prevista é pública e agregada, sem ampliação tácita para dados restritos ou coleta primária.

## Regras incorporadas pelos dossiês

O [registro de reconciliação](reconciliacao_dossies.md) distingue método decidido de implementação comprovada. A arquitetura é híbrida: Python preferencial para aquisição/engenharia quando validado; R permanece referência nos componentes já conferidos. As rotinas R existentes e o cache íntegro são reutilizados. PySUS não é requisito científico e sua cobertura é demonstrada por família, sem generalizar sucesso ou falha. Não houve migração; AGENTS.md foi alinhado às decisões híbridas já autorizadas, preservando os controles. R permanece onde adequado, sem obrigação de substituição futura.

A configuração institucional não tem período empírico nem CID global. O perfil do TCC separa 2014–2024, grupos cardiovasculares, padronização Brasil 2010, recorte focal e tendência seletiva. A tabela territorial é central; o estudo congela versão/hash e a aplica retrospectivamente. Os quatro nomes regionais e Noroeste 1 como focal já são decisões do D2; sua composição e a data/versão da fonte ainda devem ser verificadas. O contrato antigo de município gestor continua útil para o diagnóstico de 202601 e não é apresentado como localização da oferta.

A síntese anual quantitativa CNES será a média dos meses válidos, acompanhada do número de competências, última válida, mínimo/máximo e meses ativos quando pertinentes. Ano incompleto é parcial, sem limiar de publicação inventado. Ausência de arquivo não é zero; zero de recurso exige competência observada. Pessoas profissionais distintas devem ser recalculadas em cada nível territorial, separadas de vínculos e horas SUS. Nenhuma série anual foi calculada nesta rodada.

População residente total é o denominador padrão; não subtrair beneficiários ANS. A série anual harmonizada deve ser congelada por estudo e permanecer distinta da população padrão de padronização. No TCC, os pesos Brasil 2010 para 30–69 devem ser renormalizados no intervalo; as faixas de apresentação não substituem os quinquênios de cálculo.

Exclusão é por análise; registros sem idade podem permanecer no total e não integrar padronização. Não aplicar casos completos nem deduplicação genérica. Os preparadores agora interrompem diante das duplicidades antes descartadas; nenhuma causa física foi presumida. EX01–EX07 são motivos temáticos, não perdas automaticamente somáveis. A validade SIGTAP deve ser verificada por competência; as listas do Apêndice A continuam preliminares.

Fluxos mantêm origem/destino ignorados e externos explicitamente. O complemento 100−F1 do D2 só equivale à evasão quando a classificação de destinos é completa; o prompt complementar exige cálculo direto e transparência das perdas. Não medir evasão interestadual com cobertura apenas de prestadores ES. Regras de AIH, cobertura SIA, qualidade, pequenos números e ética permanecem pendentes no escopo afetado.
