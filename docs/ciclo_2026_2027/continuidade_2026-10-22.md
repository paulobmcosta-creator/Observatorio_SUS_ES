# Continuidade atual — revisão integral, 22/10/2026

**Próximo passo: REV01, segunda revisão no ChatGPT com o coordenador. Não iniciar implementação ampla.** A rodada vigente conclui revisão crítica e planejamento, conforme o prompt v2 adotado pelo usuário. O relatório 2025–2026 permanece encerrado e não foi alterado.

Branch: `feat/ciclo-2026-2027-transicao`. Base desta revisão: `937056af0af34b81d27ec38b608f5356488b46a7`; base histórica da transição: `6478f93a50d03270a78959730221f2ea5a643658`. As rodadas anteriores foram publicadas em e75e81c/47bc932/937056a. O SHA final desta entrega e a comparação imutável constam da resposta de encerramento; [passagem de trabalho](segunda_revisao_chatgpt.md) explica como identificar a versão. Sem merge na main.

## Ordem de leitura e decisão

1. [Parecer crítico integral](parecer_revisao_integral_2026-10-22.md): achados, evidências, alternativas e limites.
2. [Plano operacional](plano_operacional.md) e [49 tarefas](tarefas_operacionais.csv): O1–O6, toda a agenda herdada, sete marcos, três planos formativos e capacidade.
3. [Inventário atualizado](inventario_transicao.csv), [matriz](matriz_indicadores_preliminar.csv), [avaliação](avaliacao_preliminar.csv) e [protocolo](protocolo_validacao.md): decisões por produto e candidato, sem homologação fictícia.
4. [Primeiro percurso proposto](primeiro_percurso_analitico.md): SIH/RD nacional 202401, residentes ES, S03/S04, seguido de 202402 para demonstrar atualização.
5. [Entrega para a segunda revisão](segunda_revisao_chatgpt.md), com pedidos residuais agrupados e retomada.

Após a segunda revisão, registrar as decisões em R15 e ajustar as tarefas afetadas. As decisões novas são núcleo/percurso, profundidade das expansões e capacidade funcional, além do encaminhamento do acervo. R22 está pronta para corrigir proveniência temporal; K2 fecha referências e contrato do primeiro uso antes da aquisição/análise. LT/ES/202401 continua ensaio útil de oferta em R32, mas não bloqueia universalmente SIH ou os demais produtos.

## Avanços preservados e limites atuais

- RAW CNES recuperado por hash e cache gzip verificado; LFS histórico preservado. Fonte/data da aquisição primária antiga ainda não comprovadas. Não recomeçar recuperação nem converter hash em proveniência oficial.
- Derivados isolados de 202601 com chaves operacionais/públicas distintas; comparação anterior 12.548 estabelecimentos e 1.963 habilitações, 115 verificações, igualdade com rodada 2. Os snapshots legados continuam preservados e não são entrada vigente do contrato novo.
- Proteção contra descarte implícito, aplicador territorial versionado e perfis institucional/TCC separados. Testes sintéticos não validam a tabela territorial real, que segue sem composição oficial preenchida.
- Inventário de 78 códigos, fila de 555 combinações e fichas preparatórias continuam diagnósticos. As 501 habilitações selecionadas são registros; 304 com status interno validado e 197 em revisão não são homologação normativa.
- PoC anterior CSV nacional 602.160×56 → Parquet → CSV → R: paridade integral, 115 verificações; auditoria DuckDB e preservação dos zeros. Não equivale a aquisição DBC real ou cobertura histórica.
- Avaliação de 13 candidatos e 14 famílias/usos preservada. DataHub é `rafa-trindade/kaggle-datahub`, pin `60aa9cbd82509e0595d5c99ec74794e6be1588bd`: seis casos locais sustentam alternativa por uso, não adoção integral. PySUS 2.0.4 permanece versão avaliada operacionalmente no escopo local; HEAD 2.11.7 somente inspecionado. Pins remotos PySUS/microdatasus/DataHub não mudaram nesta consulta.
- D2 mantém 2014–2024, G0–G5, desenho regional/focal e Brasil 2010 em seu escopo. Não reabrir essas decisões nem torná-las padrão global. Composição/versão territorial, população, normas históricas e outros pins precisam de fontes verificadas. IAM pendente afeta IAM; tendência prematura e limiares seguem decisões específicas.

R permanece onde adequado, com custo de manutenção justificável; Python/PySUS é preferencial na engenharia por família validada. Não há migração total obrigatória. Os [diagnósticos desta revisão](../../metadata/ciclo_2026_2027/revisao_integral_20261022/diagnosticos.csv) confirmam origem fixa em 202601, prioridade de município gestor e limitações de brancos/competências nas contagens técnicas. Produção não foi corrigida nesta rodada: R22/R23 delimitam a adequação posterior.

## Verificações e acesso

Os registros anteriores de 16 scripts R e 55 testes Python aprovados localmente continuam evidências daquelas execuções. **CI remoto R e Python observado com sucesso no commit `47bc932fe3955ac3759d4b7bc5094c016db03cd3`**, na listagem web do GitHub. Não atribuir esse resultado a outro commit; não foram lidos os logs completos. [Registro preciso](../../metadata/ciclo_2026_2027/revisao_integral_20261022/ci_remoto.json). Esta rodada executou somente três diagnósticos novos e conferências documentais/estruturais; não repetiu a suíte de produção sem alteração que o justificasse.

A política de rede permanece restrita e não há conector Drive disponível. Não foram repetidos acessos recusados sem mudança de condição. O [parecer](parecer_revisao_integral_2026-10-22.md) lista os materiais externos faltantes por produto e as decisões afetadas: relatório/acervo, Oncologia, Cardiologia, RUE individual e municipal, MVP principal/v2, comunicação e eventual parecer anterior. Ausência no checkout não significa inexistência.

Não há novo resultado substantivo a divulgar. [Recálculos](produtos_recalculo_dossies.csv) distinguem paridade já comprovada, correção futura de metadado, nova versão de oferta e primeiro cálculo SIH/TCC. Logs, fontes fornecidas, dados e código de produção foram preservados; o estado documental anterior permanece no Git em 937056a e nos backups históricos já existentes. O projeto 2026–2027 continua em execução futura; esta rodada termina na entrega para revisão.
