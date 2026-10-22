# Continuidade do Observatório SUS-ES — ciclo 2026–2027

**Publicação:** entregas enviadas à branch `feat/ciclo-2026-2027-transicao`; [estado do envio e preparação do pull request](publicacao/estado_publicacao.md).

Rodada executada em **22/10/2026**, M2 do projeto. Referência: proposta com vigência de 01/09/2026 a 31/08/2027. Os documentos desta pasta são entregas de transição e trabalho preliminar; não são o relatório final nem a matriz regional validada.

**Atualização posterior — rodada 2:** [fonte recuperada, alternativa ao LFS e comparação isolada](rodada_02_armazenamento_cnes.md). R04/R05 foram executadas: cache gzip verificado, schema/fixture corrigidos e 115 verificações aprovadas na nova saída de comparação. Os diagnósticos e evidências da primeira rodada abaixo foram preservados como registro do estado anterior. O próximo trabalho metodológico é R06/R07.

**Rodada 3 — diagnóstico preservado:** [inventário territorial e fila de revisão das habilitações](rodada_03_territorio_habilitacoes.md). Contrato territorial testado, 78 códigos inventariados, 555 combinações triadas e 12 fichas preparatórias. R06/R07 permanecem pendentes de consulta às fontes oficiais, bloqueadas pela política de rede; a nota lista os quatro hosts necessários e o ponto exato de retomada.

**Reconciliação D1/D2:** [registro metodológico e resultados](reconciliacao_dossies.md), [matriz de impacto](matriz_impacto_dossies.csv), [produtos e recálculos](produtos_recalculo_dossies.csv) e [continuidade atualizada](continuidade_2026-10-22.md). Bases de comparação reprocessadas sem diferença; perfis institucional/TCC separados; proteção contra descarte e território congelado testados. As pendências oficiais continuam explícitas.

**Ponto atual — ferramentas e prova de conceito:** [avaliação com fontes originais](avaliacao_ferramentas_2026-10-22.md), [matriz de decisão](matriz_decisao_ferramentas.csv) e [cobertura por família](cobertura_ferramentas_por_familia.csv). Serialização PyArrow/Parquet e auditoria DuckDB verificadas com paridade R; aquisição remota bloqueada; PySUS continua preferencial sob validação por família; DataHub Brasil foi [identificado e avaliado com seis casos locais](avaliacao_datahub_2026-10-22.md): alternativa condicionada, sem adoção integral. O plano único R08/R19 e a continuidade incorporam esses resultados.

## Entregas e ordem de leitura

1. [Diagnóstico de transição](diagnostico_transicao_2026-10-22.md) e [inventário verificável](inventario_transicao.csv).
2. [Matriz preliminar](matriz_indicadores_preliminar.csv), [avaliação qualitativa inicial](avaliacao_preliminar.csv) e [protocolo de validação](protocolo_validacao.md).
3. [Plano operacional](plano_operacional.md), [tarefas priorizadas](tarefas_operacionais.csv) e [cronograma transcrito da proposta](cronograma_proposta.csv).
4. [Primeiro incremento: conferência de contrato](primeiro_incremento.md), com testes e evidências de uma **nova conferência local**.
5. [Registro de continuidade e ponto de retomada](continuidade_2026-10-22.md).

## Referências e precedência

- [Proposta recebida, preservada byte a byte](referencias/proposta_2026_2027.pdf): escopo, objetivos, metodologia e cronograma. As páginas citadas correspondem às 35 páginas físicas do PDF.
- [Prompt recebido, preservado byte a byte](referencias/solicitacao_primeira_rodada.md): escopo solicitado para esta rodada, explicitamente adotado pelo usuário. Suas descrições do primeiro ciclo foram tratadas como alegações a conferir, não como evidência de implementação.
- [Hashes dos anexos iniciais](referencias/fontes_sha256.csv) e [controle dos dois dossiês e complemento](referencias/dossies_sha256.csv). D1 define regras comuns; D2 define o TCC; código/logs demonstram implementação. O complemento foi adotado explicitamente pelo usuário.
- Checkout inspecionado: `6478f93a50d03270a78959730221f2ea5a643658`, igual à ponta remota de `main` na consulta desta rodada. Branch de trabalho: `feat/ciclo-2026-2027-transicao`.

Os arquivos, códigos e testes efetivamente inspecionados prevalecem para afirmar o que existe. O inventário anterior foi reaproveitado como ponto de partida; suas qualificações de maturidade não foram copiadas como conclusões atuais.

**O relatório 2025–2026 permanece encerrado e não recebeu nenhuma alteração.** A consulta somente de leitura ao Google Docs foi recusada pelo proxy; não houve auditoria editorial nem escrita remota. O PDF original e os snapshots históricos foram preservados. Não houve publicação de painel, merge, mudança de permissões ou comunicação a parceiros/estudantes.

## Resultado da primeira rodada — histórico preservado

Os totais legados conferem, mas os snapshots intermediários não atendem aos contratos atuais: falta `co_unidade`, o campo legado `cnes` não tem o formato de código público, há três nomes vazios e o schema de habilitações tem uma linha CSV malformada. O incremento transforma essas divergências em reprovações verificáveis. Ele não corrige as bases, não certifica indicadores e não substitui o R por Python/PySUS.
