# Pertencimento de estabelecimentos — dados integrais e agregados

Os dois arquivos originais de pertencimento por CNES/competência estão incluídos integralmente na candidata pública v3.5.1:

- [Pertencimento mensal — Parquet](arquivos_homologados/10_SOBREPOSICOES_v341/02_tabelas/pertencimento_mensal.parquet) — 950.730 linhas, 100 campos.
- [Pertencimento anual — Parquet](arquivos_homologados/10_SOBREPOSICOES_v341/02_tabelas/pertencimento_anual.parquet) — 167.288 linhas, 101 campos.

Os arquivos preservam a chave CNES, a dimensão temporal e os indicadores de serviços, equipamentos e produção. A análise técnica relatada comparou 1.144 margens com tabelas de referência, sem divergências. Esses registros se referem a **estabelecimentos**, não a indivíduos atendidos. A identificação de um estabelecimento não comprova identificação de paciente, mas pode ser possível reconhecer prestadores e inferir características em combinação com outras fontes.

As tabelas de interseções mensais e anuais continuam disponíveis como sínteses estatísticas; **não substituem** os campos detalhados dos dois Parquet. Consultar [a nota de risco](../../docs/estudos/tcc_camila/NOTA_RISCO_DIVULGACAO.md) e o [catálogo de origem](../../docs/estudos/tcc_camila/CATALOGO_RESULTADOS_318.csv).

Esta página integra uma candidata local; os links só serão públicos após incorporação ao GitHub.
