A branch organiza a continuidade do ciclo 2026–2027 com contratos e evidências verificáveis e uma revisão integral de O1–O6 e da agenda herdada. O planejamento encerra em REV01, segunda revisão no ChatGPT com o coordenador, antes de implementação ampla; parecer, tarefas, especificação do primeiro percurso e limites estão em `docs/ciclo_2026_2027/segunda_revisao_chatgpt.md`. O relatório 2025–2026 permanece intacto.

O ciclo 2026–2027 precisava de contratos verificáveis e de uma reconciliação entre o projeto, os dois dossiês e os produtos existentes. Esta mudança incorpora o plano de continuidade, separa o perfil institucional do TCC cardiovascular e acrescenta validações que interrompem o processamento diante de chaves ausentes, duplicidades ou divergências territoriais, preservando o relatório 2025–2026.

## Entregas

- Documentos de transição, matrizes de impacto/recálculo, tarefas, referências originais e manifestos de proveniência.
- Contrato CNES, cache gzip verificado por hash e seleção explícita da fonte: os preparadores podem trabalhar com o cache sem materializar o ponteiro LFS histórico. O objeto e o histórico LFS permanecem preservados.
- Preparadores R sem descarte silencioso de duplicidades, correspondência territorial com versão/papel explícitos e fila de revisão de habilitações.
- Configuração do TCC 2014–2024 separada do Observatório; candidatos de procedimentos continuam preliminares, sem promoção à seleção final.
- Serialização PyArrow com conferência integral e auditoria DuckDB, mantendo R como referência de paridade.
- Avaliação de 13 candidatos/versões e 14 linhas de cobertura, incluindo PySUS, microdatasus e DataHub Brasil identificado pelo pesquisador. Python/PySUS permanece preferencial em engenharia quando validado por família; DataHub é alternativa condicionada, sem adoção integral.

## Validação local registrada

- 16 scripts R concluídos com sucesso na reconciliação; 55 testes Python aprovados na avaliação de ferramentas.
- CSV nacional CNES com 602.160 registros e 56 campos: conversão integral, restituição e paridade dos preparadores R em 12.548 estabelecimentos e 1.963 habilitações; 115 verificações aprovadas.
- Seis casos DataHub: referência R de 12.548×18 preservada; cenários controlados demonstram limites em partes PA, schema, manifesto por tamanho e leitura tolerante.
- Hashes dos 29 artefatos da última complementação conferidos antes dos commits. Código e evidências preservados na publicação; CSVs CRLF e cópias de anexos mantidos byte a byte.

Logs e resultados estão em `metadata/ciclo_2026_2027/`. O CI remoto ainda precisa ser conferido; resultados locais não são apresentados como aprovação do GitHub Actions.

## Limites e continuidade

Não foram obtidas novas séries oficiais/Kaggle nesta avaliação. Território oficial congelado, denominadores estratificados, SIGTAP histórico e cobertura operacional por família permanecem pendentes. As séries substantivas do TCC ainda não foram calculadas. A próxima prova de aquisição continua sendo LT/ES/202401 oficial com hash, dois leitores e comparação antes de ampliar a cobertura.

O relatório 2025–2026, dados históricos e regras já compatíveis foram preservados. Microdados/cache grandes ficam fora do commit; não houve migração destrutiva de LFS nem nova publicação de bases brutas. O ponto de retomada está em `docs/ciclo_2026_2027/continuidade_2026-10-22.md`.
