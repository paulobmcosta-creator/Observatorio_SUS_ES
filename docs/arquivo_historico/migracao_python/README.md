# Arquivo histórico da migração Python/PySUS

## 1. Finalidade

Esta pasta preserva o histórico completo da migração R–Python/PySUS no Observatório SUS-ES, especialmente os documentos da Etapa 5N relacionados à avaliação de viabilidade do PySUS para CNES.

Os arquivos aqui mantidos registram diagnósticos, hipóteses, provas de conceito, decisões humanas, contratos intermediários, limitações encontradas e conclusões metodológicas. Eles foram preservados para garantir rastreabilidade e permitir auditoria futura das decisões técnicas tomadas no projeto.

## 2. Por que foi arquivado

A documentação detalhada da migração é metodologicamente importante, mas extensa demais para ser a entrada pedagógica de um aluno. Ela inclui subetapas diagnósticas, tentativas controladas, avaliações de instabilidade e registros de problemas que podem ser confundidos com orientações atuais de execução.

Por isso, esses documentos foram removidos da navegação principal e arquivados aqui de forma reversível. A consulta deve ocorrer apenas com mediação ou quando houver dúvida específica sobre decisões técnicas anteriores.

## 3. Decisão consolidada

- A Etapa 5N foi encerrada com ressalvas.
- PySUS é viável para acesso e mapeamento estrutural do CNES, com ressalvas.
- A transformação em memória é apenas parcial.
- ST permanece instável/intermitente.
- `CO_UNIDADE` permanece não resolvido.
- R permanece como oráculo metodológico.
- A geração de base não está autorizada.
- A substituição de scripts R não está autorizada.

## 4. Como consultar

O pesquisador ou orientador deve consultar estes documentos quando precisar recuperar a justificativa de uma decisão técnica, revisar limitações do PySUS/CNES, entender a origem do contrato intermediário ou explicar por que a migração Python não é atualmente o caminho produtivo do projeto.

Para entrada pedagógica do aluno, use `docs/guias_aluno/`. Para o status consolidado da migração, use `docs/migracao_python/README.md`.

## 5. Índice dos documentos arquivados

- `00_baseline_r_pre_migracao.md`
- `01_classificacao_legado_r.md`
- `02_governanca_arquitetura_hibrida.md`
- `03_poc_pysus_cnes.md`
- `04_contratos_extracao_cnes_python.md`
- `04_deliberacao_humana_pre_etapa5.md`
- `04_revisao_pos_etapa4.md`
- `05N1_isolamento_pysus_duckdb_cnes.md`
- `05N2_diagnostico_falha_cnes_pos_isolamento.md`
- `05N3R_reteste_controlado_st_cnes_pysus.md`
- `05N3_inventario_grupos_cnes_pysus.md`
- `05N4_mapeamento_estrutural_grupos_cnes_pysus.md`
- `05N5_mapeamento_multicompetencia_cnes_pysus.md`
- `05N6R_deliberacao_humana_contrato_intermediario_pysus_cnes.md`
- `05N6_contrato_intermediario_pysus_cnes.md`
- `05N7_8A_validacao_minima_transformacao_memoria_cnes_pysus.md`
- `05N7_8D_diagnostico_timeout_transformacao_memoria_cnes_pysus.md`
- `05N7_8E_correcao_caminho_padrao_transformacao_memoria_cnes_pysus.md`
- `05N7_8F_diagnostico_st_transformacao_memoria_cnes_pysus.md`
- `05N7_8G_diagnostico_acesso_st_pysus_cnes.md`
- `05N7_8_transformacao_memoria_multicompetencia_cnes_pysus.md`
- `05N_encerramento_viabilidade_pysus_cnes.md`
- `05N_reinicio_cnes_python_api_pysus.md`
