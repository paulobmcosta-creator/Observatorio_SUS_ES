# Continuidade do Observatório SUS-ES — ciclo 2026–2027

**Estado vigente: revisão crítica e planejamento integral, concluídos em 22/10/2026 para segunda revisão no ChatGPT com o coordenador (REV01).** Não iniciar implementação ampla. O projeto tem vigência setembro/2026–agosto/2027; esta entrega não é o relatório final nem uma matriz regional homologada.

Começar pelo [parecer](parecer_revisao_integral_2026-10-22.md), seguido do [plano integral](plano_operacional.md), [tarefas](tarefas_operacionais.csv), [primeiro percurso proposto](primeiro_percurso_analitico.md) e [passagem para a segunda revisão](segunda_revisao_chatgpt.md). O [ponto de continuidade](continuidade_2026-10-22.md) registra a próxima ação e as limitações.

O [inventário vigente](inventario_transicao.csv) cobre 25 produtos/componentes; [matriz](matriz_indicadores_preliminar.csv) e [avaliação](avaliacao_preliminar.csv) cobrem 6 controles e 10 candidatos/famílias. Há 49 tarefas para O1–O6, agenda herdada, três planos formativos e revisão. Propõe-se S03/S04 via SIH/RD nacional 202401, atualização 202402 e S01 quando elegível; não houve cálculo desses indicadores nesta rodada. R22/R23 especificam correções demonstradas por diagnósticos, ainda sem mudança em produção.

## Avanços anteriores preservados

- [Primeira rodada](diagnostico_transicao_2026-10-22.md): inventário, matriz preliminar e [conferência negativa de contratos](primeiro_incremento.md), refletindo o estado daquele instante.
- [Rodada 2](rodada_02_armazenamento_cnes.md): fonte LFS recuperada, cache gzip verificado, schema/fixture corrigidos, derivados isolados e 115 verificações aprovadas.
- [Rodada 3](rodada_03_territorio_habilitacoes.md): diagnóstico de 78 códigos municipais, 555 combinações e 12 fichas preparatórias; fontes territoriais/normativas ainda pendentes.
- [Reconciliação D1/D2](reconciliacao_dossies.md): [33 decisões confrontadas](matriz_impacto_dossies.csv), proteção contra descartes, perfis separados, território versionado e reprocessamento sem diferença. [Recálculos e primeiros cálculos](produtos_recalculo_dossies.csv) distinguem o que existe do que está proposto.
- [Ferramentas](avaliacao_ferramentas_2026-10-22.md): [13 candidatos](matriz_decisao_ferramentas.csv), [cobertura por família](cobertura_ferramentas_por_familia.csv), serialização Arrow e paridade R/DuckDB. [DataHub Brasil](avaliacao_datahub_2026-10-22.md) identificado e avaliado com seis casos; alternativa condicionada por uso, sem adoção integral.

Os workflows R e Python foram observados com sucesso em **47bc932fe3955ac3759d4b7bc5094c016db03cd3**. A [evidência](../../metadata/ciclo_2026_2027/revisao_integral_20261022/ci_remoto.json) não certifica outro commit, nem validade sanitária. Registros antigos de CI não executado referem-se àquelas etapas anteriores.

## Fontes, versões e publicação

O [projeto original](referencias/proposta_2026_2027.pdf) define O1–O6, produtos, três planos e [cronograma](cronograma_proposta.csv). O [prompt inicial](referencias/solicitacao_primeira_rodada.md) documenta a agenda herdada. Os DOCX D1/D2 e respectivos textos integrais estão em `referencias/`, com [hashes](referencias/dossies_sha256.csv). O [prompt atualizado v2](referencias/Prompt_Codex_Revisao_Planejamento_Observatorio_2026_2027_v2.md), adotado pelo usuário, substitui a implementação ampla por revisão e planejamento nesta rodada. Originais não foram alterados.

O relatório encerrado e o acervo externo continuam sem acesso disponível; produtos relatados não foram classificados como inexistentes. As lacunas e decisões dependentes estão no parecer. Não se inferiram autoria, participação discente, reuniões, bolsas ou uso institucional.

Branch: `feat/ciclo-2026-2027-transicao`. Base da revisão: `937056af0af34b81d27ec38b608f5356488b46a7`; base histórica: `6478f93a50d03270a78959730221f2ea5a643658`. As entregas anteriores já foram enviadas ao GitHub; [registro de publicação](publicacao/estado_publicacao.md). O SHA final e a comparação imutável desta revisão são identificados no encerramento e na orientação de [passagem](segunda_revisao_chatgpt.md).

**O relatório 2025–2026 não recebeu alteração.** Não houve implantação de painel, merge, escrita remota no relatório, mudança de permissões ou comunicação a terceiros. As versões documentais anteriores e suas evidências permanecem no histórico Git.
